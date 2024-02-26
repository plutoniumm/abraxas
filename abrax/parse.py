from re import compile
from _utils_parse import parse_circuit, isClose

# SHOULD start with -, everything else is comment
# ---, -1-, -1, -11, --11-
no_gate = compile('-(-|[0-9]*){1,}')


def parse_param(p, typ=None):
  if not isinstance(p, (str)):
    return p
  # if float or int continue
  if isinstance(p, (float, int)):
    return p
  # if not, it's a string, if includes . it's a float
  p = p.strip()
  try:
    if '.' in p:
      p = float(p)
      # check if it's pi,pi/2,pi/4
      from numpy import pi

      if isClose(p, 3.1415):
        return pi
      elif isClose(p, 1.570):
        return pi / 2
      elif isClose(p, 0.7853):
        return pi / 4

    else:
      return int(p)
  # this means we need to make a variable
  # since float/int didn't work
  except Exception:
    if typ is None or typ == 'qis':
      from qiskit.circuit import Parameter

      p = Parameter(p)
    elif typ['name'] == 'cuq':
      idx = typ['param_idx']
      typ['param_idx'] += 1
      return typ['quake'][idx]
    elif typ['name'] == 'pnl':
      typ['params'].append(0)
      return ('VAR', len(typ['params']))
    else:
      raise Exception('Invalid type')

  return p


# TODO: POLYFILL GATES
# nvidia_valid_gates = ['mx', 'my', 'mz']
# qc = QuantumCircuit provided by the user
"""
Qiskit Format
circuit.GATE(*params, wireNo)
"""


def resolve_qiskit(circuit, qc):
  for _, layer in enumerate(circuit):
    for wireNo, gate in enumerate(layer):
      if no_gate.match(gate):
        continue
      gate = gate.lower()
      if '(' in gate and ')' in gate:
        gate_name = gate[: gate.index('(')]
        param = gate[gate.index('(') + 1 : gate.index(')')]
        op = getattr(qc, gate_name)

        if ',' in param:
          param = list(map(parse_param, param.split(',')))
          param = param + [wireNo]
        else:
          param = [parse_param(param, 'qis'), wireNo]
      else:
        param = [wireNo]
        op = getattr(qc, gate)

      op(*param)
  return qc


# cudaO = [kernel, qubits, params]
# params = float | int | float[] | int[]
"""
Cudaq Format
kernel.gate(param?..., qubits[qubitno1], qubits[qubitno2]?...)
"""


def resolve_cudaq(circuit, cudaO):
  from cudaq import Kernel

  kernel = cudaO['kernel']
  qubits = cudaO['qubits']
  quake = cudaO['quake']
  cudaPass = {
    'name': 'cuq',
    'quake': quake,
    'param_idx': cudaO['params'],
  }

  def u(self, a, b, c, u):
    kernel.rz(b, u)
    kernel.ry(a, u)
    kernel.rz(c, u)

  Kernel.u = u

  for _, layer in enumerate(circuit):
    for wireNo, gate in enumerate(layer):
      if no_gate.match(gate):
        continue
      gate = gate.lower()
      if '(' in gate and ')' in gate:
        gate_name = gate[: gate.index('(')]
        param = gate[gate.index('(') + 1 : gate.index(')')]
        op = getattr(kernel, gate_name)

        if ',' in param:
          param = list(map(parse_param, param.split(',')))
          param = param + [qubits[wireNo]]
        else:
          if gate_name == 'cx':
            param = qubits[int(param)]
          param = [parse_param(param, cudaPass), qubits[wireNo]]
      else:
        param = [qubits[wireNo]]
        op = getattr(kernel, gate)

      op(*param)

  cudaO['params'] = cudaPass['param_idx']
  return kernel


# POLYFILL GATES
# SGD, TDG
# U1, U2, U3
def resolve_pennylane(circuit):
  gate_map = {
    'id': 'Identity',
    'h': 'Hadamard',
    'x': 'PauliX',
    'y': 'PauliY',
    'z': 'PauliZ',
    's': 'S',
    't': 'T',
    'rx': 'RX',
    'ry': 'RY',
    'rz': 'RZ',
    'u': 'U3',
    'cx': 'CNOT',
    'cz': 'CZ',
    'cy': 'CY',
    'swap': 'SWAP',
    'iswap': 'ISWAP',
  }
  c_based = ['CNOT', 'CZ', 'CY', 'SWAP', 'ISWAP']
  pennyPass = {
    'name': 'pnl',
    'params': [],
  }

  evals = []

  for _, layer in enumerate(circuit):
    for wireNo, gate in enumerate(layer):
      if no_gate.match(gate):
        continue
      gate = gate.lower()
      if '(' in gate and ')' in gate:
        gate_name = gate[: gate.index('(')]
        op = gate_map[gate_name]
        param = gate[gate.index('(') + 1 : gate.index(')')]

        if ',' in param:
          if gate_name in c_based:
            param = list(map(parse_param, param.split(',')))
            # remove 1st element and use it as wireNo2
            wireNo2 = param.pop(0)
            param = param + [wireNo, wireNo2]
          else:
            param = list(map(parse_param, param.split(',')))
            param = param + [wireNo]
        else:
          param = [parse_param(param, pennyPass), wireNo]
      else:
        param = [wireNo]
        op = gate_map[gate]

      # if gate is a c* type gate then we pass
      # qubits as wires=[wireNo, wireNo2]
      progam = {
        'op': op,
      }
      if op in c_based:
        # pop last 2
        wires = param[-2:]
        param = param[:-2]
        progam['wires'] = wires
        progam['param'] = param
      else:
        progam['wires'] = [param[-1]]
        progam['param'] = param[:-1]

      evals.append(progam)

  def genCirc(qml, params):
    for i in range(len(evals)):
      exec = evals[i]
      if len(exec['param']) > 0:
        if (
          isinstance(exec['param'][0], tuple)
          and exec['param'][0][0] == 'VAR'
        ):
          index = exec['param'][0][1] - 1
          exec['param'][0] = params[index]

        op = getattr(qml, exec['op'])
        op(*exec['param'], wires=exec['wires'])
      else:
        op = getattr(qml, exec['op'])
        op(wires=exec['wires'])

  param_ct = len(pennyPass['params'])
  return genCirc, [0] * param_ct


def toQiskit(qc, stri):
  circuit = parse_circuit(stri)
  return resolve_qiskit(circuit, qc)


def toCudaq(cudaO, stri):
  circuit = parse_circuit(stri)
  return resolve_cudaq(circuit, cudaO)


def toPennylane(stri):
  circuit = parse_circuit(stri)
  return resolve_pennylane(circuit)

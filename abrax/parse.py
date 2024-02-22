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


def resolve_qiskit(circuit, qc, config):
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

  if config['measure']:
    qc.measure_all()
  return qc


# TODO: POLYFILL GATES
# ibm_valid_gates = ['u']
# u(a,b,c) = rz(b)ry(a)rz(c)
# cudaO = [kernel, qubits, params]
# params = float | int | float[] | int[]
"""
Cudaq Format
kernel.gate(param?..., qubits[qubitno1], qubits[qubitno2]?...)
"""


def resolve_cudaq(circuit, cudaO, config):
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


default = {
  'measure': True,
}


def toQiskit(qc, stri, config=default):
  circuit = parse_circuit(stri)
  return resolve_qiskit(circuit, qc, config)


def toCudaq(cudaO, stri, config=default):
  circuit = parse_circuit(stri)
  return resolve_cudaq(circuit, cudaO, config)

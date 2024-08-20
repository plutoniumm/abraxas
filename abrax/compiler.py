from re import compile, findall
import numpy as np

vargex = compile("var_\w*")

def autoParam(int):
  rand = np.round(np.random.rand(), 6)
  rand = [rand+(i/1e5) for i in range(int)]
  rand = np.round(rand, 7)
  return rand

def parseVars(string):
  variables = []

  # string will contain var_0, var_1, etc.
  for line in string.split("\n"):
    if "var_" in line:
      matches = findall(vargex, line)
      variables.extend(matches)
    # endif
  # endfor
  variables = list(set(variables))
  params = list(autoParam(len(variables)))

  for i, var in enumerate(variables):
    string = string.replace(var, str(params[i]))

  variables = [i.replace('var_', '') for i in variables]
  return string, variables, params


def toQiskit(string):
  from qiskit.circuit import QuantumCircuit, Parameter
  from qiskit.transpiler import TransformationPass
  from qiskit.converters import circuit_to_dag

  string, variables, params = parseVars(string)
  variables = [Parameter(p) for p in variables]

  qc = QuantumCircuit.from_qasm_str(string)
  class BackReplace(TransformationPass):
    def run(self, dag):
      for node in dag.op_nodes():
        cparams = node.op.params
        if len(cparams) == 0:
          continue
        replacement = QuantumCircuit(node.op.num_qubits)
        op = node.op.copy()
        new_params = []
        for p in cparams:
          if p in params:
            idx = params.index(p)
            new_params.append(variables[idx])
          else:
            new_params.append(p)

        op.params = new_params
        replacement.append(op, list(range(node.op.num_qubits)))

        dag.substitute_node_with_dag(node, circuit_to_dag(replacement))
      return dag

  transpiled = BackReplace()(qc)
  return transpiled

def toPenny(string, device):
  from pennylane import qml
  from pennylane.tape import make_qscript

  string, variables, params = parseVars(string)
  qc = qml.from_qasm(string)
  ops = list(make_qscript(qc)())
  new_ops = []
  for op in ops:
    if op.num_params > 0:
      new_params = []
      for p in op.parameters:
        if p in params:
          idx = params.index(p)
          p = variables[idx]
        # endif
        new_params.append(p)
      # endfor
      op.data = tuple(
        np.array(p)
          if isinstance(p, (list, tuple))
          else p for p in new_params
      )
    # endif
    new_ops.append(op)
  # endfor

  def circuit():
    for op in new_ops:
      qml.apply(op)
    return qml.state()

  circuit=qml.QNode(circuit, device)
  return circuit

def unstring(pars):
  pars = [i.replace('/pi', '') for i in pars]
  pars = [i[1:-1] if i[0] == '(' else i for i in pars]
  pars = [float(i) for i in pars]
  return pars

# use Circuit.to_dict | Circuit.from_dict for debugging
def toTket(string):
  from pytket.qasm.qasm import parser, CircuitTransformer as CT
  from pytket import Circuit

  string, variables, params = parseVars(string)
  jsond = parser(maxwidth=32).parse(string)

  for cmd in jsond['commands']:
    if 'params' not in cmd['op']:
      continue # no parameters
    cpars = unstring(cmd['op']['params'])
    new_params = []
    for p in cpars:
      if p in params:
        p = variables[params.index(p)]
      new_params.append(p)
    # endfor
    cmd['op']['params'] = new_params
  # endfor

  qc = Circuit.from_dict(jsond)
  return qc

def toCirq(string):
  from cirq.contrib.qasm_import import circuit_from_qasm
  from sympy import Symbol
  import cirq as c
  string, variables, params = parseVars(string)

  def map_func(op, _):
    if hasattr(op.gate, 'exponent'):
      expo = op.gate.exponent
      if expo in params:
        idx = params.index(expo)
        idx = Symbol(str(variables[idx]))

        gate = getattr(c, op.gate.__class__.__name__)
        op = gate(rads=idx).on(*op.qubits)
      # endif
    yield op

  params = [i/np.pi for i in params]
  qc = circuit_from_qasm(string)
  qc2 = c.map_operations(qc, map_func)

  return qc2

def toCudaq(string):
  from qiskit.transpiler.passes import RemoveBarriers
  from qiskit.circuit import Parameter
  from qiskit import QuantumCircuit
  from cudaq import make_kernel

  string, variables, params = parseVars(string)
  variables = [Parameter(p) for p in variables]

  qc = QuantumCircuit.from_qasm_str(string)
  qc = RemoveBarriers()(qc)

  if len(params) > 0:
    kernel, thetas = make_kernel(list)
  else:
      kernel = make_kernel()
      thetas = []
  cuq = kernel.qalloc(len(qc.qubits))

  def u(self, a, b, c, u):
    kernel.rz(b, u)
    kernel.ry(a, u)
    kernel.rz(c, u)

  kernel.u = u
  kernel.p = kernel.r1
  gate_map = {
    "phase": "p", "swap": "swap","measure": "mz"
  }
  legal_gates = [
    'x', 'y', 'z', 'phase',
    'rx', 'ry', 'rz', 'cx', 'cz', 'cy',
    'u', 's', 't', 'h', 'swap', 'measure'
  ]
  # just loop over the gates and apply them

  for instr, qubits, _ in qc.data:
    if instr.name not in legal_gates:
      raise ValueError(f"Gate {instr.name} not supported")
    name = instr.name
    arguments = instr.params
    if name in gate_map:
      name = gate_map[name]

    op = getattr(kernel, name)
    qubits = [q._index for q in qubits]
    qubits = [cuq[q] for q in qubits]
    if len(arguments) > 0:
      # arguments need to be mapped to thetas if theyre in params
      new_args = []
      for arg in arguments:
        if arg in params:
          idx = params.index(arg)
          arg = thetas[idx]
        new_args.append(arg)

      arguments = new_args
      op(*new_args, *qubits)
    else:
      op(*qubits)

  return kernel, qubits, thetas

def toPyquil(string):
  from qiskit.transpiler.passes import RemoveBarriers
  from qiskit.circuit import QuantumCircuit
  from pyquil import Program
  import pyquil.gates as G

  string, variables, params = parseVars(string)
  qc = QuantumCircuit.from_qasm_str(string)
  qc = RemoveBarriers()(qc)

  # same as cudaq we need to manually generate the program
  legal_gates = [
    'I', 'X', 'Y', 'Z', 'H', 'PHASE', 'S', 'T',
    'CZ', 'RX', 'RY', 'RZ', 'CX', 'CCX',
    'SWAP', 'CSWAP', 'ISWAP', 'PSWAP',
  ]
  gate_map = {
    "CX": "CNOT", "CCX": "CCNOT"
  }

  # variables are declared as
  # theta1 = p.declare("theta1", "REAL")

  p = Program()
  for instr, qubits, _ in qc.data:
    name = instr.name.upper()
    if name not in legal_gates:
      raise ValueError(f"Gate {name} not supported")
    arguments = instr.params
    if name in gate_map:
      name = gate_map[name]

    op = getattr(G, name)
    qubits = [q._index for q in qubits]
    if len(arguments) > 0:
      new_args = []
      for arg in arguments:
        if arg in params:
          idx = params.index(arg)
          arg = variables[idx]
          arg = p.declare(str(arg), "REAL")
        new_args.append(arg)

      arguments = new_args
      p += op(*new_args, *qubits)
    else:
      p += op(*qubits)

  return p

def toBraket(string):
  from qiskit_braket_provider.providers.adapter import to_braket
  qc = toQiskit(string)

  return to_braket(qc)

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
        replacement = QuantumCircuit(len(cparams))
        op = node.op.copy()
        new_params = []
        for p in cparams:
          if p in params:
            idx = params.index(p)
            new_params.append(variables[idx])
          else:
            new_params.append(p)

        op.params = new_params
        replacement.append(op, [0])

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
      old_params = op.parameters
      new_params = []
      for p in op.parameters:
        if p in params:
          idx = params.index(p)
          new_params.append(variables[idx])
        else:
          new_params.append(p)
      print(old_params, new_params)
      # new_params = []
      # for p in op.parameters:
      #   if p in params:
      #     idx = params.index(p)
      #     new_params.append(variables[idx])
      #   else:
      #     new_params.append(p)
      # op.parameters = new_params
    # new_ops.append(op)

  return qc

def toTket(string):
  from pytket.qasm import circuit_from_qasm_str
  string, variables = parseVars(string)
  qc = circuit_from_qasm_str(string)

  return qc

def toCirq(string):
  from cirq.contrib.qasm_import import circuit_from_qasm
  from cirq import map_operations
  import cirq as cirq
  from sympy import Symbol
  string, variables, params = parseVars(string)

  def map_func(op, _):
    if hasattr(op.gate, 'exponent'):
      expo = op.gate.exponent
      if expo in params:
        idx = params.index(expo)
        idx = Symbol(str(variables[idx]))

        gate = getattr(cirq, op.gate.__class__.__name__)
        op = gate(rads=idx).on(*op.qubits)
        print(op)
        yield op
      else:
        yield op
    else:
      yield op

  params = [i/np.pi for i in params]
  # print(string, variables, params)

  qc = circuit_from_qasm(string)
  qc2 = map_operations(qc, map_func)

  return qc2
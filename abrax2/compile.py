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
  from qiskit.converters import circuit_to_dag
  from qiskit.transpiler import TransformationPass

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
  string, variables = parseVars(string)
  from pennylane import qml
  qc = qml.from_qasm(string)
  qc = qml.QNode(qc, device)

  return qc

def toTket(string):
  string, variables = parseVars(string)
  from pytket.qasm import circuit_from_qasm_str
  qc = circuit_from_qasm_str(string)

  return qc

def toCirq(string):
  string, variables, params = parseVars(string)
  print(string, variables, params)
  from cirq.contrib.qasm_import import circuit_from_qasm
  qc = circuit_from_qasm(string)

  print(qc)

  return qc
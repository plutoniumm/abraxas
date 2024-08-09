def toQiskit(string):
  from qiskit import QuantumCircuit
  qc = QuantumCircuit.from_qasm_str(string)

  return qc

def toPenny(string, device):
  from pennylane import qml
  qc = qml.from_qasm(string)
  qc = qml.QNode(qc, device)

  return qc

def toTket(string):
  from pytket.qasm import circuit_from_qasm_str
  qc = circuit_from_qasm_str(string)

  return qc

def toCirq(string):
  from cirq.contrib.qasm_import import circuit_from_qasm
  qc = circuit_from_qasm(string)

  return qc
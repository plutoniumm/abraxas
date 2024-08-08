from pytket.circuit import Circuit
import pennylane as qml
import qiskit as qk
from compiler import toPrime

dev = qml.device("default.qubit", wires=2)
@qml.qnode(dev)
def circuit(angles):
  qml.Hadamard(wires=1)
  qml.CNOT(wires=[0, 1])
  qml.RY(angles[0], wires=0)
  qml.RY(angles[1], wires=1)

  return qml.state()

def bell_ibm(theta):
  qc = qk.QuantumCircuit(2)
  qc.h(0)
  qc.cx(0, 1)
  qc.ry(theta, 0)
  qc.ry(theta, 1)

  return qc

def bell_quan(theta):
  circ = Circuit(2)
  circ.H(0)
  circ.CX(0, 1)
  circ.Ry(theta, 0)
  circ.Ry(theta, 1)

  return circ

# res = toPrime(circuit)
# print(res)
# res2 = toPrime(bell_ibm(.1))
# print(res2)
# res3 = toPrime(bell_quan(.1))
# print(res3)
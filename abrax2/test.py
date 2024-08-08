from pytket.circuit import Circuit
import pennylane as qml
import qiskit as qk
import cirq as cirq
from parser import toPrime

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

def bell_cirq(theta):

  circ = cirq.Circuit()
  q0, q1 = cirq.LineQubit.range(2)
  circ.append(cirq.H(q0))
  circ.append(cirq.CNOT(q0, q1))
  circ.append(cirq.ry(theta)(q0))
  circ.append(cirq.ry(theta)(q1))

  return circ

QASM="""
OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];


h q[0];
cx q[0],q[1];
ry(pi*0.0318309886) q[0];
ry(pi*0.0318309886) q[1];
""".strip()

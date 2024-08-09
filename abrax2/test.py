from pytket.circuit import Circuit
import pennylane as qml
import qiskit as qk
import cirq as cirq
from sympy import Symbol
from parser import toPrime, autoParam
from compile import toCirq, toQiskit, toTket, toPenny

dev = qml.device("default.qubit", wires=2)
PARSE = True

if PARSE:
  @qml.qnode(dev)
  def bell_penny(angles):

    qml.Hadamard(wires=1)
    qml.CNOT(wires=[0, 1])
    qml.RY(angles[0], wires=0)
    qml.RY(angles[1], wires=1)
    qml.RY(angles[2], wires=1)
    qml.RY(angles[3], wires=0)

    return qml.state()

  def bell_ibm():
    from qiskit.circuit import Parameter, QuantumCircuit
    a,b = Parameter('a'), Parameter('b')
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.ry(a, 0)
    qc.ry(b, 1)

    return qc

  def bell_quan():
    theta1, theta2 = Symbol('theta1'), Symbol('theta2')
    circ = Circuit(2)
    circ.H(0)
    circ.CX(0, 1)
    circ.Ry(theta1, 0)
    circ.Ry(theta2, 1)

    return circ

  def bell_cirq():
    from sympy import Symbol
    theta1, theta2 = Symbol('theta1'), Symbol('theta2')

    circ = cirq.Circuit()
    q0, q1 = cirq.LineQubit.range(2)
    circ.append(cirq.H(q0))
    circ.append(cirq.CNOT(q0, q1))
    circ.append(cirq.ry(theta1)(q0))
    circ.append(cirq.ry(theta2)(q1))

    return circ

  # res = toPrime(bell_penny, params=autoParam(4))
  # print(res)
  print(toPrime(bell_quan()))
  # print(toPrime(bell_ibm()))
  # print(toPrime(bell_cirq()))


QASM="""
OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];


h q[0];
cx q[0],q[1];
ry(pi*0.0318309886) q[0];
ry(pi*0.0318309886) q[1];
""".strip()

# qc = toQiskit(QASM)
# qc2 = toPenny(QASM, dev)
# qc3 = toCirq(QASM)
# qc4 = toTket(QASM)
# print("toQiskit: \n", qc)
# print("toPenny: \n", qml.draw(qc2)())
# print("toCirq: \n", qc3)
# print("toTket: \n", qc4)
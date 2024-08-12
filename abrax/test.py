from pytket.circuit import Circuit
from pyquil import Program
import pyquil.gates as G
from sympy import Symbol
import pennylane as qml
import cirq as cirq
import qiskit as qk

from compiler import toCirq, toQiskit, toTket, toPenny, toCudaq, toQuil
from parser import toQasm

dev = qml.device("default.qubit", wires=2)
PARSE = False

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
    qc.measure_all()

    return qc

  def bell_quan():
    theta1, theta2 = Symbol('theta1'), Symbol('theta2')
    circ = Circuit(2)
    circ.H(0)
    circ.CX(0, 1)
    circ.Ry(theta1, 0)
    circ.Ry(theta2, 1)

    return circ

  def bell_quil():
    p = Program()
    ro = p.declare("ro", "BIT", 2)
    theta1 = p.declare("theta1", "REAL")
    theta2 = p.declare("theta2", "REAL")

    p += G.H(0)
    p += G.CNOT(0, 1)
    p += G.RY(theta1, 0)
    p += G.RY(theta2, 1)
    p += G.MEASURE(0, ro[0])
    p += G.MEASURE(1, ro[1])

    return p

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

  def bell_cudaq():
    kernel = make_kernel()
    q = kernel.qalloc(q)

    kernel.h(q[0])
    kernel.cx(q[0], q[1])
    kernel.rx(0.1*0, q[0])
    kernel.rx(0.1*1, q[1])

    kernel.mz(q[0])
    kernel.mz(q[1])

    return kernel
  # print(toQasm(bell_penny))
  # print(toQasm(bell_quan()))
  # print(toQasm(bell_ibm()))
  # print(toQasm(bell_cirq()))
  # print(toQasm(bell_quil()))
  # print(toQasm(bell_cudaq()))


QASM="""
OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];


h q[0];
cx q[0],q[1];
ry(var_theta1) q[0];
ry(var_theta2) q[1];
""".strip()

# print(toQiskit(QASM))
# print(toPenny(QASM, dev))
# print(toCirq(QASM))
# print(toTket(QASM))
# print(toCudaq(QASM))
# print(toQuil(QASM))
import pyquil.latex
res = pyquil.latex.to_latex(toQuil(QASM))
print(res)
from sympy import Symbol
import cirq as cirq

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

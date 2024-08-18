from pytket.circuit import Circuit
from sympy import Symbol

def bell_quan():
  theta1, theta2 = Symbol('theta1'), Symbol('theta2')
  circ = Circuit(2)
  circ.H(0)
  circ.CX(0, 1)
  circ.Ry(theta1, 0)
  circ.Ry(theta2, 1)

  return circ

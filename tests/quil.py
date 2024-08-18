from pyquil import Program
import pyquil.gates as G

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

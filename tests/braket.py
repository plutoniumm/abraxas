from braket.circuits import Circuit as Bracket, FreeParameter

def bell_bracket():
  circuit = Bracket()
  circuit.h(0)
  circuit.cnot(0, 1)
  circuit.ry(0, FreeParameter('theta1'))
  circuit.ry(1, FreeParameter('theta2'))

  return circuit
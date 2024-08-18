import pennylane as qml
dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev)
def bell_penny(angles):

  qml.Hadamard(wires=1)
  qml.CNOT(wires=[0, 1])
  qml.RY(angles[0], wires=0)
  qml.RY(angles[1], wires=1)
  qml.RY(angles[2], wires=1)
  qml.RY(angles[3], wires=0)

  return qml.state()
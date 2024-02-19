from qiskit import QuantumCircuit
from .. import A
from numpy import pi

qc = QuantumCircuit(5)
circuit = A(qc, f"""
  // I AM JESUS
  // SPACES ARE SIGNIFICANT, DONOT add them inside a gate
  - H CX(4)  RX({pi})
  - H RZ(45) RY({5.5})
  - H ---    CX(4)
  - H X      H
  - H ---    -------
  """
)

print(circuit)
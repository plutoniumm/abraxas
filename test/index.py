from qiskit import QuantumCircuit
from abrax import A

qc = QuantumCircuit(5)
circuit = A("""
  // I AM JESUS
  // SPACES ARE SIGNIFICANT, DONOT add them inside a gate
  - H CX(4) RX(10)
  - H -    RY(55)
  - H -    CX(4)
  - H X    H
  - H -    -
  """, qc
)

print(circuit)
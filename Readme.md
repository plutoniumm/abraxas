## abraxas

A tiny DSL to compile to qiskit circuits. The goal is to speed up the time it takes to write small stupid circuits. Anything beyond a certain complexity should be written in qiskit directly.

### Example

```python
from abrax import A

# Create a circuit
circuit = A("""
- H CX(4) RX(10)
- H -    -
- H -    CX(4)
- H X    RY(55)
- H -    -
""")

# Should be equivalent to
from qiskit import QuantumCircuit

qc = QuantumCircuit(5)
qc.h([0, 1, 2, 3, 4])
qc.cx(0, 4)
qc.x(3)
qc.rx(10, 0)
qc.cx(2, 4)
qc.ry(55, 3)
qc.measure_all()
```
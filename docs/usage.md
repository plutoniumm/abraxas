## Usage
### toPennylane
```python
from qiskit import QuantumCircuit, Parameter
from abrax import toPenny, toQasm
import pennylane as qml

qc = QuantumCircuit(3)
p = Parameter('x')
qc.h([0, 1, 2])
qc.cx(0, 2)
qc.rx(0, 0)
qc.cx(1, 2)
qc.ry(p, 2)

qasm = toQasm(qc)
dev = qml.device("default.qubit", wires=2)
circuit = toPenny(qasm, dev) # pennylane needs 'dev'
# print(qml.draw(circuit)())
# 0: ──H─╭X──RX(0.00)───────────────┤  Probs
# 1: ──H─│────────────╭X────────────┤  Probs
# 2: ──H─╰●──X────────╰●──RY(x)─────┤  Probs
```

### Others
See [`test.py`](https://github.com/plutoniumm/abraxas/blob/main/abrax/test.py) for more examples.

Supported exports:
- `toQasm`
- `toPenny`, `toQiskit`, `toCirq`, `toBraket`, `toQiskit`, `toCudaQ`, `toQuil`
## Draw
Draw function is universal and can be used with any quantum circuit library. It will draw the circuit in the console as returned by said library's `draw` function.

We assume that all necessary dependencies are installed for whatever library you are using.

```py
from abrax import draw
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

draw(qc)

# OR
import pennylane as qml
dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev)
def circuit():
  qc = QuantumCircuit(2)
  qc.h(0)
  qc.cx(0, 1)
  return qc

draw(qc)
```
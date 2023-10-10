## abraxas

<img src="./test/icon.svg" width="100" height="100" align="right" />

A tiny DSL to compile to qiskit circuits. The goal is to speed up the time it takes to write small stupid circuits. Anything beyond a certain complexity should be written in qiskit directly.

[Qiskit](https://qiskit.org/) &bullet; [Abraxas](https://foundation.fandom.com/wiki/Abraxas_Conjecture) &bullet; [Issues](https://github.com/plutoniumm/abraxas/issues) &bullet; [Latest](https://github.com/plutoniumm/abraxas/releases/latest)

### Install
While not specified here you will need Qiskit since Abraxas takes in an initialized `QuantumCircuit` object to write to.
```py
pip install abrax
```

### Examples
#### Fairly Complex
```python
from abrax import A
from qiskit import QuantumCircuit

qc = QuantumCircuit(5)
qc = A("""
  - H CX(4) RX(10)
  - H -    -
  - H -    CX(4)
  - H X    RY(55)
  - H -    -
  """, qc
)

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

### Simple
```python
from abrax import A
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
# This will apply H, H to 0-qubit & 1-qubit
# Then a CX on 0-qubit (as target) with 1-qubit as control
qc = A("""
  - H CX(1)
  - H -
  """, qc
)
```

### Syntax
- Note All lines must start with a `-` or `|>` (continuation operator `NotImplemented` yet)
- Everything else is a comment
- Case insensitive

**Passing Config**
```python
qc = A("""
- H CX(1)
- H -
""", qc,
config={
  "measure": False,
})
```

| Key | Type (Default) | Description |
| --- | --- | --- |
| `measure` | `bool` (`True`) | Whether to measure all qubits at the end of the circuit |

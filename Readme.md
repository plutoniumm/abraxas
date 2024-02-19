## abraxas

<img src="./test/icon.svg" width="100" height="100" align="right" />

A tiny DSL to compile to qiskit circuits. The goal is to speed up the time it takes to write small stupid circuits. Anything beyond a certain complexity should be written in qiskit directly.

[Qiskit](https://qiskit.org/) &bullet; [Abraxas](https://foundation.fandom.com/wiki/Abraxas_Conjecture) &bullet; [Issues](https://github.com/plutoniumm/abraxas/issues) &bullet; [Latest](https://github.com/plutoniumm/abraxas/releases/latest)

> A breaking change may come soon where I change measure: True and just not do it, seems like a cleaner way to do it and will enable more things. Unless I can come up with a better way to implement Measurements

### Install
You will need Qiskit since Abraxas takes in an initialized `QuantumCircuit` object to write to.
```py
pip install abrax
```

### Features
- [x] Basic gates
- [x] Value interpolation (just pass in $\pi$ if needed)
- [x] Comments
- [x] Optional measurement
- [x] Append to existing circuit
- [x] Feel free to add multiple `--` or more spaces for formatting

### Examples
#### Fairly Complex
```python
from qiskit import QuantumCircuit
from numpy import pi
from abrax import A

qc = QuantumCircuit(5)
qc = A(qc, f"""
  - H CX(4) RX({pi/4})
  - H -     -
  - H -     CX(4)
  - H X     RY(55)
  - H -     -
  """
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

# This will apply H, H to 0-qubit & 1-qubit
# Then a CX on 0-qubit (as target) with 1-qubit as control
qc = A(QuantumCircuit(2), """
  - H CX(1)
  - H -
  """
)
```

### Append
Abraxas can also add to an existing circuit since it takes in your circuit and simply appends to it

```python
from abrax import A
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h([0,1])
qc = A(qc, """
  - RX(2) CX(1)
  - RX(3) -
  """
)

# Should be equivalent to
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h([0,1])
qc.rx(2, 0)
qc.cx(1, 0)
qc.rx(3, 1)
```

### Syntax
- Note All lines must start with a `-` or `|>` (continuation operator `NotImplemented` yet)
- Everything else is a comment
- Case insensitive

**Passing Config**
```python
qc = A(qc, """
- H CX(1)
- H -
""",
config={
  "measure": False,
})
```

| Key | Type (Default) | Description |
| --- | --- | --- |
| `measure` | `bool` (`True`) | Whether to measure all qubits at the end of the circuit |
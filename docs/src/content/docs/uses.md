---
title: Common Uses
description: Common uses of abraxas
---

# Common Uses
## To store the data
Once a circuit is converted to string we can store it for posterity. This is useful for sharing the circuit with others or for future use.

```python
def ESU2():
  from qiskit.circuit.library import EfficientSU2

  qc = EfficientSU2(5, reps=2)
  for i in range(5):
    qc.h(i)
  qc = qc.decompose()

  return toPrime(qc)

string = toPrime(ESU2())

"""
-0 ry(θ[0]) rz(θ[5]) cx(1)     ry(θ[10]) rz(θ[15]) cx(1)     ry(θ[20])
-1 ry(θ[1]) rz(θ[6]) cx(2)     ry(θ[11]) rz(θ[16]) cx(2)     ry(θ[21])
-2 ry(θ[2]) rz(θ[7]) cx(3)     ry(θ[12]) rz(θ[17]) cx(3)     ry(θ[22])
-3 ry(θ[3]) rz(θ[8])  ---      ry(θ[13]) rz(θ[18])  ---      ry(θ[23])
-4 ry(θ[4]) rz(θ[9]) ry(θ[14]) rz(θ[19]) ry(θ[24]) rz(θ[29]) u(1.5708,0,3.1416)
"""
```

## Convert to different Framework
Pass this circuit to pennylane or qiskit as shown in [Parse](/parse)
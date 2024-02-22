from parse import toQiskit, toCudaq
from compiler import toString


def ESU2():
  from qiskit.circuit.library import EfficientSU2

  qc = EfficientSU2(5, reps=2)
  for i in range(5):
    qc.h(i)
  qc = qc.decompose()

  return toString(qc)


SU2 = """
-0 ry(θ[0]) rz(θ[5]) cx(1)     ry(θ[10]) rz(θ[15]) cx(1)     ry(θ[20])
-1 ry(θ[1]) rz(θ[6]) cx(2)     ry(θ[11]) rz(θ[16]) cx(2)     ry(θ[21])
-2 ry(θ[2]) rz(θ[7]) cx(3)     ry(θ[12]) rz(θ[17]) cx(3)     ry(θ[22])
-3 ry(θ[3]) rz(θ[8]) cx(4)     ry(θ[13]) rz(θ[18]) cx(4)     ry(θ[23])
-4 ry(θ[4]) rz(θ[9]) ry(θ[14]) rz(θ[19]) ry(θ[24]) rz(θ[29]) u(1.5708,0,3.1416)
"""


if __name__ == '__main__':
  from qiskit import QuantumCircuit

  qisO = QuantumCircuit(5)
  qis = toQiskit(qisO, SU2)
  print(qis)

  from cudaq import make_kernel, sample

  kernel, thetas = make_kernel(list)
  qubits = kernel.qalloc(5)

  cudaO = {
    'kernel': kernel,
    'qubits': qubits,
    'quake': thetas,
    'params': 0,
  }
  cuq = toCudaq(cudaO, SU2)
  vals = [0.1 * i for i in range(cudaO['params'])]
  result = sample(kernel, vals)
  print(result)

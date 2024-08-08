from abrax import toQiskit, toCudaq, toPennylane
from utils import whatall, what
from abrax import toPrime

def ESU2():
  from qiskit.circuit.library import EfficientSU2

  qc = EfficientSU2(5, reps=2)
  for i in range(5):
    qc.h(i)
  qc = qc.decompose()

  return toPrime(qc)


SU2 = """
-0 ry(θ[0]) rz(θ[5]) cx(1)     ry(θ[10]) rz(θ[15]) cx(1)     ry(θ[20])
-1 ry(θ[1]) rz(θ[6]) cx(2)     ry(θ[11]) rz(θ[16]) cx(2)     ry(θ[21])
-2 ry(θ[2]) rz(θ[7]) cx(3)     ry(θ[12]) rz(θ[17]) cx(3)     ry(θ[22])
-3 ry(θ[3]) rz(θ[8])  ---      ry(θ[13]) rz(θ[18])  ---      ry(θ[23])
-4 ry(θ[4]) rz(θ[9]) ry(θ[14]) rz(θ[19]) ry(θ[24]) rz(θ[29]) u(1.5708,0,3.1416)
"""
# SU2 = """
# -0 h ry(0.3) cx(1)
# -1 h ry(0.3) ---- sx
# """


def pnlTest():
  import pennylane as qml

  dev = qml.device('default.qubit', wires=[0, 1, 2])

  @qml.qnode(dev)
  def circuit(x):
    # qml.RX(x[0], wires=0)
    qml.Toffoli(wires=(0, 1, 2))
    # qml.CRY(x[1], wires=(0, 1))
    # qml.Rot(x[2], x[3], x[0], wires=0)
    return qml.expval(qml.PauliZ(0))

  circuit([0.1, 0.2, 0.3, 0.4])
  stringed = toPrime(circuit)
  print(stringed)

  from qiskit import QuantumCircuit

  qc = QuantumCircuit(3)
  qiskit = toQiskit(qc, stringed)
  print(qiskit)


def qis2pnl(CIRC):
  QS = len(CIRC.strip().split('\n'))
  from qiskit import QuantumCircuit

  qisO = QuantumCircuit(QS)
  qis = toQiskit(qisO, CIRC)
  print(qis)

  """PENNYLANE"""
  import pennylane as qml

  dev = qml.device('default.qubit', wires=QS)

  def genCirc():
    generator, params = toPennylane(CIRC)
    params = [0.1 * i for i in range(len(params))]
    generator(qml, params)

    return qml.probs()

  circuit = qml.QNode(genCirc, dev)
  print(qml.draw(circuit)())


def qis2cuq(CIRC):
  QS = len(CIRC.strip().split('\n'))

  from qiskit import QuantumCircuit

  qisO = QuantumCircuit(QS)
  qis = toQiskit(qisO, CIRC)
  print(qis)

  """CUDAQ"""
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

"""# MAIN"""
import pennylane as qml

dev = qml.device("default.qubit", wires=3)

@qml.qnode(dev)
def circuit(angles):
  print(angles)
  qml.Hadamard(wires=1)
  qml.Hadamard(wires=2)
  qml.RX(angles[0], 0)
  qml.CNOT(wires=[1, 0])
  qml.CNOT(wires=[2, 1])
  qml.RX(angles[2], wires=0)
  qml.RZ(angles[1], wires=2)
  qml.CNOT(wires=[2, 1])
  qml.RZ(-angles[1], wires=2)
  qml.CNOT(wires=[1, 0])
  qml.Hadamard(wires=1)
  qml.CY(wires=[1, 2])
  qml.CNOT(wires=[1, 0])

  return qml.state()

circuit.construct([[0.1, 0.3, 0.5]], {})
t = circuit.qtape.to_openqasm()
print(t)
# qasm = tape.to_openqasm()
# print(qasm)

# qis2pnl(SU2)
# pnlTest()

import qiskit as qk

def bell_ibm():
  from qiskit.circuit import Parameter, QuantumCircuit
  a,b = Parameter('a'), Parameter('b')
  qc = QuantumCircuit(2)
  qc.h(0)
  qc.cx(0, 1)
  qc.ry(a, 0)
  qc.ry(b, 1)
  qc.measure_all()

  return qc

def h2_vqe():
  from qiskit.circuit.library import ExcitationPreserving
  from qiskit.circuit import Parameter, QuantumCircuit

  qc = QuantumCircuit(4)
  qc.x([0, 2])
  ep = ExcitationPreserving(4, 'iswap', 'linear', 2)
  qc.compose(ep, inplace=True)
  qc = qc.decompose()

  return qc
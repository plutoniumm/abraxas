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
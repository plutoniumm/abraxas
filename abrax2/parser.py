from qiskit.qasm2 import dumps
import numpy as np

class Unlist(list):
  def __init__(self):
    self.append(0)
    self.__class__.__module__ = "builtins"

  def __getitem__(self, index):
    while index >= len(self):
      self.append(index)
    return super(Unlist, self).__getitem__(index)

def compile_penny(qc, params):
  qc.construct([params], {})
  t = qc.qtape.to_openqasm().strip()

  return t

def compile_qiskit(qc, params):
  qc = qc.assign_parameters(params)
  t = dumps(qc).strip()

  return t

def compile_tket(qc, params):
  from pytket.extensions.qiskit import tk_to_qiskit
  params = params / np.pi
  qc.symbol_substitution(
    dict(zip(qc.free_symbols(), params))
  )
  t = tk_to_qiskit(qc)
  t = dumps(t).strip()

  return t

def compile_cirq(qc, params):
  from cirq import qasm, resolve_parameters,ParamResolver
  names = list(qc._parameter_names_())
  params = params * np.pi
  qc = resolve_parameters(
    qc, ParamResolver(dict(zip(names, params)))
  )
  t = qasm(qc).strip()

  return t


def autoParam(int):
  rand = np.round(np.random.rand(), 6)
  rand = [rand+(i/1e5) for i in range(int)]
  rand = np.round(rand, 7)
  return rand

def toQasm(qc):
  name = qc.__class__.__name__
  base = qc.__class__.__base__.__name__
  params = [0]
  qasmd = None

  if name == 'QuantumCircuit':
    name = "Qiskit"
    names = [i.name for i in qc.parameters]
    params = autoParam(len(names))
    qasmd = compile_qiskit(qc, params=params)

  elif name == 'QNode':
    name = "PennyLane"
    qc2 = qc
    names = Unlist()
    qc2(names)
    names = [str(i) for i in names]
    params = autoParam(len(names))
    qasmd = compile_penny(qc2, params=params)

  elif base == 'pybind11_object':
    name = "TKet"
    names = []
    for p in qc:
      names.extend(p.free_symbols())
    names = list(set(names))
    params = autoParam(len(names))
    qasmd = compile_tket(qc, params=params)

  elif name == 'Circuit':
    name = "Cirq"
    names = list(qc._parameter_names_())
    params = autoParam(len(names))
    qasmd = compile_cirq(qc, params=params)
  else:
    raise ValueError(f'Unsupported circuit: {name}')

  # replace all params back with var_i
  for i in range(len(params)):
    qasmd = qasmd.replace(str(params[i]), f'var_{names[i]}')

  return qasmd
from typing import Dict, Union, Callable, List
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
  params = params / np.pi
  qc.symbol_substitution(
    dict(zip(qc.free_symbols(), params))
  )
  from pytket.extensions.qiskit import tk_to_qiskit
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

def toPrime(qc):
  name = qc.__class__.__name__
  base = qc.__class__.__base__.__name__
  params = [0]
  converted = None

  if name == 'QuantumCircuit':
    # QISKIT
    params = autoParam(len(qc.parameters))
    converted = compile_qiskit(qc, params=params)
  elif name == 'QNode':
    # PENNYLANE
    qc2 = qc
    x0 = Unlist()
    qc2(x0)
    params = autoParam(len(x0))
    converted = compile_penny(qc2, params=params)
  elif base == 'pybind11_object':
    # TKET
    variables = []
    for p in qc:
      variables.extend(p.free_symbols())
    variables = list(set(variables))
    params = autoParam(len(variables))
    converted = compile_tket(qc, params=params)
  elif name == 'Circuit':
    # CIRQ
    params = autoParam(len(list(qc._parameter_names_())))
    converted = compile_cirq(qc, params=params)
  else:
    raise ValueError(f'Unsupported circuit: {name}')

  # replace all params back with var_i
  for i in range(len(params)):
    converted = converted.replace(str(params[i]), f'var_{i}')

  return converted
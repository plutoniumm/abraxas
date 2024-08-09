from _utils_compile import matrix_to_str, valid_gates
from typing import Dict, Union, Callable, List
from qiskit.qasm2 import dumps
import numpy as np

def what(o):
  params =  [i for i in dir(o) if not i.startswith('_')]
  params.sort()
  return params

def whatnot(o):
  params = [i for i in dir(o) if (i.startswith('_') and not i.startswith('__'))]
  params.sort()
  return params

def compile_penny(qc, params):
  qc2 = qc
  qc2.construct([params], {})
  t = qc2.qtape.to_openqasm().strip()

  return t

def compile_qiskit(qc, params):
  qc = qc.assign_parameters(params)
  t = dumps(qc).strip()

  return t

def compile_tket(qc, params):
  print(what(qc))
  return ""
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
    params = autoParam(len(qc.parameters))
    converted = compile_qiskit(qc, params=params)
  elif name == 'QNode':
    converted = compile_penny(qc, params=params)
  elif base == 'pybind11_object':
    converted = compile_tket(qc, params=params)
  elif name == 'Circuit':
    params = autoParam(len(list(qc._parameter_names_())))
    converted = compile_cirq(qc, params=params)
  else:
    raise ValueError(f'Unsupported circuit: {name}')

  # replace all params back with var_i
  for i in range(len(params)):
    converted = converted.replace(str(params[i]), f'var_{i}')

  return converted
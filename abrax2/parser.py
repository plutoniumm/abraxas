from _utils_compile import matrix_to_str, valid_gates
from typing import Dict, Union, Callable, List
from qiskit.qasm2 import dumps

Hook = Union[Callable, List[Callable]]

def compile_penny(qc):
  qc2 = qc
  qc2.construct([[0.1, 0.3, 0.5]], {})
  t = qc2.qtape.to_openqasm().strip()

  return t

def compile_qiskit(qc):
  t = dumps(qc).strip()

  return t

def compile_tket(qc):
  from pytket.extensions.qiskit import tk_to_qiskit
  t = tk_to_qiskit(qc)
  t = dumps(t).strip()

  return t

def compile_cirq(qc):
  from cirq import qasm
  t = qasm(qc).strip()

  return t


def toPrime(qc, hooks=None):
  name = qc.__class__.__name__
  base = qc.__class__.__base__.__name__
  if hooks is None:
    hooks = {}
  if name == 'QuantumCircuit':
    qc2 = qc.copy()
    return compile_qiskit(qc2)
  elif name == 'QNode':
    return compile_penny(qc)
  elif base == 'pybind11_object':
    return compile_tket(qc)
  elif name == 'Circuit':
    return compile_cirq(qc)
  else:
    raise ValueError(f'Unsupported circuit: {name}')
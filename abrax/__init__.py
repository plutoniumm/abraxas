from .compiler import toCirq, toQiskit, toTket, toPenny, toCudaq, toPyquil, toBraket
from .parser import toQasm
from .utils import draw

def toQuil(qc) -> str:
  if isinstance(qc, str):
    if not 'qasm' in qc:
      raise ValueError('Invalid input. Please provide a valid QASM string.')
  else:
    qc = toQasm(qc)

  return toPyquil(qc).out()

def toQir(qc) -> str:
  if isinstance(qc, str):
    if not 'qasm' in qc:
      raise ValueError('Invalid input. Please provide a valid QASM string.')
  else:
    qc = toQasm(qc)

  module, _, __ = toCudaq(qc)
  from cudaq import translate

  return translate(module, format='qir-base')

def toQasm3(qc) -> str:
  if isinstance(qc, str):
    if not 'qasm' in qc:
      raise ValueError('Invalid input. Please provide a valid QASM string.')
  else:
    qc = toQasm(qc)

  from qiskit.qasm3 import dumps
  return dumps(qc)
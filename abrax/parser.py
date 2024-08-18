import numpy as np
import re

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
  from qiskit.qasm2 import dumps
  qc = qc.assign_parameters(params)
  t = dumps(qc).strip()

  return t

def compile_tket(qc, params):
  from qiskit.qasm2 import dumps
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

"""START: compile_quil"""
def _quil_parse_decl(line):
  line = line.split(" ")
  typ = line[2] # BIT[2]
  size = int(typ.split("[")[1].split("]")[0])

  typ = typ.split("[")[0]

  return typ, size

def _quil_parse_gate(line):
  line = line.split(" ")
  qubit = line[-1]
  full_instr = line[0] # RY(theta1[0]) OR H
  instr = full_instr.split("(")[0]
  if "(" in full_instr:
    params = full_instr.split("(")[1].split(")")[0]
    params = params.split("[")[0].split(",")
    # now we need to check if theres letters in the params
    # if yes we prefix with 'var_'
    for i in range(len(params)):
      if any(c.isalpha() for c in params[i]):
        params[i] = "var_" + params[i]
  else:
    params = []

  if len(line) == 3:
    qubit = [line[1], qubit]

  return instr, qubit, params

def compile_quil(quilstr):
  quilstr = re.sub(r"//.*\n", "", quilstr)
  init = "OPENQASM 2.0;\ninclude \"qelib1.inc\";"
  qasm = ""

  # qregs, cregs, variables
  qubits = []
  variables = []
  for line in quilstr.split("\n"):
    if "DECLARE" in line:
      typ, size = _quil_parse_decl(line)
      if typ == "BIT":
        qasm += f"creg meas[{size}];\n"
    elif "MEASURE" in line:
      [_, qubit, creg] = line.split(" ")
      creg = int(creg.split("[")[1].split("]")[0])
      qasm += f"measure q[{qubit}] -> meas[{creg}];\n"
      qubits.append(qubit)
    else:
      instr, qubit, params = _quil_parse_gate(line)
      if len(instr) < 1 or len(qubit) < 1:
        continue
      variables.extend(params)
      if len(params) > 0:
        gate = f"{instr.lower()}({params[0]}) q[{qubit}]"
        qubits.append(qubit)
      else:
        if len(qubit) == 2:
          gate = f"{instr.lower()} q[{qubit[0]}],q[{qubit[1]}]"
          qubits.append(qubit[0])
          qubits.append(qubit[1])
        else:
          gate = f"{instr.lower()} q[{qubit}]"
          qubits.append(qubit)
      # endif
      qasm += f"{gate};\n"
    # endif
  # endfor
  qubits = list(set(qubits))
  qasm = qasm.replace("cnot", "cx")
  qasm = "\nqreg q[{}];\n".format(len(qubits)) + qasm
  qasm = (init + qasm).strip()

  variables = list(set(variables))
  variables = [i for i in variables if i.startswith("var_")]
  return qasm, variables

def autoParam(int):
  rand = np.round(np.random.rand(), 6)
  rand = [rand+(i/1e5) for i in range(int)]
  rand = np.round(rand, 7)
  return rand

def toQasm(qc):
  name = qc.__class__.__name__
  base = qc.__class__.__base__.__name__
  mod = qc.__module__.split('.')[0]
  params = [0]
  qasmd = None


  if name == 'QNode': # PennyLane
    qc2 = qc
    names = Unlist()
    qc2(names)
    names = [str(i) for i in names]
    params = autoParam(len(names))
    qasmd = compile_penny(qc2, params=params)

  elif base == 'pybind11_object': # tket
    names = []
    for p in qc:
      names.extend(p.free_symbols())
    names = list(set(names))
    params = autoParam(len(names))
    qasmd = compile_tket(qc, params=params)

  elif mod == 'braket':
    from qiskit_braket_provider.providers.adapter import to_qiskit
    qc = to_qiskit(qc)
    names = [i.name for i in qc.parameters]
    params = autoParam(len(names))
    qasmd = compile_qiskit(qc, params=params)

  elif name == 'QuantumCircuit': # Qiskit
    names = [i.name for i in qc.parameters]
    params = autoParam(len(names))
    qasmd = compile_qiskit(qc, params=params)

  elif name == 'Circuit': # Cirq
    names = list(qc._parameter_names_())
    params = autoParam(len(names))
    qasmd = compile_cirq(qc, params=params)

  elif name == 'Program': # Quil
    qasmd, names = compile_quil(qc.out())
    params = autoParam(len(names))
  elif name == 'PyKernel': # CudaQ
    if hasattr(qc, 'arguments'):
      args = qc.arguments
      if len(args) > 0:
        raise ValueError('Arguments not supported yet.')

    from cudaq import translate
    params = []
    qasmd = translate(qc, format="openqasm2")
  else:
    raise ValueError(f'Unsupported circuit: {name}')

  for i in range(len(params)):
    names[i] = names[i].replace("[", "_").replace("]", "")
    qasmd = qasmd.replace(str(params[i]), f'var_{names[i]}')

  return qasmd
from ._utils_compile import matrix_to_str, valid_gates


# check if .index or ._index is a valid index
def isIndex(qc):
  gate = qc.data[0][1][0]
  if hasattr(gate, 'index'):
    return 'index'
  elif hasattr(gate, '_index'):
    return '_index'


def qis_preprep(qc):
  from qiskit import QuantumCircuit
  from numpy import pi

  qregs = qc.qregs
  cregs = qc.cregs
  newc = QuantumCircuit(*qregs, *cregs)

  for i in qc.data:
    gate = i[0].name
    if gate not in valid_gates:
      raise ValueError(
        f'Invalid gate: {gate}, try decomposing the circuit. Or it may be unsupported by abraxas.'
      )

    if gate == 'u1':
      newc.u(0, 0, i[0].params[0], i[1][0])
    elif gate == 'u2':
      newc.u(pi / 2, i[0].params[0], i[0].params[1], i[1][0])
    elif gate == 'u3':
      newc.u(i[0].params[0], i[0].params[1], i[0].params[2], i[1][0])
    else:
      newc.append(i)

  return newc


def getParam(p):
  if isinstance(p, float):
    p = round(p, 4)

  return str(p)


def compile_pennylane(qfunc) -> str:
  from ._utils_parse import pnl_gate_map

  tape = qfunc.qtape
  num_qubits = len(tape.wires.tolist())
  matrix = [[] for _ in range(num_qubits)]

  ops2 = tape.operations
  # everytime there is a Tofolli, remove it and add 2 CNOTs a,b | b,c
  for i in range(len(ops2)):
    if ops2[i].name == 'Toffoli':
      a, b, c = ops2[i].wires.tolist()
      tape.operations[i] = tape.operations[i]._replace(
        name='CNOT', wires=[a, b]
      )
      tape.operations.insert(
        i + 1, tape.operations[i]._replace(name='CNOT', wires=[b, c])
      )


  for i in tape.operations:
    gate = i.name
    qubits = i.wires.tolist()
    params = i.parameters
    # name reverse
    if gate in pnl_gate_map.values():
      gate = list(pnl_gate_map.keys())[
        list(pnl_gate_map.values()).index(gate)
      ]
    if gate not in valid_gates:
      print(f'USED GATE: {gate}')
      raise ValueError(
        f'Invalid gate: {gate}, try decomposing the circuit. Or it may be unsupported by abraxas.'
      )

    if len(params) > 0:
      param = ','.join([getParam(x) for x in params])
    else:
      param = None

    if len(qubits) == 1:
      if param:
        matrix[qubits[0]].append([gate, param])
      else:
        matrix[qubits[0]].append(gate)
    elif len(qubits) == 2:
      matrix[qubits[0]].append([gate, qubits[1]])
    else:
      raise ValueError(
        f'Unsupported operation: {gate} with {len(qubits)} qubits'
      )

  return matrix_to_str(matrix)


def compile_qiskit(qc) -> str:
  matrix = [[] for _ in range(qc.num_qubits)]
  index = lambda x: getattr(x, isIndex(qc))  # noqa

  for i in qc.data:
    gate = i[0].name
    if gate not in valid_gates:
      print(qc.draw())
      raise ValueError(
        f'Invalid gate: {gate}, try decomposing the circuit. Or it may be unsupported by abraxas.'
      )
    if gate == 'measure':
      continue

    qargs = i[1]
    if len(i[0].params) > 0:
      param = ','.join([getParam(x) for x in i[0].params])
    else:
      param = None

    # if the gate is a single qubit gate
    # it may have a param
    idx = index(qargs[0])
    if len(qargs) == 1:
      if param:
        matrix[idx].append([gate, param])
      else:
        matrix[idx].append(gate)
    # if the gate is a two qubit gate
    # it wont have a param
    elif len(qargs) == 2:
      matrix[idx].append([gate, index(qargs[1])])
    else:
      raise ValueError(
        f'Unsupported operation: {gate} with {len(qargs)} qubits'
      )

  return matrix_to_str(matrix)


def toPrime(qc):
  name = qc.__class__.__name__
  if name == 'QuantumCircuit':
    qc2 = qis_preprep(qc)
    return compile_qiskit(qc2)
  elif name == 'QNode':
    return compile_pennylane(qc)
  else:
    raise ValueError(f'Unsupported circuit: {name}')

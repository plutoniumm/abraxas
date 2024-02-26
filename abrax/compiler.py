valid_gates = [
  ['h', 'x', 'y', 'z'],
  ['s', 't', 'sdg', 'tdg'],
  ['cx', 'cy', 'cz'],
  ['swap', 'iswap'],
  ['rx', 'ry', 'rz'],
  ['u', 'u1', 'u2', 'u3'],
  ['id'],
]
valid_gates = [i for j in valid_gates for i in j]


# check if .index or ._index is a valid index
def isIndex(qc):
  gate = qc.data[0][1][0]
  if hasattr(gate, 'index'):
    return 'index'
  elif hasattr(gate, '_index'):
    return '_index'


def preprocess(qc):
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


def compile_qiskit(qc, config) -> str:
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

  matrix = [*zip(*matrix)]
  stris = ['-' + str(i) for i in range(qc.num_qubits)]
  for i in range(len(matrix)):
    for j in range(len(matrix[0])):
      if isinstance(matrix[i][j], list):
        arg = matrix[i][j][1]
        # arg may have , in it and parser can deal with it
        stris[j] += f' {matrix[i][j][0]}({arg})'
      else:
        stris[j] += f' {matrix[i][j]}'

    # padding stris to make them equal width
    max = 0
    for j in stris:
      if len(j) > max:
        max = len(j)

    for j in range(len(stris)):
      stris[j] += ' ' * (max - len(stris[j]))

  return '\n'.join(stris)


default = {}


def toPrime(qc, config=default):
  name = qc.__class__.__name__
  if name == 'QuantumCircuit':
    qc2 = preprocess(qc)
    return compile_qiskit(qc2, config)
  else:
    raise ValueError(f'Unsupported circuit: {name}')

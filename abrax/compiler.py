from ._utils_compile import matrix_to_str, valid_gates


# check if .index or ._index is a valid index
def isIndex(qc):
  gate = qc.data[0][1][0]
  if hasattr(gate, 'index'):
    return 'index'
  elif hasattr(gate, '_index'):
    return '_index'


from typing import Dict, Union, Callable, List

Hook = Union[Callable, List[Callable]]


def qis_preprep(qc, hooks: Dict[str, Hook]):
  from qiskit import QuantumCircuit
  from numpy import pi

  qregs = qc.qregs
  cregs = qc.cregs
  newc = QuantumCircuit(*qregs, *cregs)

  for i in qc.data:
    # i = (gate, qargs, cargs)
    # gate is just the gate applied
    # qargs is the qubits the gate is applied to
    gate = i[0].name
    if (gate not in valid_gates) and (gate not in hooks.keys()):
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
      # if hooks is not None and gate in hooks:
      #   # a gate may be replaced by multiple gates
      #   # hook is key: lambda (circuit, instruction): ...
      #   if isinstance(hooks[gate], list):
      #     for j in hooks[gate]:
      #       j(newc, i)
      #   else:
      #     hooks[gate](newc, i)
      # else:
      newc.append(i)

  return newc


def getParam(p):
  if isinstance(p, float):
    p = round(p, 4)

  return str(p)


def flat(l):
  out = []
  for item in l:
    if isinstance(item, (list, tuple)):
      out.extend(flat(item))
    else:
      out.append(item)
  return out


def compile_pennylane(qfunc, hooks) -> str:
  from ._utils_parse import (
    pnl_gate_map,
    pnl_toffoli,
    PNLGate,
    pnl_rot,
    pwires,
  )

  pi = 3.141592653589793
  tape = qfunc.qtape
  num_qubits = len(tape.wires.tolist())
  matrix = [[] for _ in range(num_qubits)]

  ops = tape.operations
  # DECOMPOSITIONS
  for i in range(len(ops)):
    if ops[i].name == 'Toffoli':
      ops[i] = pnl_toffoli(ops[i])
    elif ops[i].name == 'Rot':
      ops[i] = pnl_rot(ops[i])
    elif ops[i].name == 'S':
      wires = pwires(ops[i].wires)
      ops[i] = [PNLGate('T', wires, [])] * 2
    elif ops[i].name == 'Sdg':
      ops[i] = [PNLGate('Tdg', wires, [])] * 2
    else:
      pass

  ops = flat(ops)

  for i in ops:
    gate = i.name
    qubits = pwires(i.wires)
    params = i.parameters
    # name reverse
    if gate in pnl_gate_map.values():
      gate = list(pnl_gate_map.keys())[
        list(pnl_gate_map.values()).index(gate)
      ]

    # manual map in for T and Tdg
    if gate == 'T':
      gate = 'rz'
      params = [pi / 4]
    elif gate == 'Tdg':
      gate = 'rz'
      params = [-pi / 4]
    else:
      gate = gate.lower()

    if gate not in valid_gates:
      print(f'USED GATE: {gate}')
      raise ValueError(
        f'Invalid gate: {gate}, try decomposing the circuit. Or it may be unsupported by abraxas.'
      )

    if len(qubits) == 2:
      # first fill all unequal rows with id
      # then add cx
      mlen = max([len(x) for x in matrix])
      for l in range(len(matrix)):
        if len(matrix[l]) < mlen:
          for _ in range(mlen - len(matrix[l])):
            matrix[l].append('id')

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
      raise ValueError(
        f'Invalid gate: {gate}, try decomposing the circuit. Or it may be unsupported by abraxas.'
      )
    if gate == 'measure':
      continue

    # for cx, fill all rows with id
    if len(i[1]) == 2:
      mlen = max([len(x) for x in matrix])
      for l in range(len(matrix)):
        if len(matrix[l]) < mlen:
          for _ in range(mlen - len(matrix[l])):
            matrix[l].append('id')

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


def toPrime(qc, hooks=None):
  name = qc.__class__.__name__
  if hooks is None:
    hooks = {}
  if name == 'QuantumCircuit':
    qc2 = qis_preprep(qc, hooks)
    return compile_qiskit(qc2)
  elif name == 'QNode':
    return compile_pennylane(qc, hooks)
  else:
    raise ValueError(f'Unsupported circuit: {name}')

from dataclasses import dataclass


@dataclass
class PNLGate:
  name: str
  wires: list
  parameters: list


def pwires(wires):
  if not isinstance(wires, list):
    wires = wires.tolist()
  return wires


def pnl_tdg(wire):
  return [
    PNLGate('RZ', [wire], [-0.7854]),
  ]


# rot(a,b,c)->rz(c)ry(b)rz(a)
def pnl_rot(rot):
  params = rot.parameters
  wires = pwires(rot.wires)
  a, b, c = params

  return [
    PNLGate('RZ', wires, [c]),
    PNLGate('RY', wires, [b]),
    PNLGate('RZ', wires, [a]),
  ]


def pnl_toffoli(toffoli):
  a, b, c = pwires(toffoli.wires)
  # Ref: Treat as same
  # Tdg = RZ(-pi/4)
  # T = RZ(pi/4)
  # Sdg = RZ(-pi/2)
  # S = RZ(pi/2)
  substitute = [
    ['Hadamard', [c]],
    ['CNOT', [c, b]],
    ['Tdg', [c]],
    ['CNOT', [c, a]],
    ['T', [c]],
    ['CNOT', [c, b]],
    ['T', [b]],
    ['Tdg', [c]],
    ['CNOT', [c, a]],
    ['CNOT', [b, a]],
    ['T', [c]],
    ['T', [a]],
    ['Tdg', [b]],
    ['Hadamard', [c]],
    ['CNOT', [b, a]],
  ]

  for j in range(len(substitute)):
    substitute[j] = PNLGate(
      name=substitute[j][0],
      wires=substitute[j][1],
      parameters=[],
    )

  return substitute


pnl_gate_map = {
  'id': 'Identity',
  'h': 'Hadamard',
  'x': 'PauliX',
  'y': 'PauliY',
  'z': 'PauliZ',
  'u': 'U3',
  'cx': 'CNOT',
  'swap': 'SWAP',
  'iswap': 'ISWAP',
  'p': 'PhaseShift',
}


def parse_circuit(string):
  lines = map(lambda e: e.strip(), string.strip().split('\n'))
  cleaned = []

  for line in lines:
    if not (line.startswith('-') or line.startswith('|>')):
      # - is a layer, |> is a continuation
      continue
    else:
      cleaned.append(line)

  by_rows = [list(filter(None, e.split(' '))) for e in cleaned]

  # sanity checks
  # check if all rows have the same length
  l = by_rows[0]
  for idx, row in enumerate(by_rows):
    if len(row) != len(l):
      raise Exception(
        f'Row {idx} has a different length than row {idx-1}'
      )

  return list(map(list, zip(*by_rows)))


isClose = lambda a, b: abs(a - b) < 0.001

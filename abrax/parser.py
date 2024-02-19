from re import compile

no_gate = compile("-{1,}")

def parse_circuit(string):
  lines = map(lambda e: e.strip(), string.strip().split("\n"))
  cleaned =[]

  for line in lines:
    if not \
    (line.startswith("-") or line.startswith("|>")):
    # - is a layer, |> is a continuation
      continue
    else:
      cleaned.append(line)

  by_rows = [list(filter(None, e.split(" "))) for e in cleaned]

  # sanity checks
  # check if all rows have the same length
  l = by_rows[0]
  for idx, row in enumerate(by_rows):
    if len(row) != len(l):
      raise Exception(f"Row {idx} has a different length than row {idx-1}")

  return list(map(list, zip(*by_rows)))

def parse_param(p):
  # if float or int continue
  if isinstance(p, (float, int)):
    return p
  # if not, it's a string, if includes . it's a float
  p = p.strip()
  return float(p) if "." in p else int(p)

def resolve_circuit(circuit, qc, config):
  for layerNo, layer in enumerate(circuit):
    if all([e.lower() == "-" for e in layer]):
      continue
    if all([e.lower() == "h" for e in layer]):
      qc.h([i for i in range(len(layer))])
      continue
    for wireNo, gate in enumerate(layer):
      if no_gate.match(gate):
        continue
      gate = gate.lower()
      if "(" in gate and ")" in gate:
        gate_name = gate[:gate.index("(")]
        param = gate[gate.index("(") + 1:gate.index(")")]
        op = getattr(qc, gate_name)

        if "," in param:
          param = param \
            .split(",") \
            .map(lambda e: parse_param(e))
          param = param + [wireNo]
        else:
          param = [parse_param(param), wireNo]
      else:
        param = [wireNo]
        op = getattr(qc, gate)

      op(*param)

  if config['measure']:
    qc.measure_all()
  return qc

default = {
  'measure': True,
}
def A(stri, qc, config=default):
  circuit = parse_circuit(stri)
  return resolve_circuit(circuit, qc, config)
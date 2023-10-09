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
  return list(map(list, zip(*by_rows)))

def resolve_circuit(circuit, qc):
  for layerNo, layer in enumerate(circuit):
    if all([e.lower() == "-" for e in layer]):
      continue
    if all([e.lower() == "h" for e in layer]):
      qc.h([i for i in range(len(layer))])
      continue
    for wireNo, gate in enumerate(layer):
      if gate == "-":
        continue
      gate = gate.lower()
      if "(" in gate and ")" in gate:
        gate_name = gate[:gate.index("(")]
        param = gate[gate.index("(") + 1:gate.index(")")]
        op = getattr(qc, gate_name)
        if "," in param:
          param = list(map(int, param.split(","))) + [wireNo]
        else:
          param = [int(param), wireNo]
      else:
        param = [wireNo]
        op = getattr(qc, gate)

      op(*param)

  qc.measure_all()
  return qc

def A(stri, qc):
  circuit = parse_circuit(stri)
  return resolve_circuit(circuit, qc)
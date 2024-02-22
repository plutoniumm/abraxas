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


def isClose(a, b):
  return abs(a - b) < 0.001

def matrix_to_str(matrix):
  matrix = [*zip(*matrix)]
  stris = ['-' + str(i) for i in range(len(matrix))]
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

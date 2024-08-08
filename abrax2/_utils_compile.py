# padd rows with [] to make them equal width
def equalize_widths(matrix):
  mlen = max([len(i) for i in matrix])
  for i in range(len(matrix)):
    matrix[i] += ['---'] * (mlen - len(matrix[i]))

  return matrix


def matrix_to_str(matrix):
  qubits = len(matrix)
  matrix = equalize_widths(matrix)
  matrix = [*zip(*matrix)]
  stris = ['-' + str(i) for i in range(qubits)]
  for i in range(len(matrix)):
    for j in range(len(matrix[0])):
      if isinstance(matrix[i][j], list):
        arg = matrix[i][j][1]
        # arg may have , in it and parser can deal with it
        stris[j] += f' {matrix[i][j][0]}({arg})'
      else:
        if matrix[i][j] == 'id':
          stris[j] += ' ' + ('-' * 3)
        else:
          stris[j] += f' {matrix[i][j]}'

    # padding stris to make them equal width
    mlen = max([len(j) for j in stris])
    for j in range(len(stris)):
      stris[j] += ' ' * (mlen - len(stris[j]))

  return '\n'.join(stris)


valid_gates = [
  ['h', 'x', 'y', 'z'],
  ['s', 't', 'sdg', 'tdg'],
  ['cx', 'cy', 'cz'],
  ['crx', 'cry', 'crz'],
  ['swap', 'iswap'],
  ['rx', 'ry', 'rz'],
  ['u', 'u1', 'u2', 'u3'],
  ['id', 'p'],
]
valid_gates = [i for j in valid_gates for i in j]

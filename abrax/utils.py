def draw(qc, **kwargs):
  name = qc.__class__.__name__
  base = qc.__class__.__base__.__name__
  mod = qc.__module__.split('.')[0]

  if name == 'QuantumCircuit': # Qiskit
    print(qc.draw(**kwargs))
  elif name == 'QNode': # PennyLane
    from pennylane import draw
    print(draw(qc)(**kwargs))
  elif base == 'pybind11_object': # tket
    raise NotImplementedError('Drawing tket circuits is not supported yet.')
  elif name == 'Circuit': # Cirq
    print(qc)
  elif name == 'Program': # Quil
    import pyquil.latex
    res = pyquil.latex.to_latex(qc, **kwargs)
    print(res)
  elif mod == 'bracket':
    print(qc)
  elif name == 'PyKernel': # CudaQ
    from cudaq import draw
    print(draw(qc, **kwargs))
  else:
    raise ValueError(f'Unsupported circuit: {name}')

  return 0
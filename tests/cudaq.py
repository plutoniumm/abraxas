def bell_cudaq():
  from cudaq import make_kernel
  kernel = make_kernel()
  q = kernel.qalloc(q)

  kernel.h(q[0])
  kernel.cx(q[0], q[1])
  kernel.rx(0.1*0, q[0])
  kernel.rx(0.1*1, q[1])

  kernel.mz(q[0])
  kernel.mz(q[1])

  return kernel
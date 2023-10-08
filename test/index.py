from abrax import A

circuit = A("""
  // I AM JESUS
  // SPACES ARE SIGNIFICANT, DONOT add them inside a gate
  - H CX(4) RX(10)
  - H -    -
  - H -    CX(4)
  - H X    RY(55)
  - H -    -
  """,
  name="circuit"
)

print(circuit)
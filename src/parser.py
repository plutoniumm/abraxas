from qiskit import QuantumCircuit

def parse_circuit(string):
  lines = string.strip().split("\n")
  lines = [e.strip() for e in lines if not e.startswith("//")]

  by_rows = [list(filter(None, e.split(" "))) for e in lines]
  return list(map(list, zip(*by_rows)))

def resolve_circuit(circuit, name):
  qc = QuantumCircuit(len(circuit[0]), name=name)

  for wireNo, wire in enumerate(circuit):
    for gateNo, gate in enumerate(wire):
      if gate == "-":
        continue
      gate = gate.lower()
      if "(" in gate and ")" in gate:
        gate_name = gate[:gate.index("(")].lower()
        param = gate[gate.index("(") + 1:gate.index(")")]
        if "," in param:
          param = list(map(int, param.split(","))) + [wireNo]
          getattr(qc, gate_name)(**param)
        else:
          getattr(qc, gate_name)(int(param), wireNo)
      else:
          getattr(qc, gate)(wireNo)

  qc.measure_all()
  return qc

test="""
// I AM JESUS
// SPACES ARE SIGNIFICANT, DONOT add them inside a gate
- H CX(4) RX(10)
- H -    -
- H -    CX(4)
- H X    RY(55)
- H -    -
"""

def A(stri, name="circuit"):
  circuit = parse_circuit(stri)
  return resolve_circuit(circuit, name)
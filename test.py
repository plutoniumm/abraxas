from abrax.compiler import toBraket, toCirq, toCudaq, toQiskit, toPenny, toPyquil, toTket
from abrax import toQasm, toQuil, toQir, toQasm3
from abrax.utils import draw

from tests.braket import bell_bracket, Bracket, FreeParameter
from tests.tket import bell_quan, Circuit, Symbol
from tests.qiskit import bell_ibm, qk, h2_vqe
from tests.quil import bell_quil, Program, G
from tests.penny import bell_penny, qml, dev
from tests.cirq import bell_cirq, cirq
# from tests.cudaq import bell_cudaq
from tests.utils import QASM

# print(toQasm(bell_penny))
# print(toQasm(bell_quan()))
# print(toQasm(bell_ibm()))
# print(toQasm(bell_cirq()))
# print(toQasm(bell_quil()))
# print(toQasm(bell_bracket()))
# print(toQasm(bell_cudaq()))

# print(toQiskit(QASM))
# print(toPenny(QASM, dev))
# print(toCirq(QASM))
# print(toTket(QASM))
# print(toBraket(QASM))
# print(toCudaq(QASM)[0])
# print(toQuil(QASM))

vqe_qasm = toQasm(h2_vqe())
braketed = toBraket(vqe_qasm)
print(braketed)

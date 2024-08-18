from abrax.compiler import toBracket, toCirq, toCudaq, toQiskit, toPenny, toQuil, toTket
from abrax.parser import toQasm
from abrax.utils import draw

from tests.tket import bell_quan, Circuit, Symbol
from tests.quil import bell_quil, Program, G
from tests.penny import bell_penny, qml, dev
from tests.cirq import bell_cirq, cirq
from tests.qiskit import bell_ibm, qk
# from tests.cudaq import bell_cudaq
from tests.utils import QASM

print(toQasm(bell_penny))
print(toQasm(bell_quan()))
print(toQasm(bell_ibm()))
print(toQasm(bell_cirq()))
print(toQasm(bell_quil()))
# print(toQasm(bell_cudaq()))

print(toQiskit(QASM))
print(toPenny(QASM, dev))
print(toCirq(QASM))
print(toTket(QASM))
# print(toCudaq(QASM))
print(toQuil(QASM))
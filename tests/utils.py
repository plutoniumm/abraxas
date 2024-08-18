QASM="""
OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];


h q[0];
cx q[0],q[1];
ry(var_theta1) q[0];
ry(var_theta2) q[1];
""".strip()

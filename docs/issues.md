## Known Issues
- Don't parameterise `exponent` in cirq for variational circuits. Else it will hard code in some random value. As a slow hack you can run the transpiler in a for loop everytime the exponent/rads change.
- CudaQ cannot do variational gates "toQasm" and writing a parser for QIR/MLIR is extremely expensive. `kernel` should not take any arguments.
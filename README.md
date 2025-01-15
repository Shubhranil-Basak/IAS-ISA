# IAS-ISA: Assembler and Simulator for the IAS Instruction Set Architecture

This project provides an assembler and simulator for the Institute for Advanced Study (IAS) Instruction Set Architecture (ISA), implemented in Python.

## Overview

The IAS machine, also known as the von Neumann machine, is a historical computer architecture designed by John von Neumann. This project emulates the IAS machine's functionality, allowing users to assemble and execute programs written in its assembly language.

## Features

- **Assembler**: Converts IAS assembly language code into machine code.
- **Simulator**: Executes the machine code, emulating the IAS machine's behavior.

## Repository Structure

- `assembler.py`: Contains the assembler implementation.
- `processor.py`: Contains the simulator implementation.
- `instructions.txt`: Lists the supported IAS assembly instructions.
- `assembly_codes/`: Directory containing sample assembly programs.
- `object_files/`: Directory for storing the assembled machine code files.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gathik-jindal/IAS-ISA.git
   cd IAS-ISA
   ```

2. **Run the assembler**:
   ```bash
   python assembler.py assembly_codes/sample_program.asm
   ```
   This will generate a machine code file in the object_files/ directory.

3. **Run the simulator**:
   ```bash
   python processor.py object_files/sample_program.obj
   ```
   This will execute the machine code and display the output.

## Requirements
   Python 3.x

## Contributing
   Contributions are welcome! Feel free to open issues or submit pull requests.

## License
   This project is licensed under the MIT License.

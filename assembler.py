import re
import sys


class Assembler:
    def __init__(self, inputFileName: str, outputFileName: str):
        if self.__checkType((inputFileName, str), (outputFileName, str)):
            self.__inputFileName = inputFileName
            self.__outputFileName = outputFileName

    def __getOpCode(self, op: str, address="") -> str:
        """
        Returns the opcode.

        arguemnts:
            op: the instruction itself
            address: default is \"\".
            The address should be of form M(XXXX)
        """
        if (op == 'ADD' and address[0] == 'M'):
            return '00000101'

        elif (op == 'STOR' and (',' not in address)):
            return '00100001'

        elif (op == 'LOAD' and address[0:2] == 'M('):
            return '00000001'

        elif (op == 'LOAD' and address[0:2] == '-M'):
            return '00000010'

        elif (op == 'LOAD' and address[0] == '|'):
            return '00000011'

        elif (op == 'LOAD' and address[0:2] == '-|'):
            return '00000100'

        elif (op == 'LOAD' and address[:5] == 'MQ,M('):
            return '00001001'

        elif (op == 'LOAD' and address == 'MQ'):
            return '00001010'

        elif (op == 'ADD' and address[0] == '|'):
            return '00000111'

        elif (op == 'SUB' and address[0] == 'M'):
            return '00000110'

        elif (op == 'SUB' and address[0] == '|'):
            return '00001000'

        elif (op == 'DIV'):
            return '00001100'

        elif (op == 'LSH'):
            return '00010100'

        elif (op == 'RSH'):
            return '00010101'

        elif (op == 'JUMP+' and address[-6:-1] == ',0:19'):
            return '00001111'

        elif (op == 'JUMP+' and address[-7:-1] == ',20:39'):
            return '00010000'

        elif (op == 'JUMP' and address[-6:-1] == ',0:19'):
            return '00001101'

        elif (op == 'JUMP' and address[-7:-1] == ',20:39'):
            return '00001110'

        elif (op == 'MUL'):
            return '00001011'

        elif (op == 'STOR' and address[-6:-1] == ',8:19'):
            return '00010010'

        elif (op == 'STOR' and address[-7:-1] == ',28:39'):
            return '00010011'

        elif (op == 'HALT'):
            return '11111111'

        elif (op == 'NOP'):
            return '00000000'

        else:
            self.__printErrorAndExit(
                f"Error: Invalid Instruction at line {self.__lineNum} in the instruction \"{op}\".")

    def __printErrorAndExit(self, message: str) -> None:
        """
        Prints the error message and exits.
        """
        print(message)
        sys.exit(1)

    def __checkType(self, *checkList):
        """
        checkList must of the form,
        (arg1, type1), (arg2, type2), (arg3, type3), ..., (argN, typeN)
        Returns true if all the types specified are correct and none of the
        arguments are None.
        Throws an Error and exits otherwise.
        """

        for arg in checkList:
            if (arg[0] == None or not isinstance(arg[0], arg[1])):
                self.__printErrorAndExit(
                    f"{arg[0]} is not of valid type {arg[1]}.")

        return True

    def __convertToBin(self, num1: int, b=12) -> str:
        """
        Converts any numerical representation to bin.
        Currently only supports binary.

        TODO: Need to add functionality for more numeral systems. Like 0x, o.
        """
        n = bin(abs(num1))[2:]

        number = '0'*(b-len(n)-1) + n
        if num1 < 0:
            number = '1' + number
        else:
            number = '0' + number

        return number

    def __convertInstructionToBin(self, instr: str) -> str:
        """
        Converts the instruction to its binary equivalent.
        """
        pattern = "[0-9]+"

        instr = instr.split(" ")

        if len(instr) == 2:
            opcode = self.__getOpCode(instr[0], instr[1])
            num = re.findall(pattern, instr[1])
        else:
            opcode = self.__getOpCode(instr[0])
            num = 0

        if (not num):
            address = '000000000000'

        else:
            address = self.__convertToBin(int(num[0]))

        instruction = opcode + " " + address

        return instruction

    def __write(self, instr: str) -> None:
        """
        Writes the instruction into the object file.
        """
        self.__oFh.write(instr)

    def run(self):
        """
        Runs the actual assembler.
        """

        self.__lineNum = 1

        with open(self.__inputFileName, 'r') as self.__iFh:
            self.__lines = self.__iFh.readlines()

        self.__oFh = open(self.__outputFileName, "w+")

        for line in self.__lines:

            line = line.split('//')[0]
            line = line.strip(" \n")
            line = line.split(';')

            if (len(line) == 1 and line[0] == ''):
                self.__write("\n")

            elif (len(line) == 2):
                instruction = self.__convertInstructionToBin(line[0].strip(
                    " \n")) + " " + self.__convertInstructionToBin(line[1].strip(" \n"))

                self.__write(instruction + "\n")

            elif (len(line) == 1 and not line[0].isnumeric()):
                instruction = self.__convertInstructionToBin(
                    line[0].strip(" \n"))

                self.__write(instruction + "\n")

            elif (len(line) == 1 and line[0].isdecimal()):
                instruction = self.__convertToBin(int(line[0]), 40)

                self.__write(instruction + "\n")

            self.__lineNum += 1

        self.__oFh.close()


asm = Assembler("helloWorld.asm", "helloWorld.obj")
asm.run()

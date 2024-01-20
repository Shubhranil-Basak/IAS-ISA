import linecache
import sys

NOTHING = '0'*8 + ' ' + '0'*12
HALT = '11111111'
NOP = '00000000'
LOAD = '00000001'
LOADNeg = '00000010'
LOADMod = '00000011'
LOADNegMod = '00000100'  # LOAD -|M(X)|
ADD = '00000101'
SUB = '00000110'
ADDMod = '00000111'
SUBMod = '00001000'
LOADMQM = '00001001'  # LOAD MQ,M(X)
LOADMQ = '00001010'
MUL = '00001011'
DIV = '00001100'
JUMPl = '00001101'  # JUMP M(X,0:19)
JUMPr = '00001110'  # JUMP M(X,20:39)
JUMPlIfG = '00001111'  # JUMP+ M(X,0:19)
JUMPrIfG = '00010000'  # JUMP+ M(X,20:39)
STORr = '00010010'  # STOR M(X,8:19)
STORl = '00010011'  # STOR M(X,28:39)
LSH = '00010100'
RSH = '00010101'
STOR = '00100001'


def checkType(*args) -> bool:
    """
    Checks the type. It can take any number of parameters (tuples).
    Parameters are given as:
    (obj, type), (obj, type) .....
    """
    for x in args:
        if (x[0] == None or not isinstance(x[0], x[1])):
            return False

    return True


def convertToBin(num: int, b=12) -> str:
    """
    Converts any numerical representation to bin.
    Currently only supports binary.

    TODO: Need to add functionality for more numeral systems. Like 0x, o.
    """
    n = bin(abs(num))[2:]

    number = '0'*(b-len(n)) + n
    if num < 0:
        ans = ""
        for x in number:
            if x == '1':
                ans += '0'
            else:
                ans += '1'

        ans = int(ans, 2) + 1
        ans = bin(ans)[2:]
        number = ans

    return number


def convertToInt(word: str, mod=False) -> int:
    """
    Converts the given word to its integer reperesntation.
    """
    if word[0] == '1' and not mod:
        word = -int(word[1:], 2)
    else:
        word = int(word[1:], 2)

    return word


class MainMemory:
    def __init__(self, inputFileName: str):
        self.__inputFileName = inputFileName

    def getWord(self, lineNumber: int) -> str:
        """
        Gets the word from that Memory address. If the Memeory address is a string it is considered to be a binary number.
        """
        if checkType((lineNumber, str)):
            lineNumber = convertToInt(lineNumber)

        lineNumber += 1

        linecache.checkcache(self.__inputFileName)
        line = linecache.getline(self.__inputFileName,
                                 lineNumber).rstrip("\n")
        return line

    def replaceMemoryAddr(self, lineNumber: int, memAddr: str, leftOrRight: int) -> None:
        """
        Replaces memory address with the memAddr given. If it is in integer it is converted to binary.
        If leftOrRight = 1, then the left address is replaced, else the right one is replaced
        """

        if leftOrRight == 1:
            leftOrRight = -1
        else:
            leftOrRight = 1

        if checkType((memAddr, int)):
            memAddr = convertToBin(memAddr)

        with open(self.__inputFileName, 'r') as fh:
            lines = fh.readlines()

        line = lines[lineNumber].strip(" \n").split()
        line[leftOrRight] = memAddr
        lines[lineNumber] = " ".join(line) + '\n'

        with open(self.__inputFileName, 'w+') as fh:
            fh.writelines(lines)

    def writeAtMem(self, lineNumber: int, word: str) -> None:
        """
        Replaces an entire word in memory with given word.
        """
        with open(self.__inputFileName, 'r') as fh:
            lines = fh.readlines()

        lines[lineNumber] = word + '\n'

        with open(self.__inputFileName, 'w+') as fh:
            fh.writelines(lines)


class ALU:
    def __init__(self):
        self.__ACval = convertToBin(0, 40)
        self.__MQval = convertToBin(0, 40)

    def __printAC(self) -> None:
        """
        Prints contents of AC.
        """
        print(f"---AC now contains {self.__ACval}---")

    def __printMQ(self) -> None:
        """
        Prints contents of AC.
        """
        print(f"---MQ now contains {self.__MQval}---")

    def putAC(self, word) -> None:
        """
        Puts the value in AC.
        """
        self.__ACval = word

    def putMQ(self, word) -> None:
        """
        Puts the value in MQ.
        """
        self.__MQval = word

    def getAC(self) -> str:
        """
        Returns value of AC.
        """
        return self.__ACval

    def getMQ(self) -> str:
        """
        Returns value of MQ.
        """
        return self.__MQval

    def mq(self) -> None:
        """
        Does the LOAD MQ operation.
        """
        self.__ACval = self.__MQval
        self.__printAC()

    def lsh(self) -> None:
        """
        Does the LSH operation.
        """
        self.__ACval = convertToBin(int(self.__ACval, 2) * 2)
        self.__printAC()

    def rsh(self) -> None:
        """
        Does the RSH operation.
        """
        self.__ACval = convertToBin(int(self.__ACval, 2) / 2)
        self.__printAC()

    def add(self, word: str, mod=False) -> None:
        """
        Does the ADD operation. mod is set to false by default.
        """

        ac = convertToInt(word, mod)
        val = convertToInt(self.__ACval)
        val += ac
        self.__ACval = convertToBin(ac, 40)
        self.__printAC()

    def sub(self, word: str, mod=False) -> None:
        """
        Does the SUB operation. mod is set to false by default.
        """

        word = convertToInt(word, mod)
        ac = convertToInt(self.__ACval)
        ac -= word
        self.__ACval = convertToBin(ac, 40)
        self.__printAC()

    def mul(self, word: str) -> None:
        """
        Does the MUL operation.
        """

        word = convertToInt(word)
        val = convertToInt(self.__ACval)
        val *= word
        val = convertToBin(val, 80)
        self.__MQval = val[-39:]
        self.__ACval = val[:-39]
        self.__printAC()
        self.__printMQ()

    def div(self, word: str) -> None:
        """
        Does the DIV operation.
        """

        word = convertToInt(word)
        ac = convertToInt(self.__ACval)
        quo = int(ac/word)
        rem = ac % word
        self.__MQval = convertToBin(quo, 40)
        self.__ACval = convertToBin(rem, 40)
        self.__printAC()
        self.__printMQ()


class MBR:
    def __init__(self):
        self.__value = convertToBin(
            0, 8) + " " + convertToBin(-1, 12) + convertToBin(0, 8) + " " + convertToBin(-1, 12)

    def put(self, value: str) -> None:
        """
        Stores the value in MBR.
        """
        self.__value = value
        print(f"----Now MBR contains: {self.__value}----")

    def get(self) -> str:
        """
        Gets the value in MBR.
        """
        return self.__value

    def getri(self) -> str:
        """
        Returns the right instruction.
        """
        ret = self.__value.split()
        ret = " ".join(ret[2:])
        return ret

    def getli(self) -> str:
        """
        Returns the left instruction.
        """
        ret = self.__value.split()
        ret = " ".join(ret[:2])
        return ret


class IBR:
    def __init__(self):
        self.__value = convertToBin(0, 8) + " " + convertToBin(-1, 12)

    def put(self, word: str) -> None:
        """
        Puts an instruciton in the IBR.
        """
        self.__value = word
        print(f"----IBR now contains {self.__value}---")

    def get(self) -> str:
        """
        Gets the entire word stored in IBR.
        """
        return self.__value

    def getOpCode(self) -> str:
        """
        Gets the Opcode stored in IBR.
        """
        return self.__value.split(" ")[0]

    def getMemAddr(self) -> str:
        """
        Gets the memeory address stored in IBR.
        """
        return self.__value.split(" ")[1]

    def isEmpty(self) -> bool:
        """
        Checks if the IBR empty.
        """
        if self.getOpCode() == NOP:
            return True
        return False

    def clear(self) -> None:
        """
        Clears the IBR.
        """
        self.__value = NOTHING


class ProgramControlUnit:
    def __init__(self, mm: MainMemory, alu: ALU, PC=0):
        self.__IR = convertToBin(0, 8)
        self.__MAR = convertToBin(0, 12)
        self.__PC = convertToBin(PC, 12)
        self.__IBR = IBR()
        self.__MBR = MBR()
        self.__MainMemory = mm
        self.__ALU = alu
        self.flag = True  # only for jumps, False when we need to right jump

    def __decodeAndExecute(self) -> None:
        """
        Decodes and executes the processor.
        """

        if self.__IR == HALT:
            sys.exit(1)

        if self.__IR == NOP:
            return

        if self.__IR == LOAD:
            self.__MBR.put(self.__MainMemory.getWord(convertToInt(self.__MAR)))
            self.__ALU.putAC(self.__MBR.get())
            print(f"Loaded AC with value M(MAR). AC: {self.__ALU.getAC()}")
            return

        if self.__IR == LOADNeg:
            self.__MBR.put(
                convertToBin(-convertToInt(self.__MainMemory.getWord(convertToInt(self.__MAR)))))
            self.__ALU.putAC(self.__MBR.get())
            print(f"Loaded AC with value -M(MAR). AC: {self.__ALU.getAC()}")
            return

        if self.__IR == LOADMod:
            self.__MBR.put(convertToBin(
                abs(convertToInt(self.__MainMemory.getWord(convertToInt(self.__MAR))))))
            self.__ALU.putAC(self.__MBR.get())
            print(f"Loaded AC with value -M(MAR). AC: {self.__ALU.getAC()}")
            return

        if self.__IR == LOADNegMod:
            self.__MBR.put(
                convertToBin(-abs(convertToInt(self.__MainMemory.getWord(convertToInt(self.__MAR))))))
            self.__ALU.putAC(self.__MBR.get())
            print(f"Loaded AC with value -M(MAR). AC: {self.__ALU.getAC()}")
            return

        if self.__IR == ADD:
            self.__MBR.put(self.__MainMemory.getWord(convertToInt(self.__MAR)))
            self.__ALU.add(self.__MBR.get())
            print(f"Added M(MAR) with AC. AC: {self.__ALU.getAC()}")
            return

        if self.__IR == SUB:
            self.__MBR.put(self.__MainMemory.getWord(convertToInt(self.__MAR)))
            self.__ALU.sub(self.__MBR.get())
            print(f"Added M(MAR) with AC. AC: {self.__ALU.getAC()}")
            return

        if self.__IR == ADDMod:
            self.__MBR.put(self.__MainMemory.getWord(convertToInt(self.__MAR)))
            self.__ALU.add(self.__MBR.get(), mod=True)
            print(f"Added M(MAR) with AC. AC: {self.__ALU.getAC()}")
            return

        if self.__IR == SUBMod:
            self.__MBR.put(self.__MainMemory.getWord(convertToInt(self.__MAR)))
            self.__ALU.sub(self.__MBR.get(), mod=True)
            print(f"Added M(MAR) with AC. AC: {self.__ALU.getAC()}")
            return

        if self.__IR == LOADMQM:
            self.__MBR.put(self.__MainMemory.getWord(convertToInt(self.__MAR)))
            self.__ALU.putMQ(word)
            print(f"Loaded MQ with value -M(MAR). MQ: {self.__ALU.getMQ()}")
            return

        if self.__IR == LOADMQ:
            self.__ALU.mq()
            print(f"Loaded AC with MQ.")
            print(f"AC: {self.__ALU.getAC}, MQ: {self.__ALU.getMQ()}")
            return

        if self.__IR == MUL:
            self.__MBR.put(self.__MainMemory.getWord(convertToInt(self.__MAR)))
            self.__ALU.mul(self.__MBR.get())
            print(f"Did the multiply operation.")
            print(f"MQ: {self.__ALU.getMQ()}, AC: {self.__ALU.getAC()}")
            return

        if self.__IR == DIV:
            word = self.__MainMemory.getWord(convertToInt(self.__MAR))
            self.__ALU.div(word)
            print(f"Did the division operation.")
            print(f"MQ: {self.__ALU.getMQ()}, AC: {self.__ALU.getAC()}")
            return

        if self.__IR == JUMPl:
            self.__IBR = NOP
            self.__PC = self.__MAR
            print(
                f"Jumping to left instruction pointed by MAR (PC -> MAR): {convertToInt(self.__PC)}")

        if self.__IR == JUMPr:
            self.__IBR = NOP
            self.__PC = self.__MAR
            self.flag = False
            print(
                f"Jumping to right intruction pointed by MAR (PC -> MAR): {convertToInt(self.__PC)}")

        if self.__IR == JUMPlIfG:
            if convertToInt(self.__ALU.getAC()) > 0:
                self.__IBR = NOP
                self.__PC = self.__MAR
                print(
                    f"Jumping to left instruction pointed by MAR (PC -> MAR): {convertToInt(self.__PC)}")

        if self.__IR == JUMPrIfG:
            if convertToInt(self.__ALU.getAC()) > 0:
                self.__IBR = NOP
                self.__PC = self.__MAR
                self.flag = False
                print(
                    f"Jumping to right intruction pointed by MAR (PC -> MAR): {convertToInt(self.__PC)}")

        if self.__IR == STOR:
            self.__MBR.put(self.__AC)
            self.__MainMemory.writeAtMem(
                convertToInt(self.__MAR), self.__MBR.get())
            print(f"Stored AC at memory location: {convertToInt(self.__MAR)}")

        if self.__IR == STORr:
            self.__MBR.put(self.__ALU[-12:])
            self.__MainMemory.replaceMemoryAddr(
                convertToInt(self.__MAR), self.__MBR.get(), 0)
            print(f"Did the STOR M(X, 28:39) operation.")
            print(f"Now location {convertToInt(
                self.__MAR)} contains {self.__MBR.get()}")
            return

        if self.__IR == STORl:
            self.__MBR.put(self.__ALU[-12:])
            self.__MainMemory.replaceMemoryAddr(
                convertToInt(self.__MAR), self.__MBR.get(), 1)
            print(f"Did the STOR M(X, 8:19) operation.")
            print(f"Now location {convertToInt(
                self.__MAR)} contains {self.__MBR.get()}")
            return

        if self.__IR == LSH:
            self.__ALU.lsh()
            print(f"Did the LSH operator on AC.")
            print(f"AC now contains: {self.__ALU.getAC()}")
            return

        if self.__IR == RSH:
            self.__ALU.rsh()
            print(f"Did the RSH operator on AC.")
            print(f"AC now contains: {self.__ALU.getAC()}")
            return

    def run(self) -> None:
        """
        Runs the processor.
        """
        while True:
            if self.__IBR.isEmpty() and self.flag:

                self.__MAR = self.__PC
                print(f"Contents in PC moved into MAR.")
                print(f"PC: {self.__PC}, MAR: {self.__MAR}")

                self.__MBR.put(self.__MainMemory.getWord(self.__MAR))
                print(f"Memory fetched from location MAR and stored into MBR, MBR: {
                      self.__MBR.get()}")

                if self.__MBR.getli().split()[0] != NOP:

                    self.__IBR.put(self.__MBR.getri())
                    self.__IR, self.__MAR = self.__MBR.getli().split()
                    print(
                        f"Left instruction moved into IR and MAR, and right intruction in IBR")
                    print(f"IR: {self.__IR}, MAR: {
                          self.__MAR}, IBR: {self.__IBR.get()}")

                    self.__decodeAndExecute()

                else:

                    self.__IBR.put(self.__MBR.getri())
                    self.__IR = self.__IBR.getOpCode()
                    self.__MAR = self.__IBR.getMemAddr()
                    self.__PC = convertToBin(convertToInt(self.__PC) + 1)
                    print("Left Instruction is not required.")
                    print(f"Right instruction moved into IR and MAR.")
                    print(f"IR: {self.__IR}, MAR: {self.__MAR}")

                    self.__decodeAndExecute()

                    self.__IBR.clear()

            elif self.flag:

                self.__IR, self.__MAR = self.__IBR.getOpCode(), self.__IBR.getMemAddr()
                print(f"IR: {self.__IR}, MAR: {self.__MAR}")

                self.__PC = convertToBin(convertToInt(self.__PC) + 1)
                print(f"Updated PC, PC: {self.__PC}")

                self.__decodeAndExecute()

                self.__IBR.clear()

            else:

                self.__MAR = self.__PC
                self.__MBR.put(self.__MainMemory.getWord(
                    convertToInt(self.__MAR)))
                print(f"Memory fetched from location MAR and stored into MBR, MBR: {
                      self.__MBR.get()}")

                self.__IBR.put(self.__MBR.getri())
                self.__IR = self.__IBR.getOpCode()
                self.__MAR = self.__IBR.getMemAddr()
                print("Left Instruction is not required.")
                print(f"Right instruction moved into IR and MAR.")
                print(f"IR: {self.__IR}, MAR: {self.__MAR}")

                self.__decodeAndExecute()


CPU = ProgramControlUnit(MainMemory("helloWorld.obj"), ALU())
CPU.run()

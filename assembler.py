class Assembler:
    def __init__(self, inputFileName, outputFileName):
        self.__inputFileName = inputFileName
        self.__outputFileName = outputFileName

        self.opCodes = {
            "LOAD":
            {
                "M(": "00000001",
                "-M(": "00000010",
                "|M(": "00000011",
                "-|M(": "00000100",
                "MQ,M(": "00001001",
                "MQ": "00001010"
            },

            "ADD":
            {
                "M(": "00000101",
                "|M(": "00000111"
            },

            "SUB":
            {
                "M(": "00000110",
                "|M(": "00001000"
            },

            "MUL": "00001011",
            "DIV": "00001100",
            "LSH": "00010100",
            "RSH": "00010101",

            "JUMP":
            {
                "M(":
                {
                    "0:19)": "00001101",  # here we have to use endswith
                    "20:39)": "00001110"
                },

                "+ M(":
                {
                    "0:19)": "00001111",
                    "20:39)": "00010000"
                }
            },

            "STOR":
            {
                "M(": "00100001",
                "8:19)": "00010010",  # here we need to use both :(
                "28:39)": "00010011"
            }
        }

    def __read(self) -> None:
        """
        Reads the file content into a list.
        """
        with open(self.__inputFileName, 'r') as fh:
            self.__code = fh.readlines()

    def __output(self) -> None:
        """
        Outputs the entire code in an .obj file.
        TODO
        """

    def __split(self, word: str) -> None:
        """
        Splits the instruciton into left and right instruction.
        Also removes the trailing and leading white spaces in each of the instruction.

        TODO: Enable the split part.
        """
        # self.li, self.ri = word.split(',')
        self.li, self.ri = word, word
        self.li = self.li.strip()
        self.ri = self.ri.strip()

    def __matchOpCode(self, code: str) -> str:
        """
        Returns the binary representation of the OpCode

        TODO: Encoding for STOR is left.
        """

        possibleOpCodes = {}
        parentOpCode = ""
        for x in self.opCodes.keys():
            if code.startswith(x):
                possibleOpCodes = self.opCodes[x]
                parentOpCode = x
                break

        code = code.removeprefix(parentOpCode)
        code = code.strip()

        if isinstance(possibleOpCodes, str):
            return possibleOpCodes

        if parentOpCode == "JUMP":
            for x in self.opCodes[parentOpCode].keys():
                if code.startswith(x):
                    for y in self.opCodes[parentOpCode][x].keys():
                        if code.endswith(y):
                            return self.opCodes[parentOpCode][x][y]

        if parentOpCode != "STOR":
            for x in self.opCodes[parentOpCode].keys():
                if code.startswith(x):
                    return self.opCodes[parentOpCode][x]

    def __convertToBin(self, instruciton: str) -> str:
        """
        Converts the following instruction to its binary / machine code equivalent.
        """
        opCode = self.__matchOpCode(instruciton)
        return opCode

    def run(self):
        """
        The actual assembler running.
        """
        self.__read()

        for x in self.__code:
            self.__split(x)
            binaryRepOfInstruction = self.__convertToBin(self.li)
            print(binaryRepOfInstruction)


asm = Assembler("helloWorld.asm", "helloWorld.obj")
asm.run()

from collections import OrderedDict
import re
import linecache

def OperandToSignedBinary(x):
    y = bin(int(x))
    if(y[0] == '0'):
        initial = y[2:]
        padding = 12 - len(initial)
        bin_val = '0'*padding  + initial
    else:
        initial = y[3:]
        padding = 11 - len(initial)
        bin_val = '1' + '0'*padding + initial
    return bin_val
    
def IntToBinary(x):
    y = bin(int(x))
    if(y[0] == '-'):
        initial = y[3:]
        padding = 39 - len(initial)
        bin_val = '1' + '0'*padding + initial
    else:
        initial = y[2:]
        padding = 40 - len(initial)
        bin_val = '0'*padding + initial
    return bin_val
    
def SignedBinaryToInt(binary):
    binary = str(binary)
    if(binary[0] == '0'):
        binary = int(binary) 
        decimal, i, n = 0, 0, 0
        while(binary != 0): 
            dec = binary % 10
            decimal = decimal + dec * pow(2, i) 
            binary = binary//10
            i += 1
        return decimal
    elif(binary[0] == '1'):
        binary = binary[1:]
        binary = int(binary)
        decimal, i, n = 0, 0, 0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return -decimal   

def OpCode(op, address):
    if(op == 'ADD' and address[0] == 'M'):
        return '00000101'

    elif(op == 'STOR' and (',' not in address)):
        return '00100001'

    elif(op == 'LOAD' and address[0:2] == 'M('):
        return '00000001'

    elif(op == 'LOAD' and address[0:2] == '-M'):
        return '00000010'

    elif(op == 'LOAD' and address[0] == '|'):
        return '00000011'

    elif(op == 'LOAD' and address[0:2] == '-|'):
        return '00000100'

    elif(op == 'LOAD' and address == 'MQ'):
        return '00001010'

    elif(op == 'LOAD' and address[:5] == 'MQ,M('):
        return '00001001'

    elif(op == 'ADD' and address[0] == '|'):
        return '00000111'

    elif(op == 'SUB' and address[0] == 'M'):
        return '00000110'

    elif(op == 'SUB' and address[0] == '|'):
        return '00001000'

    elif(op == 'DIV'):
        return '00001100'

    elif(op == 'LSH'):
        return '00010100'

    elif(op == 'RSH'):
        return '00010101'

    elif(op == 'JUMP' and address[-6:-1] == ',0:19'):
        return '00001101'

    elif(op == 'JUMP' and address[-7:-1] == ',20:39'):
        return '00001110'

    elif(op == 'JUMP+' and address[-6:-1] == ',0:19'):
        return '00001111'

    elif(op == 'JUMP+' and address[-7:-1] == ',20:39'):
        return '00010000'

    elif(op == 'MUL'):
        return '00001011'  

    elif(op == 'STOR' and address[-6:-1] == ',8:19'):
        return '00010010'

    elif(op == 'STOR' and address[-7:-1] == ',28:39'):
        return '00010011'
        
    elif(op == 'HALT'):
        return '11111111'

PC = '000000000001'

pattern = "[0-9]+"

output = open("machinecode.txt", "w+")

while True:

    PC = SignedBinaryToInt(PC)

    line = linecache.getline('assembly.txt', PC).rstrip("\n")
    if not line:
        break
    line = line.split(" ")
    temp = PC
    PC = OperandToSignedBinary(PC)

    if(len(line) == 4):
        left_opcode = OpCode(line[0], line[1])
        
        num_left = re.findall(pattern, line[1])

        if(not num_left):
            left_address = '000000000000'

        else:
            left_address = OperandToSignedBinary(int(num_left[0]))
        
        left_instruction = left_opcode + left_address
        
        right_opcode = OpCode(line[2], line[3])
        
        num_right = re.findall(pattern, line[3])

        if(not num_right):
            right_address = '000000000000'

        else:
            right_address = OperandToSignedBinary(int(num_right[0]))

        right_instruction = right_opcode + right_address
        
        instruction = left_instruction + right_instruction
        
        output.write(instruction)
        output.write("\n")
 
        PC = SignedBinaryToInt(PC)
        PC += 1
        PC = OperandToSignedBinary(PC)

    elif(len(line) == 2):
        right_opcode = OpCode(line[0], line[1])
       
        num_right = re.findall(pattern, line[1])

        if(not num_right):
            right_address = '000000000000'

        else:
            right_address = OperandToSignedBinary(num_right[0])

        right_instruction = right_opcode + right_address

        instruction = '00000000000000000000' + right_instruction
        output.write(instruction)
        output.write("\n")
        
        PC = SignedBinaryToInt(PC)
        PC += 1
        PC = OperandToSignedBinary(PC)

    elif(len(line) == 1):
        right_opcode = OpCode(line[0], 'nothing')
        right_address = '000000000000'

        right_instruction = right_opcode + right_address

        instruction = '00000000000000000000' + right_instruction
        output.write(instruction)
        output.write("\n")
         
        PC = SignedBinaryToInt(PC)
        PC += 1
        PC = OperandToSignedBinary(PC)

    elif(len(line)  == 3):
        if(line[2] == 'LSH' or line[2] == 'RSH' or line[2] == 'HALT'):
            left_opcode = OpCode(line[0], line[1])
        
            num_left = re.findall(pattern, line[1])

            if(not num_left):
                left_address = '000000000000'

            else:
                left_address = OperandToSignedBinary(int(num_left[0]))
        
            left_instruction = left_opcode + left_address
            
            right_opcode = OpCode(line[2], 'nothing')
            right_address = '000000000000'
    
            right_instruction = right_opcode + right_address

            instruction = left_instruction + right_instruction
            output.write(instruction)
            output.write("\n")
                
            PC = SignedBinaryToInt(PC)
            PC += 1
            PC = OperandToSignedBinary(PC)
 
        elif(line[0] == 'RSH' or line[0] == 'LSH' or line[0] == 'HALT'):
            left_opcode = OpCode(line[0], 'nothing')
            left_address = '000000000000'
    
            left_instruction = left_opcode + left_address
            
            right_opcode = OpCode(line[1], line[2])
        
            num_right = re.findall(pattern, line[2])

            if(not num_right):
                right_address = '000000000000'

            else:
                right_address = OperandToSignedBinary(int(num_right[0]))
        
            right_instruction = right_opcode + right_address
            
            instruction = left_instruction + right_instruction
            output.write(instruction)
            output.write("\n")
                
            PC = SignedBinaryToInt(PC)
            PC += 1
            PC = OperandToSignedBinary(PC)
            
output.close()   

         
memory = OrderedDict()

def sorted_memory(mem):
    d = dict()
    final_memory = sorted(mem.items(), key=lambda x : x[0])
    for i in final_memory:
        d[i[0]] = i[1]
    return d
    
memory = {'000000000101' : '0000000000000000000000000000000000000001', '000000000110' : '0000000000000000000000000000000000000001'}
memory = sorted_memory(memory)

print("-----------------------------------------------------------------------------------------------INITIAL-----------------------------------------------------------------------------------------------------")

print()
print()

for i, j in memory.items():
    print(i, ":", j)
print()
print()

print("------------------------------------------------------------------------------------------------FINAL------------------------------------------------------------------------------------------------------")

print()
print()

class INST_SET:
    def inst_LOAD(self, mar, AC):
        MBR = memory[mar]
        AC = MBR
        return AC

    def inst_LOAD_NEG(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            AC = '1' + MBR[1:]
        else:
            AC = '0' + MBR[1:]
        return AC

    def inst_LOAD_MOD(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            MBR = MBR
        elif(MBR[0] == '1'):
            MBR = '0' + MBR[1:]
        AC = MBR
        return AC

    def inst_LOAD_NEG_MOD(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            MBR = MBR
        elif(MBR[0] == '1'):
            MBR = '0' + MBR[1:] 
        AC = '1' + MBR[1:]
        return AC

    def inst_ADD(self, mar, AC):
        MBR = SignedBinaryToInt(memory[mar])
        AC = SignedBinaryToInt(AC)
        AC = AC + MBR
        return IntToBinary(AC)

    def inst_STOR(self, mem, mar):
        MBR = AC
        mem[mar] = MBR
        mem = sorted_memory(mem)
 
    def inst_LOAD_MQ(self, MQ, AC):
        AC = MQ
        return AC

    def inst_LOAD_MQ_MX(self, mar, MQ):
        MQ = memory[mar]
        return MQ
    
    def inst_ADD_MOD(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            MBR = MBR
        elif(MBR[0] == '1'):
            MBR = '0' + MBR[1:]
        MBR = SignedBinaryToInt(MBR)
        AC = SignedBinaryToInt(AC)
        AC = AC + MBR
        return IntToBinary(AC)

    def inst_SUB(self, mar, AC):
        MBR = SignedBinaryToInt(memory[mar])
        AC = SignedBinaryToInt(AC)
        AC = AC - MBR
        return IntToBinary(AC)

    def inst_SUB_MOD(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            MBR = MBR
        elif(MBR[0] == '1'):
            MBR = '0' + MBR[1:]
        AC = SignedBinaryToInt(AC)
        MBR = SignedBinaryToInt(MBR)
        AC = AC - MBR
        return IntToBinary(AC)

    def inst_DIV(self, mar, AC, MQ):
        MBR = SignedBinaryToInt(memory[mar])
        MQ = SignedBinaryToInt(MQ)
        AC = SignedBinaryToInt(AC)
        MQ = AC / MBR
        AC = AC % MBR
        AC = IntToBinary(AC)
        MQ = IntToBinary(MQ)
        return AC, MQ

    def inst_LSH(self, AC):
        AC = SignedBinaryToInt(AC)
        AC = AC * 2
        return IntToBinary(AC)

    def inst_RSH(self, AC):
        AC = SignedBinaryToInt(AC)
        AC = AC / 2
        return IntToBinary(AC)

    def inst_JUMP_LEFT(self, PC, X):
        PC = SignedBinaryToInt(PC)
        X = SignedBinaryToInt(X)
        PC = X - 1
        return OperandToSignedBinary(PC)

    def inst_JUMP_RIGHT(self, PC, X):
        PC = SignedBinaryToInt(PC)
        X = SignedBinaryToInt(X)
        PC = X - 1
        return OperandToSignedBinary(PC)

    def inst_JUMP_COND_LEFT(self, PC, X, AC):
        AC = SignedBinaryToInt(AC)
        PC = SignedBinaryToInt(PC)
        X = SignedBinaryToInt(X)
        if (int(AC) >= 0):
            PC = X - 1
        return OperandToSignedBinary(PC)

    def inst_JUMP_COND_RIGHT(self, PC, X, AC):
        AC = SignedBinaryToInt(AC)
        PC = SignedBinaryToInt(PC)
        X = SignedBinaryToInt(X)
        if(int(AC) >= 0):
           PC = X - 1
        return OperandToSignedBinary(PC)

    def inst_MUL(self, mar, MQ, AC):
        product = SignedBinaryToInt(memory[mar])
        MQ = SignedBinaryToInt(MQ)
        mul = product * MQ
        mul = IntToBinary(mul)
        AC = mul[:20]
        MQ = mul[20:]
        return AC, MQ

    def inst_STOR_LEFT(self, mar, AC, memory):
        bin_val = str(memory[mar])[0:8] + str(AC)[28:] + str(memory[mar])[20:40]
        return bin_val

    def inst_STOR_RIGHT(self, mar, AC, memory):
        bin_val = str(memory[mar])[:28] + str(AC)[28:]
        return bin_val

inst = INST_SET()

PC = '000000000001'
AC = int()
MQ = '0000000000000000000000000000000000000000'
right = True

while True:

    MAR = PC
    temp = SignedBinaryToInt(PC)
    
    PC = SignedBinaryToInt(PC)
    line = linecache.getline('machinecode.txt', PC).rstrip("\n")
    PC = OperandToSignedBinary(PC)
    if not line:
        break
    
    memory[MAR] = line
    MBR = memory[MAR]
    
    left_instruction = MBR[0:20]
    right_instruction = MBR[20:40]

    if(left_instruction  != '00000000000000000000'):

        IBR = MBR[20:40]    
        IR  = MBR[:8]
        MAR = MBR[8:20]

    else:
        
        IR = MBR[20:28]
        MAR = MBR[28:40]
       
    if(right and True):

        if(IR == '00000001'):
            AC = inst.inst_LOAD(MAR, AC)   
            
        elif(IR == '11111111'):
            break

        elif(IR == '00000101'):
            AC = inst.inst_ADD(MAR, AC)
            
        elif(IR == '00100001'):
            inst.inst_STOR(memory, MAR)

        elif(IR == '00000111'):
            AC = inst.inst_ADD_MOD(MAR, AC)

        elif(IR == '00000010'):
            AC = inst.inst_LOAD_NEG(MAR, AC)
        
        elif(IR == '00000011'):
            AC = inst.inst_LOAD_MOD(MAR, AC)

        elif(IR == '00000100'): 
            AC = inst.inst_LOAD_NEG_MOD(MAR, AC)

        elif(IR == '00001010'):
            AC = inst.inst_LOAD_MQ(MQ, AC)

        elif(IR == '00001001'):
            MQ = inst.inst_LOAD_MQ_MX(MAR, MQ)

        elif(IR == '00000111'):
            AC = inst.inst_ADD_MOD(MAR, AC)

        elif(IR == '00000110'):
            AC = inst.inst_SUB(MAR, AC)

        elif(IR == '00001000'):
            AC = inst.inst_SUB_MOD(MAR, AC)

        elif(IR == '00001100'):
            AC, MQ = inst.inst_DIV(MAR, AC, MQ)

        elif(IR == '00001011'):
            AC, MQ = inst.inst_MUL(MAR, MQ, AC)

        elif(IR == '00010100'):
            AC = inst.inst_LSH(AC)
  
        elif(IR == '00010101'):
            AC = inst.inst_RSH(AC)

        elif(IR == '00001101'):
            PC = inst.inst_JUMP_LEFT(PC, MAR)

        elif(IR == '00010011'):
            memory[MAR] = inst.inst_STOR_RIGHT(MAR, AC, memory)

        elif(IR == '00010010'):
            memory[MAR] = inst.inst_STOR_LEFT(MAR, AC, memory)
    
        elif(IR == '00001110'):
            PC = inst.inst_JUMP_RIGHT(PC, MAR)
            right = False
            
        elif(IR == '00001111'):
            PC = inst.inst_JUMP_COND_LEFT(PC, MAR, AC)

        elif(IR == '00010000'):
            PC = inst.inst_JUMP_COND_RIGHT(PC, MAR, AC)
            if(SignedBinaryToInt(PC) - temp >= 1):
                right = False
            else:
                right = True
            
    if(right or True):
        right = True     

        if(left_instruction != '00000000000000000000'):
            IR = IBR[0:8]
            MAR = IBR[8:20]
          
        if(IR == '00000001'):
            AC = inst.inst_LOAD(MAR, AC)   
            
        elif(IR == '11111111'):
            break

        elif(IR == '00000101'):
            AC = inst.inst_ADD(MAR, AC)

        elif(IR == '00100001'):
            inst.inst_STOR(memory, MAR)

        elif(IR == '00000111'):
            AC = inst.inst_ADD_MOD(MAR, AC)

        elif(IR == '00000010'):
            AC = inst.inst_LOAD_NEG(MAR, AC)
        
        elif(IR == '00000011'):
            AC = inst.inst_LOAD_MOD(MAR, AC)

        elif(IR == '00000100'): 
            AC = inst.inst_LOAD_NEG_MOD(MAR, AC)

        elif(IR == '00001010'):
            AC = inst.inst_LOAD_MQ(MQ, AC)

        elif(IR == '00001001'):
            MQ = inst.inst_LOAD_MQ_MX(MAR, MQ)

        elif(IR == '00000111'):
            AC = inst.inst_ADD_MOD(MAR, AC)

        elif(IR == '00000110'):
            AC = inst.inst_SUB(MAR, AC)

        elif(IR == '00001000'):
            AC = inst.inst_SUB_MOD(MAR, AC)
 
        elif(IR == '00001100'):
            AC, MQ = inst.inst_DIV(MAR, AC, MQ)

        elif(IR == '00001011'):
            AC, MQ = inst.inst_MUL(MAR, MQ, AC)
 
        elif(IR == '00010100'):
            AC = inst.inst_LSH(AC)
    
        elif(IR == '00010101'):
            AC = inst.inst_RSH(AC)

        elif(IR == '00010011'):
            memory[MAR] = inst.inst_STOR_RIGHT(MAR, AC, memory)

        elif(IR == '00010010'):
            memory[MAR] = inst.inst_STOR_LEFT(MAR, AC, memory)
 
        elif(IR == '00001101'):
            PC = inst.inst_JUMP_LEFT(PC, MAR)
  
        elif(IR == '00001110'):
            PC = inst.inst_JUMP_RIGHT(PC, MAR)
            right = False

        elif(IR == '00001111'):
            PC = inst.inst_JUMP_COND_LEFT(PC, MAR, AC)
               
        elif(IR == '00010000'):
            PC = inst.inst_JUMP_COND_RIGHT(PC, MAR, AC)
            if(SignedBinaryToInt(PC) - temp >= 1):
                right = False
            else:
                right = True
 
    PC = SignedBinaryToInt(PC)
    PC += 1
    PC = OperandToSignedBinary(PC)
       
memory = sorted_memory(memory)
for i, j in memory.items():
    print(i, ":", j)
print()
print()

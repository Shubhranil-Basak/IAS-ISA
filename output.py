
def display(output: dict):
    oct_color = [31, 32, 33, 34, 35, 36, 37]
    cop = oct_color.copy()
    for i in output:
        code = cop.pop()
        print(f'\033[1;{code};50m {i} -> \033[0;0m', end="")
        print(f'\033[4;{code};50m {output[i]} \033[0;0m')

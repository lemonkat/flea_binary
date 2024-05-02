from Compiler import Line, Blueprint, Compiler
from Binary import to_binary, to_int

Compiler.load_file("blueprints")

Compiler.compile("""DEFINE HALF_ADDER A B
SET S TO XOR A B
SET C TO AND A B
DEL A B
ORDER S C
END
DEFINE FULL_ADDER A B C
SET S C_OUT TO HALF_ADDER A B
SET S C_OUT_2 TO HALF_ADDER C S
SET C TO OR C_OUT C_OUT_2
DEL C_OUT C_OUT_2 A B
ORDER C S
END
DEFINE MAIN A3 A2 A1 A0 B3 B2 B1 B0
SET C TO FALSE
SET C S0 TO FULL_ADDER A0 B0 C
DEL A0 B0
SET C S1 TO FULL_ADDER A1 B1 C
DEL A1 B1
SET C S2 TO FULL_ADDER A2 B2 C
DEL A2 B2
SET S4 S3 TO FULL_ADDER A3 B3 C
DEL A3 B3 C
ORDER S4 S3 S2 S1 S0
GAP
END""")

def add(a:int, b:int) -> int:
	return to_int(Compiler.run(to_binary(a, length = 4)[0:5] + to_binary(b, length = 4)[0:5], 10, {" ":"#fff", "1":"#0f0","2":"#00f","3":"#f00","4":"#f0f","5":"#ff0","6":"#bde", "7":"#0ff","8":"#a2f"}, "#000", wait = 0.01, jump = 1))

while True:
	print(add(int(input("Number 1: ")), int(input("Number 2: "))))

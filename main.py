from sys import argv
from subprocess import call
from subprocess import *
from assembler import *


def choice():
    p2=check_output(["echo", "ENTER YOUR CHOICE:"], universal_newlines=True)
    print(p2)
    p3=check_output(["echo", "\t st \t Display Symbol Table"], universal_newlines=True)
    print(p3)
    p4=check_output(["echo", "\t lt \t Display Literal Table"], universal_newlines=True)
    print(p4)
    p5=check_output(["echo", "\t ic \t Display Intermediate Code"], universal_newlines=True)
    print(p5)
    p6=check_output(["echo", "\t lst \t Display lst Code"], universal_newlines=True)
    print(p6)
    p6=check_output(["echo", "\t obj \t Display object Code"], universal_newlines=True)
    print(p6)
def choice_display(x):
    if x=='st':
        call(["less","symtab_output.txt"])
    if x=='lt':
        call(["less","literal_output.txt"])
    if x=='ic':
        call(["less","intermediate_op.txt"])
    if x=='lst':
        call(["less","lstfile.txt"])
    if x=='obj':
        call(["less","objectop.txt"])
        
if __name__ == "__main__":
    i=argv[1]
    choice_display(i)
    choice()
    exit()
    
   
        
    



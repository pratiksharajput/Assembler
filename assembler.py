from sys import *
#---------------Symboltable code--------------------
def symtab(f):
    line=[]
    sym=[]
    define=[]
    undefine=[]
    size=[]
    value=[]
    stype=[]
    label=[]
    addl=[]
    undefine_label=['jmp','je','jl','jg','jge','jle']
    fn=open(f,"r")
    l1=fn.readline()
    sl=l1.split()
    ln=len(sl)
    add=00000000
    l=1
    while(l1!=""):
        for i in range(ln):
            if(sl[i]=='dd'):
                line.append(l)
                sym.append(sl[i-1])
                s=sl[i+1].split(",")
                sz=len(s)*4
                define.append('D')
                size.append(sz)
                value.append(sl[i+1])
                stype.append('int')
                addl.append(add)
                add+=sz
                
                
            if(sl[i]=='db'):
                line.append(l)
                sym.append(sl[i-1])
                vl=[]
                for j in range(i+1,ln):
                    if(sl[j]!='0'):
                        vl.append(sl[j])
                s2=",".join(vl)
                s3=s2.split(',')
                s4=[]
                for i in range(len(s3)):
                    if(s3[i]=='0'):
                        for j in range(i):
                            s4.append(s3[j])
                s5=','.join(s4)
                s6=s5.replace(","," ")
                s7=s6.replace('"','')

                sz=len(s7)
                value.append(s7)
                define.append('D')
                size.append(sz)
                stype.append('byte')
                addl.append(add)
                add=00000000
    
               
            if(sl[i]=='dw'):
                line.append(l)
                sym.append(sl[i-1])
                s=sl[i+1].split(",")
                sz=len(s)*2
                define.append('D')
                size.append(sz)
                value.append(sl[i+1])
                stype.append('word')
                addl.append(add)
                add+=sz
               
            if(sl[i]=='resb'):
                line.append(l)
                sym.append(sl[i-1])
                define.append('D')
                size.append(sl[i+1])
                value.append('-')
                stype.append("Reserved Byte")
                addl.append(add)
                s1=int(sl[i+1])
                add+=s1
               
            if(sl[i]=='resd'):
                line.append(l)
                sym.append(sl[i-1])
                define.append('D')
                size.append(sl[i+1])
                value.append('-')
                stype.append("Reserved integer")
                addl.append(add)
                s1=int(sl[i+1])
                add+=s1*4
               
            if(sl[i]=='global'):
                line.append(l)
                sym.append(sl[i+1])
                define.append('U')
                size.append('-')
                value.append('-')
                stype.append("Function")
                addl.append('')

            if(sl[i]=='extern'):
                line.append(l)
                sym.append(sl[i+1])
                define.append('D')
                size.append('-')
                value.append('-')
                stype.append("Function")
                addl.append('')

            if sl[i].endswith(":"):
                s=sl[i]
                s1=s[:-1]
                if s1 not in sym:
                    line.append(l)
                    sym.append(s1)
                    define.append('U')
                    size.append('-')
                    value.append('-')
                    stype.append("Label")
                    addl.append('')
                else:
                     exit
                
            if sl[i] in undefine_label:
                if sl[i+1] not in sym:
                    line.append(l)
                    sym.append(sl[i+1])
                    define.append('U')
                    size.append('-')
                    value.append('-')
                    stype.append("Label")
                    addl.append('')
                else:
                    exit
                              
        l1=fn.readline()
        sl=l1.split()
        ln=len(sl)
        l+=1   
    fw=open("symbol.txt","w")
    cnt=1
    for i in range(len(sym)):
        fw.write(str(sym[i])+"\t"+str("sym")+str(cnt)+"\t"+str(addl[i]).zfill(8)+"\t"+str(value[i])+"\n")
        cnt+=1
    fw=open("symtab_output.txt","w")
    fw.write("LineNo"+"\t"+"Symbol"+"\t"+"D/U"+"\t"+"Size"+"\t"+"Type"+"\t\t\t"+"Value"+"\t\t\t"+"Address"+"\n")
    for i in range(len(line)):
        fw.write(str(line[i])+"\t"+str(sym[i])+"\t"+str(define[i])+"\t"+str(size[i])+"\t"+str(stype[i])+"\t\t\t"+str(value[i])+"\t\t\t"+str(addl[i]).zfill(8)+"\n")
#--------------------------Literal table code-------------------------
def lit(f):
    line_no=[]
    literal=[]
    hex_lit=[]
    fn=open(f,"r+")
    l1=fn.readline()
    sl=l1.split()
    ln=len(sl)
    cnt=1
    while(l1!=""):
        for i in range(ln):
            if(sl[i]=='mov'):
                s=sl[i+1].split(",")
                for j in range(len(s)):
                    if(s[j].isdigit()):
                        literal.append(s[j])
                        line_no.append(cnt)
                       
            if(sl[i]=='add'):
                s=sl[i+1].split(",")
                for j in range(len(s)):
                    if(s[j].isdigit()):
                        literal.append(s[j])
                        line_no.append(cnt)
                       
        l1=fn.readline()
        sl=l1.split()
        ln=len(sl)
        cnt+=1   
    fw=open("literal_output.txt","w")
    fw.write("LitNo"+"\t"+"Line"+"\t"+"Literal  "+"\t"+"HexLiteral"+"\n")
    p=1
    for i in range(len(literal)):
        fw.write(str(p)+"\t"+str(line_no[i])+"\t"+str(literal[i])+"\t\t"+str(hex(int(literal[i])))+"\n")
        p+=1

    fw=open("litral.txt","w")
    for i in range(len(literal)):
        fw.write(str(literal[i])+"\t"+"lit#"+str(literal[i])+"\n")
#-------------Intermediate code---------------------------------------
def transform(f1,f2,f3,f4):
    arr=["eax","ebx","ecx","edx","ebp","esp","esi","edi"]#32bit register
    arr1=["ax","bx","cx","dx"]#16bit register
    arr2=["ah","al","bh","bl","ch","cl","dh","dl"]#8bit register
    address=00000000
    fl1=open(f1,"r")#add.asm
    fl2=open(f2,"r")#symbol.txt
    fl3=open(f3,"r")#literal.txt
    fl4=open(f4,"r")#opregister.txt
    ln1=fl1.readline()
    ln2=fl2.read()
    ln3=fl3.read()
    ln4=fl4.read()
    
    ls1=ln1.split()
    ls2=ln2.split()
    ls3=ln3.split()
    ls4=ln4.split()

    l1=len(ls1)
    l2=len(ls2)
    l3=len(ls3)
    l4=len(ls4)
    fw=open("intermediate_op.txt","w")
    cnt=0
    fw.write("--------------------Intermediate Code---------------------\n\n")
    while(ln1!=""):
        cnt+=1
        for i in range(l1):
            if (ls1[i]=="mov"):
                ls=ls1[i+1].split(",")
                #for mov eax,a
                if(ls[0] in arr and ls[1] in ls2):#for 32 bit
                    op="op01"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            r=ls4[k+1]
                    for j in range(l2):
                        if ls2[j]==ls[1]:
                                n=ls2[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                elif(ls[0] in arr1 and ls[1] in ls2):#for 16 bit
                    op="op02"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            r=ls4[k+1]
                    for j in range(l2):
                        if ls2[j]==ls[1]:
                                n=ls2[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                else:                            #for 8 bit
                    if(ls[0] in arr2 and ls[1] in ls2):
                        op="op03"
                        for k in range(l4):
                            if ls4[k]==ls[0]:
                                r=ls4[k+1]
                        for j in range(l2):
                            if ls2[j]==ls[1]:
                                n=ls2[j+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                        address+=6
                #for mov a,eax       
                if(ls[0] in ls2 and ls[1] in arr): # for 32 bit
                    op="op04"
                    for k in range(l2):
                        if ls2[k]==ls[0]:
                            r=ls2[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                elif(ls[0] in ls2 and ls[1] in arr1):# for 16 bit
                    op="op05"
                    for k in range(l2):
                        if ls2[k]==ls[0]:
                            r=ls2[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                else:
                    if(ls[0] in ls2 and ls[1] in arr2):#for 8 bit
                        op="op06"
                        for k in range(l2):
                            if ls2[k]==ls[0]:
                                r=ls2[k+1]
                        for j in range(l4):
                            if ls4[j]==ls[1]:
                                n=ls4[j+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                        address+=6
                        
                #for mov eax,3
                if( ls[0] in arr and ls[1] in ls3):#for 32 bit
                    op="op07"
                    for j in range(l4):
                        if ls4[j]==ls[0]:
                            r=ls4[j+1]
                    for k in range(l3):
                        if ls3[k]==ls[1]:
                            n=ls3[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                elif( ls[0] in arr1 and ls[1] in ls3):#for 16 bit
                    op="op08"
                    for j in range(l4):
                        if ls4[j]==ls[0]:
                            r=ls4[j+1]
                    for k in range(l3):
                        if ls3[k]==ls[1]:
                            n=ls3[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                else:
                    if( ls[0] in arr2 and ls[1] in ls3):#for 8 bit
                        op="op09"
                        for j in range(l4):
                            if ls4[j]==ls[0]:
                                r=ls4[j+1]
                        for k in range(l3):
                            if ls3[k]==ls[1]:
                                n=ls3[k+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                        address+=6
                #for mov eax,ebx
                if(ls[0] in arr and ls[1] in arr): #for 32 bit
                    op="op10"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                elif(ls[0] in arr1 and ls[1] in arr1):# for 16 bit
                    op="op11"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                else:
                    if(ls[0] in arr2 and ls[1] in arr2):# for 8bit
                        op="op12"
                        for k in range(l4):
                            if ls4[k]==ls[0]:
                                n1=ls4[k+1]
                        for j in range(l4):
                            if ls4[j]==ls[1]:
                                n2=ls4[j+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                        address+=3

            if (ls1[i]=="add"):
                ls=ls1[i+1].split(",")
                #for add eax,3
                if( ls[0] in arr and ls[1] in ls3):#for 32 bit
                    op="op13"
                    for j in range(l4):
                        if ls4[j]==ls[0]:
                            r=ls4[j+1]
                    for k in range(l3):
                        if ls3[k]==ls[1]:
                            n=ls3[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                elif( ls[0] in arr1 and ls[1] in ls3):#for 16 bit
                    op="op14"
                    for j in range(l4):
                        if ls4[j]==ls[0]:
                            r=ls4[j+1]
                    for k in range(l3):
                        if ls3[k]==ls[1]:
                            n=ls3[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                else:
                    if( ls[0] in arr2 and ls[1] in ls3):#for 8 bit
                        op="op15"
                        for j in range(l4):
                            if ls4[j]==ls[0]:
                                r=ls4[j+1]
                        for k in range(l3):
                            if ls3[k]==ls[1]:
                                n=ls3[k+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                        address+=6
                #for add eax,ebx
                if(ls[0] in arr and ls[1] in arr):#for 32 bit
                    op="op16"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                elif(ls[0] in arr1 and ls[1] in arr1):#for 16 bit
                    op="op17"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                else:
                    if(ls[0] in arr2 and ls[1] in arr2): #for 8 bit
                        op="op18"
                        for k in range(l4):
                            if ls4[k]==ls[0]:
                                n1=ls4[k+1]
                        for j in range(l4):
                            if ls4[j]==ls[1]:
                                n2=ls4[j+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                        address+=3
            if (ls1[i]=="sub"):
                ls=ls1[i+1].split(",")
                #for sub eax,3
                if( ls[0] in arr and ls[1] in ls3):#for 32 bit
                    op="op19"
                    for j in range(l4):
                        if ls4[j]==ls[0]:
                            r=ls4[j+1]
                    for k in range(l3):
                        if ls3[k]==ls[1]:
                            n=ls3[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                elif( ls[0] in arr1 and ls[1] in ls3):#for 16 bit
                    op="op20"
                    for j in range(l4):
                        if ls4[j]==ls[0]:
                            r=ls4[j+1]
                    for k in range(l3):
                        if ls3[k]==ls[1]:
                            n=ls3[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                    address+=6
                else:
                    if( ls[0] in arr2 and ls[1] in ls3):  #for 8 bit
                        op="op21"
                        for j in range(l4):
                            if ls4[j]==ls[0]:
                                r=ls4[j+1]
                        for k in range(l3):
                            if ls3[k]==ls[1]:
                                n=ls3[k+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(r)+" "+str(n)+"\n")
                        address+=6
                #for sub eax,ebx
                if(ls[0] in arr and ls[1] in arr):#for 32 bit
                    op="op22"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                elif(ls[0] in arr1 and ls[1] in arr1):#for 16 bit
                    op="op23"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                else:
                    if(ls[0] in arr2 and ls[1] in arr2):#for 8 bit
                        op="op24"
                        for k in range(l4):
                            if ls4[k]==ls[0]:
                                n1=ls4[k+1]
                        for j in range(l4):
                            if ls4[j]==ls[1]:
                                n2=ls4[j+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                        address+=3
            #jmp instruction
            if(ls1[i]=="jmp"):
                op="op25"
                for k in range(l2):
                    if ls1[i+1]==ls2[k]:
                        n=ls2[k+1]
                        
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            #Mul instruction
            if(ls1[i]=="mul"):
                if(ls1[i+1] in arr):#32 bit
                    op="op26"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                elif(ls1[i+1] in arr1):#16 bit
                    op="op27"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                else:
                    if(ls1[i+1] in arr2):#8 bit
                        op="op28"
                        for k in range(l4):
                            if ls4[k]==ls1[i+1]:
                                n=ls4[k+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                        address+=2
            #DIV instruction
            if(ls1[i]=="div"):
                if(ls1[i+1] in arr):#32 bit
                    op="op29"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                elif(ls1[i+1] in arr1):#16 bit
                    op="op30"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                else:
                    if(ls1[i+1] in arr2):#8 bit
                        op="op31"
                        for k in range(l4):
                            if ls4[k]==ls1[i+1]:
                                n=ls4[k+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                        address+=2
            #INC instruction
            if(ls1[i]=="inc"):
                #INC eax
                if(ls1[i+1] in arr):#32 bit
                    op="op32"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                elif(ls1[i+1] in arr1):#16 bit
                    op="op33"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                else:
                    if(ls1[i+1] in arr2):#8 bit
                        op="op34"
                        for k in range(l4):
                            if ls4[k]==ls1[i+1]:
                                n=ls4[k+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                        address+=2
                #INC a
                if(ls1[i+1] in ls2):#32 bit
                    op="op35"
                    for k in range(l2):
                        if ls2[k]==ls1[i+1]:
                            n=ls2[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                
            #DEC instruction
            if(ls1[i]=="dec"):
                #dec eax
                if(ls1[i+1] in arr):#32 bit
                    op="op36"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                elif(ls1[i+1] in arr1):#16 bit
                    op="op37"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                else:
                    if(ls1[i+1] in arr2):#8 bit
                        op="op38"
                        for k in range(l4):
                            if ls4[k]==ls1[i+1]:
                                n=ls4[k+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                        address+=2
                #DEC a
                if(ls1[i+1] in ls2):#32 bit
                    op="op39"
                    for k in range(l2):
                        if ls2[k]==ls1[i+1]:
                            n=ls2[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
            #call instruction
            if(ls1[i]=="call"):
                op="op40"
                for k in range(l2):
                    if ls2[k]==ls1[i+1]:
                        n=ls2[k+1]
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            #Push instruction
            if(ls1[i]=="push"):
                if(ls1[i+1] in arr):#32 bit
                    op="op41"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                elif(ls1[i+1] in arr1):#16 bit
                    op="op42"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                else:
                    if(ls1[i+1] in arr2):#8 bit
                        op="op43"
                        for k in range(l4):
                            if ls4[k]==ls1[i+1]:
                                n=ls4[k+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                        address+=2
                if(ls1[i+1] in ls2):#if symbol
                    op="op44"
                    for k in range(l2):
                        if ls2[k]==ls1[i+1]:
                            n=ls2[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
            #Pop instruction
            if(ls1[i]=="pop"):
                if(ls1[i+1] in arr):#32 bit
                    op="op45"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                elif(ls1[i+1] in arr1):#16 bit
                    op="op46"
                    for k in range(l4):
                        if ls4[k]==ls1[i+1]:
                            n=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                    address+=2
                else:
                    if(ls1[i+1] in arr2):#8 bit
                        op="op47"
                        for k in range(l4):
                            if ls4[k]==ls1[i+1]:
                                n=ls4[k+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                        address+=2

            #for XOR eax,ebx
            if(ls1[i]=='xor'):
                ls=ls1[i+1].split(",")
                if(ls[0] in arr and ls[1] in arr): #for 32 bit
                    op="op48"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                elif(ls[0] in arr1 and ls[1] in arr1):# for 16 bit
                    op="op49"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                else:
                    if(ls[0] in arr2 and ls[1] in arr2):# for 8bit
                        op="op50"
                        for k in range(l4):
                            if ls4[k]==ls[0]:
                                n1=ls4[k+1]
                        for j in range(l4):
                            if ls4[j]==ls[1]:
                                n2=ls4[j+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                        address+=3

            #for compare instruction
            if(ls1[i]=='cmp'):
                ls=ls1[i+1].split(",")
                if(ls[0] in arr and ls[1] in arr): #for 32 bit
                    op="op51"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                elif(ls[0] in arr1 and ls[1] in arr1):# for 16 bit
                    op="op52"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    for j in range(l4):
                        if ls4[j]==ls[1]:
                            n2=ls4[j+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                    address+=3
                else:
                    if(ls[0] in arr2 and ls[1] in arr2):# for 8bit
                        op="op53"
                        for k in range(l4):
                            if ls4[k]==ls[0]:
                                n1=ls4[k+1]
                        for j in range(l4):
                            if ls4[j]==ls[1]:
                                n2=ls4[j+1]
                        fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+str(n2)+"\n")
                        address+=3
                if(ls[0] in arr and ls[1].isdigit()): #cmp eax,0
                    op="op54"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+" " +"\n")
                    address+=3
                if(ls[0] in arr1 and ls[1].isdigit()): #cmp ax,0
                    op="op55"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+" "+"\n")
                    address+=3
                if(ls[0] in arr2 and ls[1].isdigit()): #cmp ah,0
                    op="op56"
                    for k in range(l4):
                        if ls4[k]==ls[0]:
                            n1=ls4[k+1]
                    fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n1)+" "+" "+"\n")
                    address+=3

            #je instruction
            if(ls1[i]=="je"):
                op="op57"
                for k in range(l2):
                    if ls1[i+1]==ls2[k]:
                        n=ls2[k+1]
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            #jz instruction
            if(ls1[i]=="jz"):
                op="op58"
                for k in range(l2):
                    if ls1[i+1]==ls2[k]:
                        n=ls2[k+1]
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            #jne instruction
            if(ls1[i]=="jne"):
                op="op59"
                for k in range(l2):
                    if ls1[i+1]==ls2[k]:
                        n=ls2[k+1]       
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            #jg instruction
            if(ls1[i]=="jg"):
                op="op60"
                for k in range(l2):
                    if ls1[i+1]==ls2[k]:
                        n=ls2[k+1]      
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            #jge instruction
            if(ls1[i]=="jge"):
                op="op61"
                for k in range(l2):
                    if ls1[i+1]==ls2[k]:
                        n=ls2[k+1]      
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            #jl instruction
            if(ls1[i]=="jl"):
                op="op62"
                for k in range(l2):
                    if ls1[i+1]==ls2[k]:
                        n=ls2[k+1]     
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            #jle instruction
            if(ls1[i]=="jle"):
                op="op63"
                for k in range(l2):
                    if ls1[i+1]==ls2[k]:
                        n=ls2[k+1]
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            #Movsb instruction
            if(ls1[i]=='rep' and ls1[i+1]=='movsb'):
                op="op64"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='rep' and ls1[i+1]=='movsw'):
                op="op65"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='rep' and ls1[i+1]=='movsd'):
                op="op66"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='movsb'):
                op="op67"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='movsw'):
                op="op68"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='movsd'):
                op="op69"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='movsb'):
                op="op70"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='movsw'):
                op="op71"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='movsd'):
                op="op72"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            #stosb instruction
            if(ls1[i]=='rep' and ls1[i+1]=='stosb'):
                op="op73"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='rep' and ls1[i+1]=='stosw'):
                op="op74"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='rep' and ls1[i+1]=='stosd'):
                op="op75"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='stosb'):
                op="op76"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='stosw'):
                op="op77"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='stosd'):
                op="op78"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='stosb'):
                op="op79"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='stosw'):
                op="op80"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='stosd'):
                op="op81"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            #cmpsb instruction
            if(ls1[i]=='rep' and ls1[i+1]=='cmpsb'):
                op="op82"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='rep' and ls1[i+1]=='cmpsw'):
                op="op83"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='rep' and ls1[i+1]=='cmpsd'):
                op="op84"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='cmpsb'):
                op="op85"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='cmpsw'):
                op="op86"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='cmpsd'):
                op="op87"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='cmpsb'):
                op="op88"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='cmpsw'):
                op="op89"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='cmpsd'):
                op="op90"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            #lodsb instruction
            if(ls1[i]=='rep' and ls1[i+1]=='lodsb'):
                op="op91"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='rep' and ls1[i+1]=='lodsw'):
                op="op92"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='rep' and ls1[i+1]=='lodsd'):
                op="op93"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='lodsb'):
                op="op94"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='lodsw'):
                op="op95"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repz' and ls1[i+1]=='lodsd'):
                op="op96"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='lodsb'):
                op="op97"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repnz' and ls1[i+1]=='lodsw'):
                op="op98"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            if(ls1[i]=='repne' and ls1[i+1]=='lodsd'):
                op="op99"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            #cld instruction
            if(ls1[i]=="cld"):
                op="op100"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            #std instruction
            if(ls1[i]=="std"):
                op="op101"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            #ret instruction
            if(ls1[i]=="ret"):
                op="op102"
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+"\n")
                address+=2
            #loop instruction
            if(ls1[i]=='loop'):
                op="op103"
                for k in range(l2):
                    if ls2[k]==ls1[i+1]:
                        n=ls2[k+1]
                fw.write(str(cnt)+"\t"+str(address).zfill(8)+"\t"+str(op)+" "+str(n)+" "+" "+"\n")
                address+=2
            
        ln1=fl1.readline()
        ls1=ln1.split()
        l1=len(ls1)



def replace_x(s):
    for i in s:
        if(i=='x'):
            s=s.replace(i,'0')
    return s.upper()
def cal_add(s):
    cn=0
    ls=['[',']','(',')']
    for i in s:
        if i not in ls:
            cn+=1
        else:
            exit
        c=cn/2
    return c

            
#-------------------------------lst file Code-------------------------------            

def replace_x(s):
    for i in s:
        if(i=='x'):
            s=s.replace(i,'0')
    return s.upper()
def cal_add(s):
    cn=0
    ls=['[',']','(',')']
    for i in s:
        if i not in ls:
            cn+=1
        else:
            exit
        c=cn/2
    return c

            
            
def lst_code(f1,f2,f3,f4,f5,f6):
    arr=["eax","ebx","ecx","edx","ebp","esp","esi","edi"]#32bit register
    arr1=["ax","bx","cx","dx"]#16bit register
    arr2=["ah","al","bh","bl","ch","cl","dh","dl"]#8bit register
    fn1=open(f1,"r")#add.asm
    fn2=open(f2,"r")#symbol.txt
    fn3=open(f3,"r")#literal.txt
    fn4=open(f4,"r")#modregister.txt
    fn5=open(f5,"r")#intermediate code op
    fn6=open(f6,"r")#opcode.txt
    ln1=fn1.readline()
    ln2=fn2.read()
    ln3=fn3.read()
    ln4=fn4.read()
    ln5=fn5.read()
    ln6=fn6.read()

    ls1=ln1.split()
    ls2=ln2.split()
    ls3=ln3.split()
    ls4=ln4.split()
    ls5=ln5.split()
    ls6=ln6.split()

    l1=len(ls1)
    l2=len(ls2)
    l3=len(ls3)
    l4=len(ls4)
    l5=len(ls5)
    l6=len(ls6)
    fw=open("lstfile.txt","w")
    cnt=0
    add1=0000000
    while(ln1!=""):
        cnt+=1
        if(ls1==[]):
            fw.write(str(cnt)+"\n")
        for i in range(l1):
            if(ls1[i]=="section" or ls1[i]=="global" or ls1[i]=="main:" or ls1[i]=="extern"):
                fw.write(str(cnt)+"\t"+"          "+"\t"+"         "+"\t"+str(ln1))
            if(ls1[i]=="dd"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        add=ls2[j+2]
                oc=replace_x(hex(int(ls1[i+1])))
                fw.write(str(cnt)+"\t"+str(add)+"\t"+str(oc).zfill(8)+"\t"+str(ln1))
            if(ls1[i]=="db"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        add=ls2[j+2] 
                oc=replace_x(hex(10)+hex(0))
                fw.write(str(cnt)+"\t"+str(add)+"\t"+str(oc).zfill(8)+"\t"+str(ln1))
            if(ls1[i]=="resb"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        add=ls2[j+2]
                oc=replace_x(hex(int(ls1[i+1])))
                fw.write(str(cnt)+"\t"+str(add)+"\t"+str('<res')+" "+str(oc).zfill(8)+">"+"\t"+str(ln1))
            if(ls1[i]=="resd"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        add=ls2[j+2]
                l=int(ls1[i+1])*4
                oc=replace_x(hex(int(l)))
                fw.write(str(cnt)+"\t"+str(add)+"\t"+str('<res')+" "+str(oc).zfill(8)+">"+"\t"+str(ln1))
            if(ls1[i]=="mov"):
                ls=ls1[i+1].split(",")
                #for mov eax,a
                if(ls[0] in arr and ls[1] in ls2):
                    for j in range(l2):
                        if ls[1]==ls2[j]:
                            s1=ls2[j+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+"["+str(s1)+"]"
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #16 bit mov ax,a
                if(ls[0] in arr1 and ls[1] in ls2):
                    for j in range(l2):
                        if ls[1]==ls2[j]:
                            s1=ls2[j+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+"["+str(s1)+"]"
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for 8 bit mov al,a
                if(ls[0] in arr2 and ls[1] in ls2):
                    for j in range(l2):
                        if ls[1]==ls2[j]:
                            s1=ls2[j+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+"["+str(s1)+"]"
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for mov eax,3
                if(ls[0] in arr and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for mov ax,3
                if(ls[0] in arr1 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for mov al,3
                if(ls[0] in arr2 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for mov eax,ebx 32 bit
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for mov ax,bx
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr1:
                        if x==ls[0]:
                            r1=x
                    for y in arr1:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for mov ah,bh
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr2:
                        if x==ls[0]:
                            r1=x
                    for y in arr2:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
            if(ls1[i]=="add"):
                ls=ls1[i+1].split(",")
                # for add eax,ebx
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for add ax,bx
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr1:
                        if x==ls[0]:
                            r1=x
                    for y in arr1:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for add ah,bh
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr2:
                        if x==ls[0]:
                            r1=x
                    for y in arr2:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for add esi,3
                if(ls[0] in arr and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                # for add ah,3
                if(ls[0] in arr1 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for add al,3
                if(ls[0] in arr2 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)

            if(ls1[i]=="sub"):
                ls=ls1[i+1].split(",")
                # for sub eax,ebx
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for sub ax,bx
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr1:
                        if x==ls[0]:
                            r1=x
                    for y in arr1:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for sub ah,bh
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr2:
                        if x==ls[0]:
                            r1=x
                    for y in arr2:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for sub esi,3
                if(ls[0] in arr and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                # for sub ah,3
                if(ls[0] in arr1 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for sub al,3
                if(ls[0] in arr2 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
            # jmp instruction
            if(ls1[i]=="jmp"):
                for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                add1=add1+cal_add(obj)
            # mul  instruction
            if(ls1[i]=="mul"):
                for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1+'E3'
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                add1=add1+cal_add(obj)
            # div instruction
            if(ls1[i]=="div"):
                for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1+'F3'
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                add1=add1+cal_add(obj)
            #inc instruction
            if(ls1[i]=='inc'):
                if(ls1[i+1] in arr):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                if(ls1[i+1] in arr1):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj='66'+p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                if(ls1[i+1] in arr2):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+'C0'
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)

            #dec instruction
            if(ls1[i]=='dec'):
                if(ls1[i+1] in arr):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                if(ls1[i+1] in arr1):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj='66'+p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                if(ls1[i+1] in arr2):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+'C8'
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)

            if(ls1[i]=="xor"):
                ls=ls1[i+1].split(",")
                # for xor eax,ebx
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for xor ax,bx
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr1:
                        if x==ls[0]:
                            r1=x
                    for y in arr1:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for xor ah,bh
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr2:
                        if x==ls[0]:
                            r1=x
                    for y in arr2:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)

            if(ls1[i]=="cmp"):
                ls=ls1[i+1].split(",")
                # for cmp eax,ebx
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for cmp ax,bx
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr1:
                        if x==ls[0]:
                            r1=x
                    for y in arr1:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for cmp ah,bh
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr2:
                        if x==ls[0]:
                            r1=x
                    for y in arr2:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
                #for cmp eax,3
                if(ls[0] in (arr or arr1 or arr2) and ls[1].isdigit()):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+ls[1].zfill(2)
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t"+str(ln1))
                    add1=add1+cal_add(obj)
            # je instruction
            if(ls1[i]=="je"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
            # jz instruction
            if(ls1[i]=="jz"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
            # jne instruction
            if(ls1[i]=="jne"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
            # jg instruction
            if(ls1[i]=="jg"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
            # jge instruction
            if(ls1[i]=="jge"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
            # jl instruction
            if(ls1[i]=="jl"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
            # jle instruction
            if(ls1[i]=="jle"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
            #push instruction
            if(ls1[i]=="push"):
                if(ls1[i+1] in arr):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                if(ls1[i+1] in ls2):
                    for k in range(l2):
                        if ls2[k]==ls1[i+1]:
                            s1=ls2[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+"["+s1+"]"
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
            #call instruction
            if(ls1[i]=="call"):
                if(ls1[i+1]=="printf"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+'('+str(0).zfill(8)+')'
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
            #rep movsb/stosb/cmpsb/lodsb instruction
            if(ls1[i]=="rep"):
                if(ls1[i+1]=="movsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="movsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="movsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="stosb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="stosw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="stosd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="cmpsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="cmpsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="cmpsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                
                elif(ls1[i+1]=="lodsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="lodsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                else:
                    if(ls1[i+1]=="lodsd"):
                        for k in range(l5):
                            if str(cnt) == ls5[k]:
                                p=ls5[k+2]
                        for l in range(l6):
                            if str(p)==ls6[l]:
                                p1=ls6[l+1]
                        obj=p1
                        fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                        add1=add1+cal_add(obj)

            #repz movsb/stosb/cmpsb/lodsb instruction
            if(ls1[i]=="repz"):
                if(ls1[i+1]=="movsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="movsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="movsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="stosb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="stosw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="stosd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="cmpsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="cmpsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="cmpsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                
                elif(ls1[i+1]=="lodsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="lodsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                else:
                    if(ls1[i+1]=="lodsd"):
                        for k in range(l5):
                            if str(cnt) == ls5[k]:
                                p=ls5[k+2]
                        for l in range(l6):
                            if str(p)==ls6[l]:
                                p1=ls6[l+1]
                        obj=p1
                        fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                        add1=add1+cal_add(obj)
            #repnz movsb/stosb/cmpsb/lodsb instruction
            if(ls1[i]=="repnz"):
                if(ls1[i+1]=="movsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="movsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="movsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="stosb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="stosw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="stosd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="cmpsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="cmpsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="cmpsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                
                elif(ls1[i+1]=="lodsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                elif(ls1[i+1]=="lodsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                    add1=add1+cal_add(obj)
                else:
                    if(ls1[i+1]=="lodsd"):
                        for k in range(l5):
                            if str(cnt) == ls5[k]:
                                p=ls5[k+2]
                        for l in range(l6):
                            if str(p)==ls6[l]:
                                p1=ls6[l+1]
                        obj=p1
                        fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                        add1=add1+cal_add(obj)
            #std instruction
            if(ls1[i]=="std"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
            #cld instruction
            if(ls1[i]=="cld"):
                for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
            #ret instruction
            if(ls1[i]=="ret"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
            #loop instruction
            if(ls1[i]=="loop"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(obj)+"\t\t"+str(ln1))
                add1=add1+cal_add(obj)
        ln1=fn1.readline()
        ls1=ln1.split()
        l1=len(ls1)

#-----------------------------------Object Code--------------------------------------------------
def replace_x(s):
    for i in s:
        if(i=='x'):
            s=s.replace(i,'0')
    return s

def cal_add(s):
    cn=0
    ls=['[',']','(',')']
    for i in s:
        if i not in ls:
            cn+=1
        else:
            exit
        c=int(cn)/2
    return int(c)
def add_space(s):
    s1=[s[i:i+2] for i in range(0,len(s),2)]
    r=' '.join(s1)
    return r

def obj_code(f1,f2,f3,f4,f5,f6):
    arr=["eax","ebx","ecx","edx","ebp","esp","esi","edi"]#32bit register
    arr1=["ax","bx","cx","dx"]#16bit register
    arr2=["ah","al","bh","bl","ch","cl","dh","dl"]#8bit register
    fn1=open(f1,"r")#add.asm
    fn2=open(f2,"r")#symbol.txt
    fn3=open(f3,"r")#literal.txt
    fn4=open(f4,"r")#modregister.txt
    fn5=open(f5,"r")#intermediate code op
    fn6=open(f6,"r")#opcode.txt
    ln1=fn1.readline()
    ln2=fn2.read()
    ln3=fn3.read()
    ln4=fn4.read()
    ln5=fn5.read()
    ln6=fn6.read()

    ls1=ln1.split()
    ls2=ln2.split()
    ls3=ln3.split()
    ls4=ln4.split()
    ls5=ln5.split()
    ls6=ln6.split()

    l1=len(ls1)
    l2=len(ls2)
    l3=len(ls3)
    l4=len(ls4)
    l5=len(ls5)
    l6=len(ls6)
    fw=open("objectop.txt","w")
    ls7=[]
    
    cnt=0
    while(ln1!=""):
        cnt+=1
        for i in range(l1):
            if(ls1[i]=="section"):
                if(ls1[i+1]==".data"):
                    add1=80840314
                    fw.write(str(add1)+"<__data_start>:"+"\n")
                if(ls1[i+1]==".bss"):
                    add2=80840200
                    fw.write(str(add2)+"<__bss_start>:"+"\n")        
            if(ls1[i]=="dd"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        a=ls2[j+3]
                oc=str(replace_x(hex(int(ls1[i+1])))).zfill(4)
                ls7.append(ls1[i-1])
                ls7.append(add1)
                fw.write("\t\t\t"+str(add1)+"\t"+str(add_space(oc))+"\n")
                add1=add1+int(a)
            if(ls1[i]=="db"):
                oc=str(replace_x(hex(10)+hex(0))).zfill(4)
                fw.write("\t\t\t"+str(add1)+"\t"+str(add_space(oc))+"\n")
            if(ls1[i]=="resb"):
                c=0000
                oc=str(c).zfill(4)
                a=ls1[i+1]
                fw.write("\t\t\t"+str(add2)+"\t"+str(add_space(oc))+"\n")
                add2=add2+int(a)
            if(ls1[i]=="resd"):
                c=0000
                oc=str(c).zfill(4)
                a=int(ls1[i+1])*4
                fw.write("\t\t\t"+str(add2)+"\t"+str(add_space(oc))+"\n")
                add2=add2+int(a)
            if(ls1[i]=="main:"):
                add=80840440
                fw.write(str(add)+"<main>:"+"\n")
            if(ls1[i]=="mov"):
                ls=ls1[i+1].split(",")
                #for mov eax,a
                if(ls[0] in arr and ls[1] in ls2):
                    for j in range(len(ls7)):
                        if ls[1]==ls7[j]:
                            s1=ls7[j+1]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+str(s1)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for 16 bit mov ax,a
                if(ls[0] in arr1 and ls[1] in ls2):
                    for j in range(len(ls7)):
                        if ls[1]==ls7[j]:
                            s1=ls7[j+1]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+str(s1)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for 8 bit mov al,a
                if(ls[0] in arr2 and ls[1] in ls2):
                    for j in range(len(ls7)):
                        if ls[1]==ls7[j]:
                            s1=ls7[j+1]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+str(s1)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for mov eax,3
                if(ls[0] in arr and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for 16 bit mov ax,3
                if(ls[0] in arr1 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for 8 bit mov al,3
                if(ls[0] in arr2 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for mov eax,ebx 32 bit
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for mov ax,bx 16 bit
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for mov al,bl 8 bit
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
            if(ls1[i]=="add"):
                ls=ls1[i+1].split(",")
                #for add eax,3
                if(ls[0] in arr and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for 16 bit add ax,3
                if(ls[0] in arr1 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for 8 bit add al,3
                if(ls[0] in arr2 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for add eax,ebx 32 bit
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for add ax,bx 16 bit
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for add al,bl 8 bit
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)

            if(ls1[i]=="sub"):
                ls=ls1[i+1].split(",")
                #for sub eax,3
                if(ls[0] in arr and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for 16 bit sub ax,3
                if(ls[0] in arr1 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for 8 bit sub al,3
                if(ls[0] in arr2 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1.zfill(8)[::-1]
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for sub eax,ebx 32 bit
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for sub ax,bx 16 bit
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for sub al,bl 8 bit
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
            # jmp instruction
            if(ls1[i]=="jmp"):
                for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            # mul  instruction
            if(ls1[i]=="mul"):
                for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1+'E3'
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            # div instruction
            if(ls1[i]=="div"):
                for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1+'F3'
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            #inc instruction
            if(ls1[i]=='inc'):
                if(ls1[i+1] in arr):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                if(ls1[i+1] in arr1):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj='66'+p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                if(ls1[i+1] in arr2):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+'C0'
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)

            #dec instruction
            if(ls1[i]=='dec'):
                if(ls1[i+1] in arr):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                if(ls1[i+1] in arr1):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj='66'+p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                if(ls1[i+1] in arr2):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+'C8'
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)

            if(ls1[i]=="xor"):
                ls=ls1[i+1].split(",")
                # for xor eax,ebx
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for xor ax,bx
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr1:
                        if x==ls[0]:
                            r1=x
                    for y in arr1:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for xor ah,bh
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr2:
                        if x==ls[0]:
                            r1=x
                    for y in arr2:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)

            if(ls1[i]=="cmp"):
                ls=ls1[i+1].split(",")
                # for cmp eax,ebx
                if(ls[0] in arr and ls[1] in arr):
                    for x in arr:
                        if x==ls[0]:
                            r1=x
                    for y in arr:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for cmp ax,bx
                if(ls[0] in arr1 and ls[1] in arr1):
                    for x in arr1:
                        if x==ls[0]:
                            r1=x
                    for y in arr1:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for cmp ah,bh
                if(ls[0] in arr2 and ls[1] in arr2):
                    for x in arr2:
                        if x==ls[0]:
                            r1=x
                    for y in arr2:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                #for cmp eax,3
                if(ls[0] in (arr or arr1 or arr2) and ls[1].isdigit()):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+ls[1].zfill(2)
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)

            # je instruction
            if(ls1[i]=="je"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            # jz instruction
            if(ls1[i]=="jz"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            # jne instruction
            if(ls1[i]=="jne"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            # jg instruction
            if(ls1[i]=="jg"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            # jge instruction
            if(ls1[i]=="jge"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            # jl instruction
            if(ls1[i]=="jl"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            # jle instruction
            if(ls1[i]=="jle"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            #push instruction
            if(ls1[i]=="push"):
                if(ls1[i+1] in arr):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                if(ls1[i+1] in ls2):
                    for k in range(l2):
                        if ls2[k]==ls1[i+1]:
                            s1=ls2[k+2]
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+s1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
            #call instruction
            if(ls1[i]=="call"):
                if(ls1[i+1]=="printf"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1+str(0).zfill(8)
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
            #rep movsb/stosb/cmpsb/lodsb instruction
            if(ls1[i]=="rep"):
                if(ls1[i+1]=="movsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="movsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="movsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="stosb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="stosw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="stosd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="cmpsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="cmpsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="cmpsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                
                elif(ls1[i+1]=="lodsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="lodsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                else:
                    if(ls1[i+1]=="lodsd"):
                        for k in range(l5):
                            if str(cnt) == ls5[k]:
                                p=ls5[k+2]
                        for l in range(l6):
                            if str(p)==ls6[l]:
                                p1=ls6[l+1]
                        obj=p1
                        fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                        add=add+cal_add(obj)

            #repz movsb/stosb/cmpsb/lodsb instruction
            if(ls1[i]=="repz"):
                if(ls1[i+1]=="movsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="movsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="movsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="stosb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="stosw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="stosd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="cmpsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="cmpsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="cmpsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                
                elif(ls1[i+1]=="lodsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="lodsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                else:
                    if(ls1[i+1]=="lodsd"):
                        for k in range(l5):
                            if str(cnt) == ls5[k]:
                                p=ls5[k+2]
                        for l in range(l6):
                            if str(p)==ls6[l]:
                                p1=ls6[l+1]
                        obj=p1
                        fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                        add=add+cal_add(obj)
            #repnz movsb/stosb/cmpsb/lodsb instruction
            if(ls1[i]=="repnz"):
                if(ls1[i+1]=="movsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="movsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="movsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="stosb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="stosw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="stosd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="cmpsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="cmpsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="cmpsd"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                
                elif(ls1[i+1]=="lodsb"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="lodsw"):
                    for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    obj=p1
                    fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                    add=add+cal_add(obj)
                else:
                    if(ls1[i+1]=="lodsd"):
                        for k in range(l5):
                            if str(cnt) == ls5[k]:
                                p=ls5[k+2]
                        for l in range(l6):
                            if str(p)==ls6[l]:
                                p1=ls6[l+1]
                        obj=p1
                        fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                        add=add+cal_add(obj)
            #std instruction
            if(ls1[i]=="std"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            #cld instruction
            if(ls1[i]=="cld"):
                for k in range(l5):
                        if str(cnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            #ret instruction
            if(ls1[i]=="ret"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
            #loop instruction
            if(ls1[i]=="loop"):
                for k in range(l5):
                    if str(cnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                obj=p1
                fw.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(obj))+"\n")
                add=add+cal_add(obj)
    
        ln1=fn1.readline()
        ls1=ln1.split()
        l1=len(ls1)


if __name__=="__main__":
    f=argv[1]
    symtab(f)   
    lit(f)    
    transform(f,"symbol.txt","litral.txt","op_register.txt")
    lst_code(f,"symbol.txt","litral.txt","mod.txt","intermediate_op.txt","opcode.txt")
    obj_code(f,"symbol.txt","litral.txt","mod.txt","intermediate_op.txt","opcode.txt")


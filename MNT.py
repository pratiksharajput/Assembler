
def mnt(f):
    mname=[]
    mpara=[]
    mstart=[]
    mend=[]
    fn=open(f,"r")
    l1=fn.readline()
    sl=l1.split()
    ln=len(sl)
    cnt=1
    while(l1!=""):
        for i in range(ln):
            if(sl[i]=='%macro'):
                mname.append(sl[i+1])
                mpara.append(sl[i+2])
                mstart.append(cnt)
            if(sl[i]=='%endmacro'):
                mend.append(cnt)
        l1=fn.readline()
        sl=l1.split()
        ln=len(sl)
        cnt+=1
    fw=open("mntop.txt","w")
    fw.write("Macro Name"+"\t"+"No.of parameter"+"\t"+"StartLine"+"\t"+"EndLine"+"\n")
    for i in range(len(mname)):
        fw.write(str(mname[i])+"\t\t"+str(mpara[i])+"\t\t"+str(mstart[i])+"\t\t"+str(mend[i])+"\n")

mnt("macdemo.asm")
        
        

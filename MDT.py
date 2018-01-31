def mdt(f):
    fn=open(f,"r")
    l1=fn.readline()
    sl=l1.split()
    ln=len(sl)
    fw=open("mdt_op.txt","w")
    f=0
    cnt=1
    while(l1!=""):
        if(f==1):
            fw.write(str(cnt)+"\t"+str(l1))
        for i in range(ln):
            if(sl[i]=='%macro'):
                f+=1
            if(sl[i]=='%endmacro'):
                f-=1
        l1=fn.readline()
        sl=l1.split()
        ln=len(sl)
        cnt+=1
mdt("macdemo.asm")

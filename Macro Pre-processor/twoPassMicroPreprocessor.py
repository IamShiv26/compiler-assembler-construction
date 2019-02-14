import re

mdt=list()
mnt=dict()
ala=dict()
macroStart=False
macroEnd=False
macroName=""
f = open("input.txt","r")
s=f.read()
f.close()
f1=open("outputpass1.txt","w")
s=s.split("\n")
for j in s:
  words = re.split(r'[,\s]\s*', j)
  if "MACRO" in words:
    macroStart=True
    continue
  elif(macroStart==True):
    if(len(words)==4):
      macroName=words[1]
      ala[macroName] = list()
      ala[macroName].append(words[0])
      for i in range(2,len(words)):
        ala[macroName].append(words[i])
    else:
      macroName=words[0]
      ala[macroName] = list()
      ala[macroName].append("-1")
      for i in range(1,len(words)):
        ala[macroName].append(words[i])
    mdt.append(j)
    mnt[macroName]=mdt.index(j)
    macroStart=False
    macroEnd=False
  elif(macroEnd==False):
    if "MEND" in words:
      mdt.append(j)
      macroEnd=True
    else:
      line = ""
      for i in words:
        if i in ala[macroName]:
          line=line+" #"+str(ala[macroName].index(i))
        else:
          line=line+" "+i
      mdt.append(line)
  else:
    f1.write(j)
    f1.write("\n")
    
f1.close() 
print("MDT :")
print(mdt)
print("MNT :")
print(mnt)
print("ALA : ")
print(ala)
import re

def pass1():
  g = open("input.txt","r")
  s = g.read()
  g.close()
  words = s.split("\n")

  f = open("outputpass1.txt","w")

  for j in words:
    if(j.find("equ")==-1):
      f.write(j)
      f.write("\n")
    m=j
    if(searchInPOT1(j)==False):
      searchInMOT1(m)
  f.close()
  print("Symbol table:")
  print('{:<10s}{:>4s}{:>12s}{:>12s}'.format("Symbol","Value","Length","Relocation"))
  for key,v in sym.items():
    print('{:<10s}{:>5d}{:^18d}{:>1s}'.format(key,v["value"],v["length"],v["relocation"]))
  print()
  print("Literal table:")
  print('{:<10s}{:>4s}{:>12s}{:>12s}'.format("Symbol","Value","Length","Relocation"))
  for key,v in lit.items():
    print('{:<10s}{:>5d}{:^18d}{:>1s}'.format(key,v["value"],v["length"],v["relocation"]))
  lc=0

def pass2():
  global line_no
  f = open("outputpass1.txt","r")
  s1 = f.read()
  f.close()
  words1 = s1.split("\n")
  for j in words1:
    m=j
    if(searchInPOT2(j)==False):
      #print(j)
      searchInMOT2(m)
    line_no=line_no+1

def searchInPOT1(w1):
  global lc
  w = w1.split(" ")
  k=0
  if(len(w)==3):
    k=1
  if(w[k]=="dc" or w[k]=="ds"):
    x = w[k+1]
    index = x.index("f")
    if(k==1):
      sym[w[0]] = {
        "value" : lc,
        "length" : 4,
        "relocation" : "R"
      }
    if(index!=0):
      #F at the end
      l = int(x[:len(x)-1])
      l =l*4
      lc = lc+l
    else:
      #F at the start
      nums = x[index+1:len(x)]
      intnums = nums.split(",")
      lclist.append(lc)
      for e in range(len(intnums)):
        lclist.append(lc)
        lc=lc+4
    return True
  elif(w[k]=="equ"):
    if(w[2]=="*"):
      sym[w[0]] = {
        "value" : lc,
        "length" : 1,
        "relocation" : "R"
      }
    else:
      sym[w[0]] = {
        "value" : int(w[2]),
        "length" : 1,
        "relocation" : "A"
      }
    #lclist.append(lc)
    return True
  elif(w[k]=="start"):
    sym[w[0]] = {
        "value" : int(w[2]),
        "length" : 1,
        "relocation" : "R"
      }
    lc = int(w[2])
    lclist.append(lc)
    return True
  elif(w[k]=="ltorg"):
    ltorg(True)
    #lclist.append(lc)
    return True
  elif(w[k]=="end"):
    ltorg(False)
    #lclist.append(lc)
    return True
  else:
    return False

def searchInMOT1(w1):
  global lc
  we = re.split(r'[,\s]\s*', w1)
  k=0
  if(len(we)==4):
    k=1
  if(we[len(we)-1][0]=="="):
    lit[we[len(we)-1][1:]] = {
        "value" : -1,
        "length" : 4,
        "relocation" : "R"
      }
  if(k==1 and we[0]!="end"):
    sym[we[0]] = {
        "value" : lc,
        "length" : 4,
        "relocation" : "R"
      }
  lclist.append(lc)
  for m in we:
    if m in mot:
      lc = lc+mot[m]["length"]
      break  

def ltorg(isnotEnd):
  global lc
  valueAssigned=True
  for b in lit:
    if(lit[b]["value"]==-1):
      valueAssigned=False
      break
  if(valueAssigned):
    return
  if(isnotEnd):
    while(lc%8!=0):
      lc=lc+1
      #lclist.append(lc)
  lclist.append(lc)
  for b in lit:
    lit[b]["value"]=lc
    lc=lc+4
    lclist.append(lc)

def searchInPOT2(w3):
  if(w3.find("using")!=-1):
    we1 = re.split(r'[,\s]\s*', w3)
    if(we1[1]=="*"):
      baset[int(we1[2])-1] = lclist[line_no]
      return True
    elif we1[2].isdigit():
      baset[int(we1[2])-1] = int(sym[we1[1]]["value"])
      return True
    else:
      baset[int(sym[we1[2]]["value"])-1] = int(sym[we1[1]]["value"])
      return True
  we1 = w3.split(" ")
  k=0
  if(len(we1)==3):
    k=1
  if(we1[k]=="ds"):
    
    return True
  elif(we1[k]=="dc"):
    
    return True
  elif(we1[k]=="equ"):
    return True
  elif(we1[k]=="start"):
    return True
  elif(we1[k]=="ltorg"):
    return True
  elif(we1[k]=="end"):
    return True
  else:
    return False

def searchInMOT2(w4):
  global lc2
  we2 = re.split(r'[,\s]\s*', w4)
  k=0
  mask=""
  temp=""
  if(we2[0]==""):
    return
  if(len(we2)==4):
    k=1
  if we2[k] in mot:
    temp = we2[k]
  if(we2[k]=="bne"):
    mask = "7"
  elif(we2[k]=="br"):
    mask="15"
  else:
    mask="0"
  if(we2[k][0]=="b"):
    if(we2[k][-1]=="r"):
      we2[k]="bcr"
    else:
      we2[k]="bc"
    we2.insert(k+1,mask)
  output=""
  output=str(lclist1[lc2])
  lc2=lc2+1
  if(mot[temp]["type"] == "rr"):
    output =output +" " +we2[k]
    output=output+ " "*(6-len(we2[k]))
    for i in range(k+1,len(we2)):
      value=getSymValue(we2[i])
      if(value!=-1):
        we2[i]=str(value)+""
    output=output+we2[k+1]
    for j in range(k+2,len(we2)):
      output=output+", " + we2[j]
  else:
    output =output +" " + we2[k]
    output=output+ " "*(6-len(we2[k]))
    for i in range(k+1,len(we2)-1):
      value=getSymValue(we2[i])
      if(value!=-1):
        we2[i]=str(value)+""
    #print(i)
    we2[i+1]=createOffset(we2[i+1])
    output=output+we2[k+1]
    for j in range(k+2,len(we2)):
      #print(output)
      output=output+", " + we2[j]
  f1.write(output)
  f1.write("\n")
  
def getSymValue(s):
  if s in sym:
    return sym[s]["value"]
  return -1

def getLitValue(s):
  if s in lit:
    #print(lit[s]["value"])
    return lit[s]["value"]
  return -1

def createOffset(s):
  orig=s
  index=0
  value=-1
  index_reg=0
  print(s)
  if(s[0]=="="):
    value=getLitValue(s[1:len(s)])
    #print(value)
  else:
    para = s.find("(")
    if(para!=-1):
      s=s[0:(s.find("("))]
      index_string=orig[(orig.find("(")+1):(orig.find(")"))]
      index_reg = sym[index_string]["value"]
    value=getSymValue(s)
  offset = abs(value-baset[index])
  for b in range(len(baset)):
    new_offset = abs(value-baset[b])
    if(new_offset<offset):
      offset=new_offset
      index=b+1
  result = str(offset) + "(" + str(index_reg) + ", " + str(index) + ")"
  return result

pot = {
  "start" : "initiate the first or only executable control section",
  "using" : "specifies a base address and range and assigns one or more base registers",
  "ltorg" : "collects and assembles literals into a literal pool.",
  "equ" : "assigns absolute or relocatable values to symbols",
  "drop" : "ends the domain of a USING instruction",
  "dc" : "define the data constants you need for program execution.",
  "ds" : "Reserves areas of storage",
  "end" : "End of Program"
}

mot = {
  "l" :{
    "type":"rx",
    "length":4,
    "binary opcode":"03h"
  },
  "a" :{
    "type":"rx",
    "length":4,
    "binary opcode":"05h"
  },
  "st" : {
    "type":"rx",
    "length":4,
    "binary opcode":"09h"
  },
  "sr" : {
    "type":"rr",
    "length":2,
    "binary opcode":"02h"
  },
  "c" : {
    "type":"rx",
    "length":4,
    "binary opcode":"06h"
  },
  "lr" :{
    "type":"rr",
    "length":2,
    "binary opcode":"08h"
  },
  "ar" :{
    "type":"rr",
    "length":2,
    "binary opcode":"04h"
  },
  "br" :{
    "type":"rr",
    "length":2,
    "binary opcode":"15h"
  },
  "bne" :{
    "type":"rx",
    "length":4,
    "binary opcode":"07h"
  },
  "la" :{
    "type":"rx",
    "length":4,
    "binary opcode":"01h"
  }
}
lc=0
sym = dict()
lit=dict()
lclist = list()
baset = [-1]*15
line_no=0
pass1()
f1=open("outputpass2.txt","w")
lclist1=sorted(list(set(lclist)))
print(lclist1)
lc2=0
pass2()
f1.close()
print(baset)


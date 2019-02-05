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
    else:
      #F at the start
      nums = x[index+1:len(x)]
      intnums = nums.split(",")
      l = 4*len(intnums)
    lc = lc+l
    lclist.append(lc)
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
    lclist.append(lc)
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
    lclist.append(lc)
    return True
  elif(w[k]=="end"):
    ltorg(False)
    lclist.append(lc)
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
  for m in we:
    if m in mot:
      lc = lc+mot[m]["length"]
      break
  lclist.append(lc)  

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
  for b in lit:
    lit[b]["value"]=lc
    lc=lc+4

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

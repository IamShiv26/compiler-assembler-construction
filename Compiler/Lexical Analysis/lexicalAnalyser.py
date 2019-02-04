import re
import time
from bisect import bisect_left 
def BinarySearch(a, x): 
    i = bisect_left(a, x) 
    if i != len(a) and a[i] == x: 
        return True 
    else: 
        return False
keys = ["auto","double","int","struct",
"break","else","long","switch",
"case","enum","register","typedef",
"char","extern","return","union",
"continue","for","signed","void",
"do","if","static","while",
"default","goto","sizeof","volatile",
"const","float","short","unsigned"]
funcs = ["main","scanf","printf"]
ops=["+","-","/","*","%","=","(",")"]
spch=["{","}",";",'"',"'",","]
keys=sorted(keys)
funcs=sorted(funcs)
ops=sorted(ops)
spch=sorted(spch)
v = list()
numlits=list()
strlits=list()
g = open("inputfile.txt","r")
s = g.read()
g.close()
words = re.split("([^a-zA-Z0-9\._])",s);
for j in words:
  if (j==" " or j==""):
    words.remove(j)
flag=0
ind=0
print()
init=time.time()
for w in words:
  if(w=="\n"):
    print()
    continue
  if(flag==0 or w=='"'):
    if BinarySearch(keys,w):
      print("<keyword #",keys.index(w),">",end="\t")
    elif BinarySearch(funcs,w):
      print("<function #",funcs.index(w),">",end="\t")
    elif BinarySearch(ops,w):
      print("<operator #",ops.index(w),">",end="\t")
    elif BinarySearch(spch,w):
      if(w=='"'):
        flag=flag+1
        if(flag==2):
          strarr = words[ind:(words.index(w))]
          str1="".join(strarr)
          strlits.append(str1)
          print("<strliterals #",strlits.index(str1),">",end="\t")
          flag=0
        ind = words.index(w)
        words[words.index(w)] = "";
      print("<special chars #",spch.index(w),">",end="\t")
    elif(w.isdigit()):
      if w in numlits:
        print("<numliterals #",numlits.index(w),">",end="\t")
        continue
      else:
        numlits.append(w)
        print("<numliterals #",numlits.index(w),">",end="\t")
    elif(not(w[0].isdigit())):
      if w in v:
        print("<variable #",v.index(w),">",end="\t")
        continue
      else:
        v.append(w)
        print("<variable #",v.index(w),">",end="\t")
    else:
      try: 
        float(w)
        if w not in numlits:
          numlits.append(w)
        print("<numliterals #",numlits.index(w),">",end="\t")
      except ValueError: 
        continue
print()
final=time.time()
print("Time taken = ",final-init)
print("Variables : ",v)
print("Numerical Literals : ",numlits)
print("String Literals : ",strlits)
#x, y, z, n = (int(input()) for _ in range(4))
#masterlist=[]
#
#for a in range(0,x+1):
#  for b in range(0,y+1):
#    for c in range(0,z+1):
#
#      masterlist.append([a,b,c])
#
#print(masterlist)

X = int(input())
Y = int(input())
Z = int(input())
N = int(input())

X += 1
Y += 1
Z += 1

tmp_list = [[x, y, z] for x in range(X) for y in range(Y) for z in range(Z) if x + y + z != N]
print(tmp_list)

x=[]
y=[]

import matplotlib.pyplot as plt

with open("contours.txt", 'r') as f:
   temp = f.readlines()
#    print(temp) 

for coord in temp:
    x.append(coord.split(" ")[0])
    y.append(coord.split(" ")[1])
    
# print(x)

plt.scatter(x,y)
plt.show()
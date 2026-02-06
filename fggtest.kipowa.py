
import matplotlib.pyplot as plt
import random
import math
xmax,ymax = 20, 10
InitFieldTexture = "J"
BordureFieldTexture = "A"

junglefield = " "
jungleTexture = InitFieldTexture
ci = 0
# junglefield initialization
for yi in range(ymax):
    junglefield += "\n"
    ci=0
    for xi in range(xmax):
        junglefield += "F "
        ci+=1
print(junglefield)
grid = list(junglefield)

def access_case(case_x, case_y, grid):
    return str(grid[case_y][case_x])

def modify_case(element, case_x, case_y, grid):
    grid[case_y][case_x]=element
    return grid

#print("".join(grid))
#print(grid)c
#searchgrid = "".join(grid)

computinggrid = "".join("".join(grid).rstrip().split(" ")).split("\n")
#print(computinggrid)
cptgrid = [tsr.split(" ") for tsr in "".join(grid).split("\n")]
#print(cptgrid)

centers = []
centers_char = []
nb_fields = 4
# center fields gen.
for fci in range(nb_fields):
    centers.append([random.randint(0,xmax),random.randint(0,ymax)])
    centers_char.append(str(fci))
    
centers_color = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']    
if(len(centers) != nb_fields):
    logging.error("Incorrect Centers gen.")
    exit(-1)

points = [[],[],[]]
for xi in range(xmax):
    for yi in range(1,ymax+1):
        nearestcenter = 0
        ici = 0
        nearestdist = math.sqrt((centers[0][0]-xi)**2+(centers[0][1]-yi)**2)
        for fci in centers[1:]:
            ici += 1
            dist = math.sqrt((fci[0]-xi)**2+(fci[1]-yi)**2)
            if(dist <= nearestdist):
                nearestcenter = ici
                nearestdist = dist
            modify_case(centers_char[nearestcenter], xi, yi, cptgrid)
            points[0].append(xi)
            points[1].append(yi)
            points[2].append(centers_color[nearestcenter])

#print(access_case(5, 7, cptgrid))
#ch = "A"
#cptgrid = modify_case("AA", 5, 7, cptgrid)
gridtoshow = [" ".join(cptlist) for cptlist in cptgrid]
gridtoshow = "\n".join(gridtoshow)
print(gridtoshow)

#fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 18))
plt.suptitle('FGG GENERIC PROGRAM #001 (2026-02-06) Ay.O.', fontsize=20, fontweight='bold')
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
colorsm = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
mintemp_locations = [10, 15, 20]
maxtemp_locations = [25, 30, 35]
names = ["Siberia", "Moscow", "Sochi"]

# Modified function call with marker and color
#plt.scatter(mintemp_locations, maxtemp_locations, s=100, c='red', marker='D')
#plt.scatter([1,2,3,4,5,6,7,8,9],[10,20,30,40,50,60,70,80,90],[2,3,4,1,1,1,5,6,7],c='#9467bd',marker='D')
plt.scatter(points[0],points[1],100,c=points[2],marker='D')
#for i in range(len(names)):
#    plt.text(mintemp_locations[i], maxtemp_locations[i], names[i], fontsize=9, verticalalignment='bottom', horizontalalignment='right')

plt.show()
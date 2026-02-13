import datetime
TOP,DOWN,LEFT,RIGHT=0,1,2,3
xmax,ymax = 20, 10
InitFieldTexture = "J"
BordureFieldTexture = "A"

# ---------------   LOADING GRID ---------------------------------
f = open("./fggstep1.txt", "r")
lines = f.readlines()
#print(lines)
goldfield = ""
for line in lines:
    line = line[0:40]
    goldfield += line+"\n"
#print(goldfield)
cptgrid = [fieldalt.split(' ')[:-1] for fieldalt in goldfield.split('\n')][2:-1]
#print(cptgrid)

# ----------------- LOADING CENTERS -------------------------------
f2 = open("./fggstep1centers.txt", "r")
lines = f2.readlines()
#print(lines)
centers = []
for line in lines:
    cx,cy = line.split(",")
    cx,cy = int(cx)-1,int(cy)-1
    centers.append([cx,cy])
#print("Centers : ", centers)

def access_case(case_x, case_y, grid):
    return str(grid[case_y][case_x])

def modify_case(element, case_x, case_y, grid):
    cptgrid[case_y][case_x]=element
    return grid

def show_grid(grid):
    ptgd = "\n".join([" ".join(gridline) for gridline in grid])
    print(ptgd+"\n\n")

#show_grid(cptgrid)
#print(access_case(5, 7, cptgrid))
#ch = "A"
#grid = modify_case("AA", 5, 7, cptgrid)
#show_grid(grid)

field_texture = []
"""for xi in range(xmax):
    for yi in range(ymax):
        car = access_case(xi, yi, cptgrid)
        if car not in field_texture:
            field_texture.append(car)
"""     
fields = list(set(goldfield))
#print(fields)
#print("How many fields there are ?")
fields2 = []
for n in fields:
    if n.isdecimal():
        fields2.append(n)

#print("There are "+str(len(fields2))+" fields")
#print(fields2)

class FieldState:
    
    def __init__(self, cx, cy, state):
        self.center = {'cx':cx, 'cy':cy}
        self.state_car = state
            
        self.uppers = 0
        self.downers = 0
        self.lefters = 0
        self.righters = 0
            
        self.uplers = 0
        self.upriers = 0
        self.dolers = 0
        self.doriers = 0
            
        self.maxwidth = 0
        self.maxheigth = 0
        self.minwidth = 0
        self.minheigth = 0
            
        self.neighbours = [[],[],[],[]]
            
    def update_ers(self, ixi, iyi, prevstate, xi, yi, state):
        if state == access_case(cx, cy, cptgrid):
            if xi > self.center['cx']:
                self.uppers += 1
            if xi < self.center['cx']:
                self.downers +=1
            if yi > self.center['cy']:
                self.righters +=1
            if yi < self.center['cy']:
                self.lefters +=1
                    
            if xi>self.center['cx'] and yi>self.center['cy']:
                self.upriers +=1
            if xi>self.center['cx'] and yi<self.center['cy']:
                self.uplers +=1
            if xi<self.center['cx'] and yi>self.center['cy']:
                self.doriers +=1
            if xi<self.center['cx'] and yi<self.center['cy']:
                self.dolers +=1
                    
            if prevstate != state:
                if ixi > xi:
                    self.neighbours[TOP].append(prevstate)
                if iyi > yi:
                    self.neighbours[LEFT].append(prevstate)
                if iyi < yi:
                    self.neighbours[RIGHT].append(prevstate)
                if ixi < xi:
                    self.neighbours[DOWN].append(prevstate)
                
    def show_state_card(self):
        print("\nUppers : "+str(self.uppers))
        print("\nDowners : "+str(self.downers))
        print("\nLefters : "+str(self.lefters))
        print("\nRighters : "+str(self.righters))
                
        print("\nUplers : "+str(self.uplers))
        print("\nUpriers : "+str(self.upriers))
        print("\nDolers : "+str(self.dolers))
        print("\nDoriers : "+str(self.doriers))
        
        print("\nMax Width : "+str(self.maxwidth))
        print("\nMax Heigth : "+str(self.maxheigth))
        print("\nMin Heigth : "+str(self.minwidth))
        print("\nMin Heigth : "+str(self.minheigth))
        
        print("\nNeighbours : "+str(self.neighbours))
        
    def print_state_card(self):
        datetimetod = datetime.datetime
        today = datetimetod.now()
        print(today)
        cardtxt= str(today)
        cardtxt+="\nUppers : "+str(self.uppers)
        cardtxt+="\nDowners : "+str(self.downers)
        cardtxt+="\nLefters : "+str(self.lefters)
        cardtxt+="\nRighters : "+str(self.righters)
                
        cardtxt+="\nUplers : "+str(self.uplers)
        cardtxt+="\nUpriers : "+str(self.upriers)
        cardtxt+="\nDolers : "+str(self.dolers)
        cardtxt+="\nDoriers : "+str(self.doriers)
        
        cardtxt+="\nMax Width : "+str(self.maxwidth)
        cardtxt+="\nMax Heigth : "+str(self.maxheigth)
        cardtxt+="\nMin Heigth : "+str(self.minwidth)
        cardtxt+="\nMin Heigth : "+str(self.minheigth)
        
        cardtxt+="\nNeighbours : "+str(self.neighbours)
        return cardtxt
        
    def save_state(self):
        namefile = "./fggtest.running/states/state_"+str(self.state_car)+".txt"
        cardtxt = self.print_state_card()
        f = open(namefile, "w+")
        f.write(cardtxt)
        f.close()

fieldstates = []
for centi in centers:
    cix,ciy = centi[0], centi[1]
    citxt = access_case(cix, ciy, cptgrid)
    ifieldstate = FieldState(cix-1, ciy-1, citxt)
    print("Field center : "+str(ifieldstate.center))
    print("Field floor : "+ifieldstate.state_car)
    fieldstates.append(ifieldstate)




for xi in range(xmax):
    for yi in range(ymax):
        if xi>0:
            oldstate = access_case(xi-1, yi, cptgrid)
            for iproc_state in range(len(fieldstates)):
                fieldstates[iproc_state].update_ers(xi-1, yi, oldstate, xi, yi, access_case(xi, yi, cptgrid))
            
for iproc_state in range(len(fieldstates)):
    fieldstates[iproc_state].show_state_card()
    fieldstates[iproc_state].print_state_card()
    fieldstates[iproc_state].save_state()
    
print("\nFIELDS STATES PROCESSED, you can find results in 'states' Folder\n")

import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
        self.namefile = "./fggtest.running/states/state_"+str(self.state_car)+".txt"
            
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

    def draw_field_cross(self, ax=None):
        """
        Draw a cross representing the min/max extents of the classified field
        centered on the field's center point.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))

        cx = self.center['cx']
        cy = self.center['cy']

        # --- Cross arms using max extents ---
        # Horizontal arm (width)
        ax.plot(
            [cx - self.maxwidth, cx + self.maxwidth],
            [cy, cy],
            color='blue', linewidth=2, label='Max extent'
        )
        # Vertical arm (height)
        ax.plot(
            [cx, cx],
            [cy - self.maxheigth, cy + self.maxheigth],
            color='blue', linewidth=2
        )

        # --- Inner cross arms using min extents ---
        # Horizontal arm (min width)
        ax.plot(
            [cx - self.minwidth, cx + self.minwidth],
            [cy, cy],
            color='cyan', linewidth=1.5, linestyle='--', label='Min extent'
        )
        # Vertical arm (min height)
        ax.plot(
            [cx, cx],
            [cy - self.minheigth, cy + self.minheigth],
            color='cyan', linewidth=1.5, linestyle='--'
        )

        # --- Endpoint markers on max cross ---
        endpoints_max = [
            (cx - self.maxwidth, cy),
            (cx + self.maxwidth, cy),
            (cx,                 cy - self.maxheigth),
            (cx,                 cy + self.maxheigth),
        ]
        for px, py in endpoints_max:
            ax.plot(px, py, 'bs', markersize=6)

        # --- Endpoint markers on min cross ---
        endpoints_min = [
            (cx - self.minwidth, cy),
            (cx + self.minwidth, cy),
            (cx,                 cy - self.minheigth),
            (cx,                 cy + self.minheigth),
        ]
        for px, py in endpoints_min:
            ax.plot(px, py, 'c^', markersize=5)

        # --- Center point ---
        ax.plot(cx, cy, 'ro', markersize=8, label='Center')

        # --- Annotations ---
        ax.annotate(f'maxW={self.maxwidth}',
                    xy=(cx + self.maxwidth, cy),
                    xytext=(8, 4), textcoords='offset points', fontsize=8, color='blue')
        ax.annotate(f'maxH={self.maxheigth}',
                    xy=(cx, cy + self.maxheigth),
                    xytext=(4, 6), textcoords='offset points', fontsize=8, color='blue')
        ax.annotate(f'minW={self.minwidth}',
                    xy=(cx + self.minwidth, cy),
                    xytext=(8, -12), textcoords='offset points', fontsize=8, color='teal')
        ax.annotate(f'minH={self.minheigth}',
                    xy=(cx, cy + self.minheigth),
                    xytext=(4, -14), textcoords='offset points', fontsize=8, color='teal')

        # --- Bounding box (optional visual reference) ---
        bbox = patches.Rectangle(
            (cx - self.maxwidth, cy - self.maxheigth),
            self.maxwidth * 2,
            self.maxheigth * 2,
            linewidth=0.8, edgecolor='gray', facecolor='none', linestyle=':'
        )
        ax.add_patch(bbox)

        ax.set_aspect('equal')
        ax.legend(loc='upper right', fontsize=8)
        ax.set_title(f'Field cross — center ({cx}, {cy})')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()    
        
    def update_ers_ex(self, ixi, iyi, prevstate, xi, yi, state):
        maxwidth = 0
        maxheigth = 0
        minwidth = xmax
        minheigth = ymax
        
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
                    
    def update_ers_ex2(self, ixi, iyi, prevstate, xi, yi, state):
        if state == access_case(cx, cy, cptgrid):
            # Directional counters relative to center
            if xi > self.center['cx']:
                self.uppers += 1
            if xi < self.center['cx']:
                self.downers += 1
            if yi > self.center['cy']:
                self.righters += 1
            if yi < self.center['cy']:
                self.lefters += 1

            if xi > self.center['cx'] and yi > self.center['cy']:
                self.upriers += 1
            if xi > self.center['cx'] and yi < self.center['cy']:
                self.uplers += 1
            if xi < self.center['cx'] and yi > self.center['cy']:
                self.doriers += 1
            if xi < self.center['cx'] and yi < self.center['cy']:
                self.dolers += 1

            # Compute distance from center for this cell
            dist_x = abs(xi - self.center['cx'])
            dist_y = abs(yi - self.center['cy'])

            # Update min/max width (horizontal spread from center)
            if dist_x > self.maxwidth:
                self.maxwidth = dist_x
            if dist_x < self.minwidth:
                self.minwidth = dist_x

            # Update min/max height (vertical spread from center)
            if dist_y > self.maxheigth:
                self.maxheigth = dist_y
            if dist_y < self.minheigth:
                self.minheigth = dist_y

            # Neighbour tracking on state transitions
            if prevstate != state:
                if ixi > xi:
                    self.neighbours[TOP].append(prevstate)
                if iyi > yi:
                    self.neighbours[LEFT].append(prevstate)
                if iyi < yi:
                    self.neighbours[RIGHT].append(prevstate)
                if ixi < xi:
                    self.neighbours[DOWN].append(prevstate)
                    
    def update_ers(self, ixi, iyi, prevstate, xi, yi, state):
        if state == access_case(cx, cy, cptgrid):
            # Directional counters relative to center
            if xi > self.center['cx']:
                self.uppers += 1
            if xi < self.center['cx']:
                self.downers += 1
            if yi > self.center['cy']:
                self.righters += 1
            if yi < self.center['cy']:
                self.lefters += 1

            if xi > self.center['cx'] and yi > self.center['cy']:
                self.upriers += 1
            if xi > self.center['cx'] and yi < self.center['cy']:
                self.uplers += 1
            if xi < self.center['cx'] and yi > self.center['cy']:
                self.doriers += 1
            if xi < self.center['cx'] and yi < self.center['cy']:
                self.dolers += 1

            # Absolute distances from this field's center point
            dist_x = abs(xi - self.center['cx'])
            dist_y = abs(yi - self.center['cy'])

            # --- MAX: farthest cell from center on each axis ---
            if dist_x > self.maxwidth:
                self.maxwidth = dist_x
            if dist_y > self.maxheigth:
                self.maxheigth = dist_y

            # --- MIN: closest *non-center* cell from center on each axis ---
            # Width: only consider cells that are actually offset horizontally
            if dist_x > 0 and dist_x < self.minwidth:
                self.minwidth = dist_x

            # Height: only consider cells that are actually offset vertically
            if dist_y > 0 and dist_y < self.minheigth:
                self.minheigth = dist_y

            # Neighbour tracking on state transitions
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
        #plt.scatter(points[0],points[1],100,c=points[2],marker="s")
        #plt.show()
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
        namefile = self.namefile
        cardtxt = self.print_state_card()
        f = open(namefile, "w+")
        f.write(cardtxt)
        f.close()

    def load_state(self, filepath="./state.txt"):
        f2 = open(self.namefile, "r")
        lines = f2.readlines()
        print(lines)
        vectors = []
        for line in lines[1:]:
            vectors.append(line.split(" : ")[1][:-1])
        
        self.uppers = int(vectors[0])
        self.downers = int(vectors[1])
        self.lefters = int(vectors[2])
        self.righters = int(vectors[3])
        
        self.uplers = int(vectors[4])
        self.upriers = int(vectors[5])
        self.dolers = int(vectors[6])
        self.doriers = int(vectors[7])
            
        self.maxwidth = min([self.righters-self.lefters, xmax])
        self.maxheigth = min([self.downers-self.uppers, ymax])
        self.minwidth = int(vectors[10])
        self.minheigth = int(vectors[11])
        print(vectors)

        
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

fimax = len(fieldstates)
print("\nFIELDS STATES PROCESSING, LOADING STATES\n")
loadedstates = []
for fi in range(fimax):
    cxi,cyi = centers[fi][0],centers[fi][1]
    statei = FieldState(cxi,cyi,fi)
    statei.namefile = "./fggtest.running/states/state_"+str(fi)+".txt"
    statei.load_state()
    loadedstates.append(statei)

    statei.show_state_card()



# One color per classified field
FIELD_COLORS = ['blue', 'red', 'green', 'orange', 'purple']

def draw_fields_cross(fields):
    """
    Draw all synthetic field crosses on the same plan.

    Parameters
    ----------
    fields : list of dict, each containing:
        {
            'center':    {'cx': int, 'cy': int},
            'maxwidth':  float,
            'minwidth':  float,
            'maxheigth': float,
            'minheigth': float,
            'label':     str   (optional)
        }
    """
    fig, ax = plt.subplots(figsize=(10, 10))

    for i, fieldi in enumerate(fields):
            
        fieldin = {
            'center':    {'cx': fieldi.center['cx'], 'cy': fieldi.center['cy']},
            'maxwidth':  fieldi.maxwidth,
            'minwidth':  fieldi.maxheigth,
            'maxheigth': fieldi.minwidth,
            'minheigth': fieldi.minheigth,
            'label':    fieldi.state_car 
        }
        
        color     = FIELD_COLORS[i % len(FIELD_COLORS)]
        cx        = fieldin['center']['cx']
        cy        = fieldin['center']['cy']
        maxwidth  = fieldin['maxwidth']
        minwidth  = fieldin['minwidth']
        maxheigth = fieldin['maxheigth']
        minheigth = fieldin['minheigth']
        label     = fieldin.get('label', f'Field {i}')

        # --- Max cross arms ---
        ax.plot(
            [cx - maxwidth/2, cx + maxwidth/2], [cy, cy],
            color=color, linewidth=2,
            label=f'{label} max'
        )
        ax.plot(
            [cx, cx], [cy - maxheigth/2, cy + maxheigth/2],
            color=color, linewidth=2
        )

        # --- Min cross arms ---
        ax.plot(
            [cx - minwidth/2, cx + minwidth/2], [cy, cy],
            color=color, linewidth=1.5, linestyle='--',
            label=f'{label} min'
        )
        ax.plot(
            [cx, cx], [cy - minheigth/2, cy + minheigth/2],
            color=color, linewidth=1.5, linestyle='--'
        )

        # --- Max arm endpoint markers ---
        for px, py in [
            (cx - maxwidth/2, cy), (cx + maxwidth/2, cy),
            (cx, cy - maxheigth/2), (cx, cy + maxheigth/2)
        ]:
            ax.plot(px, py, 's', color=color, markersize=6)

        # --- Min arm endpoint markers ---
        for px, py in [
            (cx - minwidth/2, cy), (cx + minwidth/2, cy),
            (cx, cy - minheigth/2), (cx, cy + minheigth/2)
        ]:
            ax.plot(px, py, '^', color=color, markersize=5, alpha=0.7)

        # --- Center point ---
        ax.plot(cx, cy, 'o', color=color, markersize=8)

        # --- Bounding box ---
        bbox = patches.Rectangle(
            (cx - maxwidth, cy - maxheigth),
            maxwidth  * 2,
            maxheigth * 2,
            linewidth=0.8, edgecolor=color,
            facecolor=color, alpha=0.05, linestyle=':'
        )
        ax.add_patch(bbox)

        # --- Annotations ---
        offset = 6
        ax.annotate(f'{label}\nmaxW={maxwidth} minW={minwidth}',
                    xy=(cx + maxwidth, cy),
                    xytext=(offset, 4), textcoords='offset points',
                    fontsize=7, color=color)
        ax.annotate(f'maxH={maxheigth}\nminH={minheigth}',
                    xy=(cx, cy + maxheigth),
                    xytext=(4, offset), textcoords='offset points',
                    fontsize=7, color=color)

    ax.set_aspect('equal')
    ax.legend(loc='upper right', fontsize=8)
    ax.set_title('All synthetic fields — FGG GENERIC PROGRAM 13_3_2026 2026 #OA004')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    
draw_fields_cross(fieldstates)

from sys import argv # here we are importing 'sys' module for argv function 
import numpy as np # here i have taken numpy module yo use as mathematical calculations specially in matrices.
import cmath# another module imported


if len(argv) != 2:# second argument is the file to be operated upon
    print("\nERROR :%s does not have an input file" % argv[0])
    exit()
# Provide error if no file is provided for operation
netlist_name = argv[1]
(CIRCUIT,FREQ,END) = (".circuit",".ac",".end")
Pi = np.pi            # i have Stored important constants for easily usage of it later in this code

class V_S:
    
    def __init__(self,node1,node2,val,phi):# here i have defined voltage class having nodes between its connected and its value as its properties including its phase also
        self.n1 = int(node1)# assigning nodes to a variable as mentioned
        self.n2 = int(node2)
        self.val = cmath.rect(val,(Pi*phi)/180)# here i have used 'cmath' module
        
class I_S:
    
    def __init__(self,node1,node2,val,phi):# same thing for current in wires
        self.n1 = int(node1)
        self.n2 = int(node2)
        self.val = cmath.rect(val,(Pi*phi)/180)

class Res:
# here i have defined class for resistors
    def __init__(self,node1,node2,val):# no need for phase in case of resistors
        self.n1 = int(node1)
        self.n2 = int(node2)
        self.val = float(val)
        

class Cap:

    def __init__(self,node1,node2,val):
        self.n1 = int(node1)
        self.n2 = int(node2)
        self.val = float(val)

    def impedance(self,w):
        if w == 0:
            return(float("inf"))
        else:
            return(complex(0,-1/(w*self.val)))
        
class Ind:

    def __init__(self,n1,n2,val):
        self.n1 = int(n1)
        self.n2 = int(n2)
        self.val = float(val)

    def impedance(self,w):
        return(complex(0,w*self.val))

try:
    f = open(netlist_name,"r")             # this command is for opening the file
    lines = f.readlines()            # here i want to read each line of the file as a seperate string
    f.close()                              #Closing the file 
    del(f,netlist_name)
    (start,end) = (-1,-2)                 #initialising the indexs value

    for i in range(len(lines)):
        if CIRCUIT == lines[i][:len(CIRCUIT)]:  
            start = i
        elif END == lines[i][:len(END)]:    
            end = i
# above commands for authenticating right type of file that is whether the file is in required format or not
            break
    w = 0
    for i in range(end + 1,len(lines)):
        if FREQ == lines[i][:len(FREQ)]:
            line = lines[i].split("#")[0].rstrip().split(" ")
            w = 2*Pi*float(line[-1])
            break

    if start >= end or start*end < 0:
        print("\nInvalid Circuit")
        exit()

except IOError:                             #If the file provided is not uo to our requirements that is it has some flaws
    print("\nCould not open the File.")
    exit()


"""
Printing the output in the desired format.
i.e. Circuit definition from bottom to top and right to left.
"""
Resistors, V_sources, I_sources, Capacitors, Inductors, nodes = {},{},{},{},{},{}
Shorts = []
#nodes = {}

    
def Identify(line):

    if line[0][0] == "R":
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            Resistors[line[0]] = Res(nodes[line[1]], nodes[line[2]], line[3])
    elif line[0][0] == "V":
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            if line[3].lower() == "dc":
                print("I got here in dc!")
                V_sources[line[0]] = V_S(nodes[line[1]], nodes[line[2]], float(line[4]), 0.0)
            elif line[3].lower() == "ac":
                print("I got here in ac!")
                V_sources[line[0]] = V_S(nodes[line[1]], nodes[line[2]], float(line[4])/2, float(line[5]))
    elif line[0][0] == "I":
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            if line[3].lower() == "dc":
                I_sources[line[0]] = I_S(nodes[line[1]], nodes[line[2]], float(line[4]), 0)
            elif line[3].lower() == "ac":
                I_sources[line[0]] = I_S(nodes[line[1]], nodes[line[2]], float(line[4])/2, line[5])
    elif line[0][0] == "C":
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            Capacitors[line[0]] = Cap(nodes[line[1]], nodes[line[2]], line[3])
    elif line[0][0] == "L":
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            Inductors[line[0]] = Ind(nodes[line[1]], nodes[line[2]], line[3])

def nodes_and_shorts(w):
    node_index = 1
    for line in lines[start+1:end]:
        line = line.split("#")[0].rstrip().split(" ")
        try:
            if line[0][0] not in ['R','V','I','C','L']:
                print("\nThis program currently does not support some of the elements")
                print("that are present in this circuit.Currently only R,L,C,V,I are supported.")
                print("Symbols have their usual meaning")
                exit()            
            for index1 in range(1,3):
                if line[index1] not in nodes.keys():
                    if line[index1] == "GND":
                        nodes[line[index1]] = 0
                    else:
                        nodes[line[index1]] = node_index
                        node_index += 1
            if (line[0][0] == "R") and (float(line[3]) == 0):
                Shorts.append(sorted([nodes[line[1]],nodes[line[2]]]))
            elif (line[0][0] == "V") and (float(line[4]) == 0):
                Shorts.append(sorted([nodes[line[1]],nodes[line[2]]]))
            elif (line[0][0] == "L") and (w == 0):
                Shorts.append(sorted([nodes[line[1]],nodes[line[2]]]))
        
        except IndexError:
            continue
        
    if "GND" not in nodes.keys():
        print("\nThe circuit does not have a conducting path to ground. Feed a proper circuit.")
        exit()

def manage_shorts():
    for short in Shorts:
        for R in Resistors.values():
            if R.n1 == short[1]:
                R.n1 = short[0]
            elif R.n2 == short[1]:
                R.n2 = short[0]
        for C in Capacitors.values():
            if C.n1 == short[1]:
                C.n1 = short[0]
            elif C.n2 == short[1]:
                C.n2 = short[0]
        for L in Inductors.values():
            if L.n1 == short[1]:
                L.n1 = short[0]
            elif L.n2 == short[1]:
                L.n2 = short[0]
        for V in V_sources.values():
            if V.n1 == short[1]:
                V.n1 = short[0]
            elif V.n2 == short[1]:
                V.n2 = short[0]
        for I in I_sources.values():
            if I.n1 == short[1]:
                I.n1 = short[0]
            elif I.n2 == short[1]:
                I.n2 = short[0]
                
def Read_Ciruit():
    for line in lines[start+1:end]:
        line = line.split("#")[0].rstrip().split(" ")
        if len(line) in [4,5,6]:
            Identify(line)


def Create_MNA_matrix():

    for R in Resistors.values():
        r = R.n1
        c = R.n2
        if r == c:
            continue
        elif r == 0:
            G[c-1,c-1] += 1/R.val
        elif c == 0:
            G[r-1,r-1] += 1/R.val
        else:
            G[r-1,r-1] += 1/R.val
            G[r-1,c-1] -= 1/R.val
            G[c-1,r-1] -= 1/R.val
            G[c-1,c-1] += 1/R.val

    for C in Capacitors.values():
        r = C.n1
        c = C.n2
        if r == c:
            continue
        elif r == 0:
            G[c-1,c-1] += 1/C.impedance(w)
        elif c == 0:
            G[r-1,r-1] += 1/C.impedance(w)
        else:
            G[r-1,r-1] += 1/C.impedance(w)
            G[r-1,c-1] -= 1/C.impedance(w)
            G[c-1,r-1] -= 1/C.impedance(w)
            G[c-1,c-1] += 1/C.impedance(w)

    for In in Inductors.values():
        r = In.n1
        c = In.n2
        if r == c:
            continue
        elif r == 0:
            if In.impedance(w) != 0:
                G[c-1,c-1] += 1/In.impedance(w)
        elif c == 0:
            if In.impedance(w) != 0:
                G[r-1,r-1] += 1/In.impedance(w)             
        else:
            if In.impedance(w) != 0:
                G[r-1,r-1] += 1/In.impedance(w)
                G[r-1,c-1] -= 1/In.impedance(w)
                G[c-1,r-1] -= 1/In.impedance(w)
                G[c-1,c-1] += 1/In.impedance(w)               

    aux_index = len(nodes) - 1 - len(Shorts)
    for V in V_sources.values():
        r = V.n1
        c = V.n2
        if r == c:
            continue
        elif c == 0:
            G[r-1,aux_index] += 1
            G[aux_index,r-1] += 1
            I[aux_index] += V.val
            aux_index += 1
        elif r == 0:
            G[c-1,aux_index] -= 1
            G[aux_index,c-1] -= 1
            I[aux_index] += V.val
            aux_index += 1
        else:
            G[r-1,aux_index] += 1
            G[c-1,aux_index] -= 1
            G[aux_index,r-1] += 1
            G[aux_index,c-1] -= 1
            I[aux_index] += V.val
            aux_index += 1

    for Is in I_sources.values():
        r = Is.n1
        c = Is.n2
        if r == c:
            continue
        elif c == 0:
            I[r-1] -= Is.val
        elif r == 0:
            I[c-1] += Is.val
        else:
            I[r-1] -= Is.val
            I[c-1] += Is.val

def Solve():
    sol = np.linalg.solve(G, I)
    for i in range(len(nodes)-1-len(Shorts),len(nodes) + len(V_sources) -len(Shorts)-1):
        #print("I(V%d) : %4.4f + j%4.4f (A)" % (i - len(nodes) + 2,solution[i].real,solution[i-1].imag))
        print("I(V",i - len(nodes) + 2 - len(Shorts),") :",sol[i])
    for i in range(1,len(nodes)-len(Shorts)):
        #print("V(node%d) : %4.4f + j%4.4f (V)" % (i,solution[i-1].real,solution[i-1].imag))
        print("V(node",i,") :",sol[i-1])
    print(sol)


nodes_and_shorts(w)
Read_Ciruit()
manage_shorts()
order = len(nodes) + len(V_sources) - len(Shorts) - 1
G = np.zeros((order,order),dtype=complex)
I = np.zeros(order,dtype=complex)
Create_MNA_matrix()
Solve()

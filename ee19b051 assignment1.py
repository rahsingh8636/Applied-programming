# EE2703 course
# Assignment 1:Traverse a circuit definition from last element to first and print out each line with words in reverse order.
#ROLL NO: EE19B051

from sys import argv, exit
# Here we are using "argv" function for accepting arguments from commandline. We are using "sys" module which contains that function.

# For convenience during change of .circuit and .end in spice programme we assign these values to a constant variable .
CIRCUIT = '.circuit'
END = '.end'

# Since we have to import a file on which this code could pe operated,we demand for two arguments in commandline
# First one is always the code file name followed by the second argument which is the file name to be operated upon. for example:$python3 assignment.py ckt.netlist .
# So for required functioning of the programme we crosscheck whether we have got appropriate number of arguments or not.If not ; give suitable error message.
if len(argv) != 2:
# always use ':' for condition statements
    print('\nERROR: %s does not have an <inputfile>!!' % argv[0])
    exit()
# we can use 'try','except' statement for whether the user have provide right file or not,if not give the error
try:
        f=open(argv[1])# opening the file enterd at argv[1] pointing towards variable f.
        lines = f.readlines()# this command is for reading each line of the argument file as seperate strings.
        f.close()# closing the file so as to stop reading it.
# Note: we could have also used 'with' statement which is more convenient as in that we dont have to think of closing the file
        start = -1; 
        end = -2
        for line in lines:              # extracting circuit definition start and end lines
            if CIRCUIT == line[:len(CIRCUIT)]:# slicing is done for the line string in order to check when to start fetching each line. To avoid junks statements this command is used.
                start = lines.index(line)
            elif END == line[:len(END)]:# to acknowledge when the file has ended and to avoid furthur junk .
                end = lines.index(line)
                break# after END ,come out of the 'for' loop
        if start >= end:                # validating circuit block
            print('Wrong circuit description!')
            exit(0)
# For printing in reverse order we use following statements/ syntax
        for line in reversed([' '.join(reversed(line.split('#')[0].split())) for line in lines[start+1:end]]):
            print(line)                 # print required order of output

except IOError:
    print('Invalid file!')# if the file provided was wrong
    exit()



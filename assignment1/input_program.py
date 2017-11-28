#Freddy Marquez
#https://www.youtube.com/watch?v=Ui2CaZWUSCg&t=23s
import sys

print('Standard Input: ')
text= sys.stdin.readline() #read line from standard input while program is running
while text: # will continue to ask for input until ctrl+Z is pressed
    print(text, end='') #prints out the text, does not create an extra new line
    text= sys.stdin.readline() #store new input to text variable

#global initializers/global assignments
option_o = False
option_t = False
option_h = False
x=''
y=''

print("Command line arguments: ")
i=1 #start at 1 to skip the first argument (the python file)
while i <len(sys.argv): # i is less than the length of command line arguments
    if sys.argv[i] == "-o": # if -o command line argument exists
        option_o = True # change option_o to true
        x= sys.argv[i+1] #store the string that proceeds '-o'
        i += 1
    elif sys.argv[i] == "-t": # if -t command line argument exists
        option_t = True # change option_t to true
        y= sys.argv[i+1] # store the string that proceeds '-t'
        i += 1
    elif sys.argv[i] == "-h": # if -h command line argument exists
        option_h = True # change option_h to true
        i += 1 # -h will never have a string follow it
    else:
        i += 1

if option_o == True:
    print("option 1: " + x) # print option_o if found
if option_t == True:
    print("option 2: " + y) # print option_t
if option_h == True:
    print("option 3") # print option_h if found
else:
    pass

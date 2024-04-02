import sys,getopt
import numpy as np

if __name__=='__main__':
    argument_list = sys.argv[1:]
    options = 'o:v:'
    long_options = ['opponent=','value-policy=']
    state=[]
    Pi = []
    Vf = []
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ('-o','--opponent'):
                path = currentValue
                fp = open(path,'r')
                line = fp.readline().strip()
                line = fp.readline().strip() 
                while line!='':
                    line = line.split(' ')
                    state.append(line[0])
                    line=fp.readline().strip() 
            elif currentArgument in ('v','--value-policy'):
                path = currentValue
                fp = open(path,'r')
                line = fp.readline().strip()
                while line!='':
                    line = line.split(' ')
                    Vf.append(line[0])
                    Pi.append(line[1])
                    line=fp.readline().strip()
    except getopt.error as err:
        print (str(err))
    for i in range(8192):
        print(state[i],Pi[i],Vf[i])
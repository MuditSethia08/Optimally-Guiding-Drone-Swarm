import numpy as np
import matplotlib.pyplot as plt
#Finding expected number of goals
V=[]
path_list=['policyfile_p01_q07.txt','policyfile_2_p01_q07.txt','policyfile_3_p01_q07.txt']
for p in path_list:
    fp=open(p,'r')
    vf=[]
    line=fp.readline().strip()
    while line!='':
        line=line.split(' ')
        vf.append(float(line[2]))
        line=fp.readline().strip()
    vf = np.array(vf)
    V.append(np.sum(vf)/8192)
#P varying, Q constant
w1=[]
path_list=['policyfile_p00_q07.txt','policyfile_p01_q07.txt','policyfile_p02_q07.txt','policyfile_p03_q07.txt','policyfile_p04_q07.txt','policyfile_p05_q07.txt']
for p in path_list:
    fp=open(p,'r')
    line=line=fp.readline().strip()
    line.split(' ')
    while(True):
        if(line[0]=='0509081'):
            w1.append(float(line[2]))
            break
        else:
            line=fp.readline().strip()
            line=line.split(' ')
w2=[]
path_list=['policyfile_p03_q06.txt','policyfile_p03_q07.txt','policyfile_p03_q08.txt','policyfile_p03_q09.txt','policyfile_p03_q10.txt']
for p in path_list:
    fp=open(p,'r')
    line=fp.readline().strip()
    line=line.split(' ')
    while(True):
        if(line[0]=='0509081'):
            w2.append(float(line[2]))
            break
        else:
            line=fp.readline().strip()
            line=line.split(' ')
print(w2)
print(w1)

#Ps
p = [0,0.1,0.2,0.3,0.4,0.5]
#Qs
q=[0.6,0.7,0.8,0.9,1.0]

#Plot
plt.plot(p,w1)
plt.xlabel('Value of p given q=0.7')
plt.ylabel('Probability of winning by starting at state 0509081')
plt.savefig('PS.png')
plt.close()
plt.plot(q,w2)
plt.xlabel('Value of q given p=0.3')
plt.ylabel('Probability of winning by starting at state 0509081')
plt.savefig('QS.png')


fr = open('expectation.txt','w')
for i in V:
    fr.write(str(i))
    fr.write('\n')


import getopt, sys
import numpy as np
import time

def extract_distance(X):
    (x,y)=((X-1)%4,int((X-1)/4))
    return(x,y)

def compute_transition(stat,pi,qi,p_opp):
    T = np.zeros((8193,10,8193))
    #------------------------------------------------------------------------------------------
    #FOR PASSING; ACTION=8
    #First for passing
    
    for i in range(8192):
        B1=int((stat[i])[0:2])
        B2=int((stat[i])[2:4])
        pos = int((stat[i])[6])
        b1 = extract_distance(B1)
        b2 = extract_distance(B2)
        #Find list of intermediate states Sr after R moves from initial state i
        Sr=[]
        r_add=[-2,2,-2*4,2*4]
        for k in range(4):
            if p_opp[k,i]!=0:
                Sr.append([p_opp[k,i],i+r_add[k]])
        #Loop over these intermediate states
        interm=0
        for sri in Sr:
            j=sri[1]
            prs = sri[0]
            R=int((stat[j])[4:6])
            r = extract_distance(R)
            if (b1==b2): #B1,B2 on same square
                if (r==b1): #B1,B2,R on same square, prob gets halved
                    if pos==1:
                        T[i,8,j+1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j+1]
                    else:
                        T[i,8,j-1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j-1]
                else: #R not on same square as B1,B2
                    if pos==1:
                        T[i,8,j+1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j+1]
                    else:
                        T[i,8,j-1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j-1]
            elif(b1[0]==b2[0]): #B1,B2 in same column but not on same square
                if r[0]==b1[0] and (r[1]-b1[1])*(r[1]-b2[1])<=0 : #R lies between or on B1,B2
                    if pos==1:
                        T[i,8,j+1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j+1]
                    else: 
                        T[i,8,j-1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j-1]
                else: #R does not lie between or on B1 and B2
                    if pos==1:
                        T[i,8,j+1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j+1]
                    else:
                        T[i,8,j-1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j-1]
            elif(b1[1]==b2[1]): #B1,B2 in same row but not same square
                if r[1]==b1[1] and (r[0]-b1[0])*(r[0]-b2[0])<=0: #R lies on or between B1,B2
                    if pos==1:
                        T[i,8,j+1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j+1]
                    else:
                        T[i,8,j-1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j-1]
                else: #R does not lie between or on B1,B2
                    if pos==1:
                        T[i,8,j+1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j+1]
                    else:
                        T[i,8,j-1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j-1]
            elif(abs((b1[1]-b2[1])/(b1[0]-b2[0]))==1): #B1,B2 lie on 45 deg diagonal
                if (r==b1) or (r==b2): #R lies on B1 or B2
                    if pos==1:
                        T[i,8,j+1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j+1]
                    else:
                        T[i,8,j-1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j-1]
                elif (r[0]==b1[0]): #R lies in the same column as B1
                    if pos==1:
                        T[i,8,j+1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j+1]
                    else:
                        T[i,8,j-1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                        interm += T[i,8,j-1]
                elif (r[1]-b1[1])/(r[0]-b1[0])==(b1[1]-b2[1])/(b1[0]-b2[0])  and (r[0]-b1[0])*(r[0]-b2[0])<0:
                    #Slope is of same diagonal, R lies in between for any 1 coordinate
                    if pos==1:
                        T[i,8,j+1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1])-b2[1])))*prs
                        interm += T[i,8,j+1]
                    else:
                        T[i,8,j-1]=0.5*(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1])-b2[1])))*prs
                        interm += T[i,8,j-1]
                else: #R does not lie between or on B1,B2
                    if pos==1:
                        T[i,8,j+1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1])-b2[1])))*prs
                        interm += T[i,8,j+1]
                    else:
                        T[i,8,j-1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1])-b2[1])))*prs
                        interm += T[i,8,j-1]
            else:
                if pos==1:
                    T[i,8,j+1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                    interm += T[i,8,j+1]
                else:
                    T[i,8,j-1]=(qi-0.1*(max(abs(b1[0]-b2[0]),abs(b1[1]-b2[1]))))*prs
                    interm += T[i,8,j-1]
            T[i,8,8192]=1-interm
    #-----------------------------------------------------------------------------------------------
    #FOR SHOOTING; ACTION=9
    #For shooting a goal, game surely ends. The only difference is in the reward
    #Game either ends with a goal or without a goal
    for i in range(8192):
        T[i,9,8192]=1
    #-------------------------------------------------------------------------------------------------
    #STARTING COMPUTATION FOR MOVEMENT HERE
    #------------------------------------------------------------------------------------------
    for i in range(8192):
        B1=int((stat[i])[0:2])
        B2=int((stat[i])[2:4])
        R_old=int((stat[i])[4:6])
        pos = int((stat[i])[6])
        if (B1==1 or B1==5 or B1==9 or B1==13):
            T[i,0,8192]=1 #You either lose possession or go out of bounds, game ends
        if (B1==4 or B1==8 or B1==12 or B1==16):
            T[i,1,8192]=1 #You either lose possession or go out of bounds, game ends
        if (B1==1 or B1==2 or B1==3 or B1==4):
            T[i,2,8192]=1 #You either lose possession or go out of bounds, game ends
        if (B1==13 or B1==14 or B1==15 or B1==16):
            T[i,3,8192]=1 #You either lose possession or go out of bounds, game ends
        if (B2==1 or B2==5 or B2==9 or B2==13):
            T[i,4,8192]=1 #You either lose possession or go out of bounds, game ends
        if (B2==4 or B2==8 or B2==12 or B2==16):
            T[i,5,8192]=1 #You either lose possession or go out of bounds, game ends
        if (B2==1 or B2==2 or B2==3 or B2==4):
            T[i,6,8192]=1 #You either lose possession or go out of bounds, game ends
        if (B2==13 or B2==14 or B2==15 or B2==16):
            T[i,7,8192]=1 #You either lose possession or go out of bounds, game ends
        Sr=[]
        r_add=[-2,2,-2*4,2*4]
        b_add=[-512,512,-4*512,4*512,-32,32,-4*32,4*32]
        #Compute intermediate states S'
        for k in range(4):
            if p_opp[k,i]!=0:
                Sr.append([p_opp[k,i],i+r_add[k]])
        #Loop over these intermediate states
        interm = np.zeros(8)
        for sri in Sr:
            j=sri[1]
            prs = sri[0]
            R=int((stat[j])[4:6])
            #B1 moves L, action=0
            if(not(B1==1 or B1==5 or B1==9 or B1==13)): #not calculating for terminal state for this action, done above
                B1_new=B1-1
                if(pos==1):
                    if ((R==B1 and B1_new==R_old) or (R==B1_new)): #Tackling, game ends
                        T[i,0,j+b_add[0]]+=0.5*(1-2*pi)*prs #Tackle unsuccessful, move successful
                        interm[0]+=T[i,0,j+b_add[0]]
                    else: #Successful move with ball
                        T[i,0,j+b_add[0]]+=(1-2*pi)*prs
                        interm[0]+=T[i,0,j+b_add[0]]
                else:
                    T[i,0,j+b_add[0]]+=(1-pi)*prs #Successful move without ball
                    interm[0]+=T[i,0,j+b_add[0]]
            #B1 moves R, action=1
            if(not(B1==4 or B1==8 or B1==12 or B1==16)):
                B1_new=B1+1
                if(pos==1):
                    if ((R==B1 and B1_new==R_old) or (R==B1_new)): #Tackling, game ends
                        T[i,1,j+b_add[1]]+=0.5*(1-2*pi)*prs #Tackle unsuccessful, move successful
                        interm[1]+=T[i,1,j+b_add[1]]
                    else: #Successful move with ball
                        T[i,1,j+b_add[1]]+=(1-2*pi)*prs
                        interm[1]+=T[i,1,j+b_add[1]]
                else:
                    T[i,1,j+b_add[1]]+=(1-pi)*prs #Successful move without ball
                    interm[1]+=T[i,1,j+b_add[1]]
            #B1 moves U, action=2
            if(not(B1==1 or B1==2 or B1==3 or B1==4)):
                B1_new=B1-4
                if(pos==1):
                    if ((R==B1 and B1_new==R_old) or (R==B1_new)): #Tackling, game ends
                        T[i,2,j+b_add[2]]+=0.5*(1-2*pi)*prs #Tackle unsuccessful, move successful
                        interm[2]+=T[i,2,j+b_add[2]]
                    else: #Successful move with ball
                        T[i,2,j+b_add[2]]+=(1-2*pi)*prs
                        interm[2]+=T[i,2,j+b_add[2]]
                else:
                    T[i,2,j+b_add[2]]+=(1-pi)*prs #Successful move without ball
                    interm[2]+=T[i,2,j+b_add[2]]
            #B1 moves D, action=3
            if(not(B1==13 or B1==14 or B1==15 or B1==16)):
                B1_new=B1+4
                if(pos==1):
                    if ((R==B1 and B1_new==R_old) or (R==B1_new)): #Tackling, game ends
                        T[i,3,j+b_add[3]]+=0.5*(1-2*pi)*prs
                        interm[3]+=T[i,3,j+b_add[3]]
                    else: #Successful move with ball
                        T[i,3,j+b_add[3]]+=(1-2*pi)*prs
                        interm[3]+=T[i,3,j+b_add[3]]
                else:
                    T[i,3,j+b_add[3]]+=(1-pi)*prs #Successful move without ball
                    interm[3]+=T[i,3,j+b_add[3]]
            #B2 moves L, action=4
            if(not(B2==1 or B2==5 or B2==9 or B2==13)):
                B2_new=B2-1
                if(pos==2):
                    if ((R==B2 and B2_new==R_old) or (R==B2_new)): #Tackling, game ends
                        T[i,4,j+b_add[4]]+=0.5*(1-2*pi)*prs
                        interm[4]+=T[i,4,j+b_add[4]]
                    else: #Successful move with ball
                        T[i,4,j+b_add[4]]+=(1-2*pi)*prs
                        interm[4]+=T[i,4,j+b_add[4]]
                else:
                    T[i,4,j+b_add[4]]+=(1-pi)*prs #Successful move without ball
                    interm[4]+=T[i,4,j+b_add[4]]
            #B2 moves R, action=5
            if(not(B2==4 or B2==8 or B2==12 or B2==16)):
                B2_new=B2+1
                if(pos==2):
                    if ((R==B2 and B2_new==R_old) or (R==B2_new)): #Tackling, game ends
                        T[i,5,j+b_add[5]]+=0.5*(1-2*pi)*prs
                        interm[5]+=T[i,5,j+b_add[5]]
                    else: #Successful move with ball
                        T[i,5,j+b_add[5]]+=(1-2*pi)*prs
                        interm[5]+=T[i,5,j+b_add[5]]
                else:
                    T[i,5,j+b_add[5]]+=(1-pi)*prs #Successful move without ball
                    interm[5]+=T[i,5,j+b_add[5]]
            #B2 moves U, action=6
            if(not(B2==1 or B2==2 or B2==3 or B2==4)):
                B2_new=B2-4
                if(pos==2):
                    if ((R==B2 and B2_new==R_old) or (R==B2_new)): #Tackling, game ends
                        T[i,6,j+b_add[6]]+=0.5*(1-2*pi)*prs
                        interm[6]+=T[i,6,j+b_add[6]]
                    else: #Successful move with ball
                        T[i,6,j+b_add[6]]+=(1-2*pi)*prs
                        interm[6]+=T[i,6,j+b_add[6]]
                else:
                    T[i,6,j+b_add[6]]+=(1-pi)*prs #Successful move without ball
                    interm[6]+=T[i,6,j+b_add[6]]
            #B2 moves D, action=7
            if(not(B2==13 or B2==14 or B2==15 or B2==16)):
                B2_new=B2+4
                if(pos==2):
                    if ((R==B2 and B2_new==R_old) or (R==B2_new)): #Tackling, game ends
                        T[i,7,j+b_add[7]]+=0.5*(1-2*pi)*prs
                        interm[7]+=T[i,7,j+b_add[7]]
                    else: #Successful move with ball
                        T[i,7,j+b_add[7]]+=(1-2*pi)*prs
                        interm[7]+=T[i,7,j+b_add[7]]
                else:
                    T[i,7,j+b_add[7]]+=(1-pi)*prs #Successful move without ball
                    interm[7]+=T[i,7,j+b_add[7]]
        for m in range(8):
            T[i,m,8192]=1-interm[m]
            
    #--------------------------------------------------------------------------------------------------------------------
    return T

def compute_reward(stat,qi,p_opp):
    R=np.zeros((8193,10,8193))
    for i in range(8192):
        pos = int((stat[i])[6]) #Find who has the ball
        B = int((stat[i])[(pos-1)*2:2*pos]) #Find the position of the player who has the ball
        d2 = extract_distance(B)
        #Find list of intermediate states Sr after R moves from initial state i
        Sr=[]
        r_add=[-2,2,-2*4,2*4]
        for k in range(4):
            if p_opp[k,i]!=0:
                Sr.append([p_opp[k,i],i+r_add[k]])
        #Loop over these intermediate states Sr and find respective reward
        for sri in Sr:
            prs=sri[0]
            opp=int((stat[sri[1]])[4:6])
            d1 = extract_distance(8)
            if (opp==8 or opp==12):
                R[i,9,8192]+=0.5*(qi-0.2*(d1[0]-d2[0]))*prs #multiply the probability of ending up in that intermediate state by the probability that a successful goal is scored
            else:
                R[i,9,8192]+=(qi-0.2*(d1[0]-d2[0]))*prs
    return R

if __name__=='__main__':
    start = time.time()
    argument_list = sys.argv[1:]
    options = 'o:p:q:'
    long_options = ['opponent=','p=','q=']
    state = []
    P_opp=np.zeros((4,8192))
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ('-o','--opponent'):
                path = currentValue
                fp = open(path,'r')
                line = fp.readline().strip()
                line = fp.readline().strip()
                i=0
                while line!='':
                    line = line.split(' ')
                    state.append(line[0])
                    P_opp[0,i]=float(line[1])
                    P_opp[1,i]=float(line[2])
                    P_opp[2,i]=float(line[3])
                    P_opp[3,i]=float(line[4])
                    line = fp.readline().strip()
                    i+=1 
                state.append('-1') 
            elif currentArgument in ('p','--p'):
                P=float(currentValue)
            elif currentArgument in ('q','--q'):
                Q=float(currentValue)      
    except getopt.error as err:
        print (str(err))
    numStates = 8193
    numActions = 10
    mdptype = 'episodic'
    transition = compute_transition(state,P,Q,P_opp)
    reward = compute_reward(state,Q,P_opp)
    print('numStates',numStates)
    print('numActions',numActions)
    print('end 8192')
    move_add=[-512,512,-512*4,512*4,-32,32,-32*4,32*4]
    r_mov=[-2,2,-8,8]
    iter = np.argwhere(transition)
    for it in iter:
            print('transition',it[0],it[1],it[2],reward[it[0],it[1],it[2]],transition[it[0],it[1],it[2]])
    print('mdptype episodic')
    print('discount 1')
    
        
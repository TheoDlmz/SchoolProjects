
import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx   
import math

n = 149 #Nombre de noeuds du graphe

def random_choice(L,n): #Fonction pour choisir un élément dans un type iterable non liste
    i = np.random.randint(n)
    return L[i]
        
   

def step(L,n,states): #Fonction qui actualise les états pour une étape t
    (a,b)=random_choice(L,n)
    sa,sb = states[a],states[b]
    if sa > sb: # a prends la plus petite valeur
        a,b = b,a
        sa,sb = sb,sa
    (va,pa) = sa
    (vb,pb) = sb
    if va == vb: #Si valeur égale, on échange la positivité
        states[a] = (vb,pb)
        states[b] = (va,pa)
    else:
        middle = (va+vb)/(2) #on calcule le milieu ainsi que x_i[t+1] et x_j[t+1]
        inf = math.floor(middle)
        sup = math.ceil(middle)
        if inf == sup: #Si valeur égale, a prends la positivité + et b la -
            states[a] = (inf,1)
            states[b] = (sup,0)
        else: #Sinon a prends - et b prends + 
            states[a] = (sup,0)
            states[b] = (inf,1)
    return states
            
def print_majority_vote(n,states,show,i): #Fonction pour afficher le vote majoritaire
    cont = True
    n_ones = 0
    points = []
    for j in range(n):
        if states[j] >= (1,1): #Si le curseur est en "1"
            n_ones += 1
            points.append(j)
    if n_ones == n or n_ones == 0: #Si convergence 
        cont = False
        print("Arrêt après ",i,"étapes")
    if show ==1:
        plt.plot(points,[i//25 for j in range(n_ones)],'ok',markersize=.5)
    elif show ==2:
        n_kind=[0,0,0]
        points=[[],[],[]]
        for j in range(n):
            if states[j] == (1,0):
                n_kind[0] +=1
                points[0].append(j)
            elif states[j] == (1,1):
                n_kind[1] +=1
                points[1].append(j)
            elif states[j] == (2,0):
                n_kind[2] +=1
                points[2].append(j)
        plt.plot(points[0],[i//25 for j in range(n_kind[0])],'o',color="yellow",markersize=0.5)
        plt.plot(points[1],[i//25 for j in range(n_kind[1])],'o',color="orange",markersize=0.5)
        plt.plot(points[2],[i//25 for j in range(n_kind[2])],'o',color="red",markersize=0.5)
    return cont
    

def majority_vote(L,votes,show): #Fonction de vote majoritaire
    n = len(votes)
    states = [(votes[i]*2,0) for i in range(n)] #On initialises les états
    cont = True
    i = 0
    while(cont):
        states = step(L,n,states) #Mise a jour
        i+=1
        if i%25 ==0:
            cont = print_majority_vote(n,states,show,i) #affichage
    v = states[0] #Tous identiques car convergence
    plt.show()
    if v >= (1,1):
        print("Majorité de 1")
    else:
        print("Majorité de 0")


def print_large_majority_vote(n,states,show,i):
    cont = True
    n_ones = 0
    n_zeros = 0
    points = [[],[]]
    for j in range(n):
        if states[j] >= (2,1):
            n_ones += 1
            points[1].append(j)
        elif states[j] <= (1,0):
            n_zeros += 1
            points[0].append(j)
    if n_ones == n or n_zeros == n or (n_ones+n_zeros) ==0:
        cont = False
        print("Arrêt après ",i,"étapes")
    if show ==1:
        plt.plot(points[1],[i//25 for j in range(n_ones)],'o',color="green",markersize=.8)
        plt.plot(points[0],[i//25 for j in range(n_zeros)],'o',color="red",markersize=.8)
    return cont
    

def large_majority_vote(L,votes,show):
    n = len(votes)
    states = [(votes[i]*3,0) for i in range(n)]
    cont = True
    i = 0
    while(cont):
        step(L,n,states)
        i+=1
        if i%25 ==0:
            cont = print_large_majority_vote(n,states,show,i)
    v = states[0]
    plt.show()
    if v >= (2,1):
        print("Majorité de 1")
    elif v <= (1,0):
        print("Majorité de 0")
    else:
        print("Pas de large gagnant")
        
        
def print_quorum_checking(n,states,show,i):
    cont = True
    n_ones = 0
    n_zeros = 0
    points = []

    for j in range(n):
        if states[j] >= (2,1):
            n_ones += 1
            points.append(j)
    if n_ones == n or n_ones == 0:
        cont = False
        print("Arrêt après ",i,"étapes")
    if show ==1:
        plt.plot(points,[i//25 for j in range(n_ones)],'o',color="black",markersize=.5)
    return cont
    

def quorum_checking(L,votes,show):
    n = len(votes)
    states = [(votes[i]*3,0) for i in range(n)]
    cont = True
    i = 0
    while(cont):
        step(L,n,states)
        i+=1
        if i%25 ==0:
            cont = print_quorum_checking(n,states,show,i)
    plt.show()
    v = states[0]
    if v >= (2,1):
        print("Quorum checked on 1")
    else:
        print("Quorum not checked on 1")
        




def random_list(p): #générer une liste aléatoire avec proba p de 1 en chaque item
    L = [np.random.binomial(1,p) for i in range(n)]
    print(sum(L)/len(L))
    return L
    

def random_list_2(p): #générer une liste aléatoire aveci entre 0 et p en chaque item
    L = [np.random.randint(p) for i in range(n)]
    print(sum(L)/len(L))
    return L
    
## Tests

G = nx.complete_graph(n) #notre graphe
L = list(G.edges) #liste des arrêtes
##
votes = random_list(0.5)
majority_vote(L,votes,1)

##
majority_vote(L,votes,2)


##
votes = random_list(1/3)
large_majority_vote(L,votes,1)



##
quorum_checking(L,votes,1)


##
votes = random_list(1/3)
large_majority_vote(L,votes,1)



### BONUS

        
def print_average_precis(n,states,show,s,b,maxv):
    cont = True
    points = [[] for i in range(b)]
    n_points = [0]*b
    res = 0
    for j in range(n):
        i=1
        while states[j] < ((b-i)*maxv,1):
            i+=1
        n_points[b-i] += 1
        points[b-i].append(j)
    for i in range(b):
        if n_points[i] == n:
            cont=False
            res = i
            print("Arrêt après ",s,"étapes")
    if show ==1:
        for i in range(b):
            plt.plot(points[i],[s//25 for j in range(n_points[i])],'o',color=(i/b,(i/b)**2,(i/b)**3),markersize=.8)
    return cont,res
def average_precis(L,votes,show,precis):
    n = len(votes)
    maxv = np.max(votes)
    states = [(votes[i]*precis,0) for i in range(n)]
    cont = True
    i = 0
    while(cont):
        step(L,n,states)
        i+=1
        if i%25 ==0:
            cont,res = print_average_precis(n,states,show,i,precis,maxv)
    plt.show()
    print("The average is between "+str(res*maxv/precis)+" and "+str((res+1)*maxv/precis))
    return i
##

votes = random_list(4/7)
average_precis(L,votes,1,14)
##

votes = random_list(0.348)
P = []
for k in range(1,20):
    P.append(average_precis(L,votes,0,3*k))

plt.plot([i*2 for i in range(1,20)],P)
plt.show()

##

votes = random_list_2(17)
P = []
for k in range(1,20):
    P.append(average_precis(L,votes,0,3*k))

plt.plot([i*2 for i in range(1,20)],P)
plt.show()

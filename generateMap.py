import os
import random
import sys



def generateMap():
    
    fwall = open("data/env_walls.txt","w")
    fvictims = open("data/env_victims.txt","w")
    fsinaisvitais = open("data/sinais_vitais.txt","w")

    walls = []
    victms = []

    for i in range(0, random.randrange(1,100)+1):
        originCoordnatex =random.randrange(0,11)
        originCoordnatey =random.randrange(0,11)
        
        for i in range(0, random.randrange(1,6)+1):
            nextCoordx = random.randrange(-1,1)
            nextCoordy = random.randrange(-1,1)
            if originCoordnatex+nextCoordx < 0 or  originCoordnatex+nextCoordx> 11 or originCoordnatey+nextCoordy < 0 or  originCoordnatey+nextCoordy > 11:
                walls.append((originCoordnatey+nextCoordx,originCoordnatey+nextCoordy))
                originCoordnatex += nextCoordx
                originCoordnatey += nextCoordy
    
    for i in range(0, random.randrange(1,10)+1):
        
        VictimCoordnatex =random.randrange(0,11)
        VictimCoordnatey =random.randrange(0,11)
        Victim = (VictimCoordnatex, VictimCoordnatey)
        
        if Victim not in walls:
            victms.append(Victim)
    
    i =1 

    for w in walls:
        fwall.write("{0},{1}\n".format(w[0],w[1]))

    for v in victms:
        fsinaisvitais.write("{0},18.954033,4.771111,-6.834524,157.992606,19.918640,19.088752,1\n".format(i))
        fvictims.write("{0}, {1}\n".format(v[0],v[1]))    
        i+=1
    fwall.close()
    fvictims.close()
    fsinaisvitais.close()        

    
   

    

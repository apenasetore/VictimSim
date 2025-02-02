import os
import random
import sys



def generateMap():
    
    fwall = open("data/env_walls.txt","w")
    fvictims = open("data/env_victims.txt","w")
    fsinaisvitais = open("data/sinais_vitais.txt","w")
    fenv_size = open("data/env_size.txt","w")

    walls = []
    victms = []

    for i in range(0, random.randrange(2,7)): #select random position 
        originCoordnatex =random.randrange(0,11)
        originCoordnatey =random.randrange(0,11)
        
        for i in range(0, random.randrange(2,7)):
            nextCoordx = random.randrange(-1,2)
            nextCoordy = random.randrange(-1,2)
            if originCoordnatex+nextCoordx >= 0 and  originCoordnatex+nextCoordx <= 11 and originCoordnatey+nextCoordy >= 0 and  originCoordnatey+nextCoordy <= 11:
                walls.append((originCoordnatex+nextCoordx,originCoordnatey+nextCoordy))
                originCoordnatex += nextCoordx
                originCoordnatey += nextCoordy
    
    for i in range(0, random.randrange(20,50)+1):
        
        VictimCoordnatex =random.randrange(0,11)
        VictimCoordnatey =random.randrange(0,11)
        Victim = (VictimCoordnatex, VictimCoordnatey)
        
        if Victim not in walls:
            victms.append(Victim)
    
    i =1 

    for w in walls:
        fwall.write("{0},{1}\n".format(w[0],w[1]))

    for v in victms:
        rand = random.randint(0, 3)
        if rand ==0:
            fsinaisvitais.write("{0},18.954033,4.771111,-6.834524,157.992606,19.918640,19.088752,1\n".format(i))
            fvictims.write("{0}, {1}\n".format(v[0],v[1]))    
            i+=1
        if rand ==1:
            fsinaisvitais.write("{0},18.954033,4.771111,-6.834524,157.992606,19.918640,19.088752,2\n".format(i))
            fvictims.write("{0}, {1}\n".format(v[0],v[1]))    
            i+=1
        if rand ==2:
            fsinaisvitais.write("{0},18.954033,4.771111,-6.834524,157.992606,19.918640,19.088752,3\n".format(i))
            fvictims.write("{0}, {1}\n".format(v[0],v[1]))    
            i+=1
        if rand ==3:
            fsinaisvitais.write("{0},18.954033,4.771111,-6.834524,157.992606,19.918640,19.088752,4\n".format(i))
            fvictims.write("{0}, {1}\n".format(v[0],v[1]))    
            i+=1
        
        
    spawnx =random.randrange(0,11)
    spawny =random.randrange(0,11)
    
    while (spawnx, spawny) in walls:
        spawnx =random.randrange(0,11)
        spawny =random.randrange(0,11)
    fenv_size.write("BASE {0},{1}\nGRID_WIDTH 12\nGRID_HEIGHT 12\nWINDOW_WIDTH 300\nWINDOW_HEIGHT 300\nDELAY 0.01".format(spawnx,spawny))
    
    fenv_size.close()
    fwall.close()
    fvictims.close()
    fsinaisvitais.close()        

    
   

    

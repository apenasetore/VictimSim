## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.

import sys
import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod
from time import sleep

class Explorer(AbstractAgent):
    def __init__(self, env, config_file, resc):
        """ Construtor do agente random on-line
        @param env referencia o ambiente
        @config_file: the absolute path to the explorer's config file
        @param resc referencia o rescuer para poder acorda-lo
        """

        super().__init__(env, config_file)
        
        # Specific initialization for the rescuer
        #self.map = [[0]*12 for i in range(12)] #create the enviroment map with zeros
        self.position = (0,0)
        self.map = {}
        self.resc = resc           # reference to the rescuer agent
        self.rtime = self.TLIM     # remaining time to explore     

    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""

        # No more actions, time almost ended
        if self.rtime < 10.0: 
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            print(self.map)
            self.resc.go_save_victims([],[])
            return False
        
        sleep(0.7)

        possiblemoves = []
        
        for i in range(-1,2):
            for j in range(-1,2):
                newpos = (self.position[0]+i,self.position[1]+j)
                if newpos != self.position and newpos not in self.map.keys():
                    possiblemoves.append(newpos)  
        if  not possiblemoves:
            var = 0
            #to do
        bestmov = possiblemoves[0]
        for mov in possiblemoves:
            if distance(mov) <= distance(bestmov):
                bestmov = mov
        
        dx = bestmov[0]-self.position[0]
        dy = bestmov[1]-self.position[1]
        # dx = random.choice([-1, 0, 1])

        # if dx == 0:
        #    dy = random.choice([-1, 1])
        # else:
        #    dy = random.choice([-1, 0, 1])
       
        # #if self.position in self.map.keys():

        
        # Moves the body to another position
        result = self.body.walk(dx, dy)

        # Update remaining time
        if dx != 0 and dy != 0:
            self.rtime -= self.COST_DIAG
        else:
            self.rtime -= self.COST_LINE

        # Test the result of the walk action
        if result == PhysAgent.BUMPED:
            self.map[(self.position[0]+dx,self.position[1]+dy)] = 1
            #self.map[dx][dy] = 1  # build the map- to do
            # print(self.name() + ": wall or grid limit reached")

        if result == PhysAgent.EXECUTED:
            self.position = (self.position[0]+dx,self.position[1]+dy)
            # check for victim returns -1 if there is no victim or the sequential
            # the sequential number of a found victim
            seq = self.body.check_for_victim()
            if seq >= 0:
                vs = self.body.read_vital_signals(seq)
                self.rtime -= self.COST_READ
                self.map[self.position] = 2
                # print("exp: read vital signals of " + str(seq))
                # print(vs)
            else:
                self.map[self.position] = 0       
        return True

def distance(pos) -> float:
        return pos[0]**2 + pos[1]**2




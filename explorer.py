## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.

import sys
import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod
import time


class Explorer(AbstractAgent):
    def __init__(self, env, config_file, resc):
        """ Construtor do agente random on-line
        @param env referencia o ambiente
        @config_file: the absolute path to the explorer's config file
        @param resc referencia o rescuer para poder acorda-lo
        """

        super().__init__(env, config_file)
        
        # Specific initialization for the rescuer
        self.resc = resc           # reference to the rescuer agent
        self.rtime = self.TLIM     # remaining time to explore     

        self.cost = {}
        self.visited = []
        self.visited.append((0,0))
        self.cost[(0, 0)] = 0.0
        self.timetogo = False
        self.x = 0
        self.y = 0
        self.victims = []
   
    #determine believed cost of moving from (0, 0) to (x, y)
    def determine_cost(self, x, y):
        least_neighbor_cost = 10000
        self.cost[(x, y)] = least_neighbor_cost

        #search the neighbors for the least total cost (cost of the position + cost of move)
        for i in range(-1, 2):
            for j in range(-1, 2):
                print("checking {} {}", i, j)
                if (x+i, y+j) in self.visited and (x+i, y+j) in self.cost.keys() and self.cost[(x+i, y+j)] + (self.COST_LINE if i==0 or j==0 else self.COST_DIAG) < least_neighbor_cost:
                    print("is less")
                    least_neighbor_cost = self.cost[(x+i, y+j)] + (self.COST_LINE if i==0 or j==0 else self.COST_DIAG)
        self.cost[(x, y)] = least_neighbor_cost

        print(least_neighbor_cost)
        return self.cost[(x, y)]

    def deliberate(self) -> bool:
        
        #time.sleep(0.24)
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""
        #print(self.cost)
        # No more actions, time almost ended
        if self.x == 0 and self.y == 0 and self.timetogo: 
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            for pos in self.cost.keys():
                if pos not in self.visited:
                    self.cost[pos] = 1000
                    
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            self.resc.go_save_victims(self.cost,self.victims)
            return False
        
        dx = random.choice([-1, 0, 1])

        if dx == 0:
           dy = random.choice([-1, 1])
        else:
           dy = random.choice([-1, 0, 1])

        #determine cost of all possible moves and takes the one with least cost
        least_move_cost = 10000
        return_cost = 10000
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (self.x+i, self.y+j) not in self.cost.keys():
                    move_cost = self.determine_cost(self.x+i, self.y+j)
                else:
                    move_cost = self.cost[(self.x+i, self.y+j)]
                
                if (self.x+i, self.y+j) in self.visited and self.cost[(self.x+i, self.y+j)] < return_cost:
                    self.goback = (i, j)
                    return_cost = self.cost[(self.x+i, self.y+j)]

                if move_cost < least_move_cost and (i != 0 or j != 0) and (self.x+i, self.y+j) not in self.visited:
                    least_move_cost = move_cost
                    dx = i
                    dy = j

        if self.rtime < return_cost + self.COST_DIAG + self.COST_LINE:
            self.timetogo = True
            print("Voltar")
        if self.timetogo:
            dx = self.goback[0]
            dy = self.goback[1]

        # Moves the body to another position
        result = self.body.walk(dx, dy)
        #print(dx)
        #print(dy)
        print("tempo q me resta"+str(self.rtime))
        print("tempo para voltar"+str(return_cost))

        # Update remaining time
        if dx != 0 and dy != 0:
            self.rtime -= self.COST_DIAG
        else:
            self.rtime -= self.COST_LINE
        # Test the result of the walk action
        if result == PhysAgent.BUMPED:
            walls = 1  # build the map- to do
            self.cost[(self.x+dx, self.y+dy)] = 10000
            # print(self.name() + ": wall or grid limit reached")

        if result == PhysAgent.EXECUTED:
            self.x += dx
            self.y += dy
            # check for victim returns -1 if there is no victim or the sequential
            # the sequential number of a found victim
            if (self.x, self.y) not in self.visited: 
                seq = self.body.check_for_victim()
                if seq >= 0:
                    vs = self.body.read_vital_signals(seq)
                    self.victims.append(((self.x, self.y),vs))

                    self.rtime -= self.COST_READ
                    # print("exp: read vital signals of " + str(seq))
                    # print(vs)
        self.visited.append((self.x, self.y))
       
        return True


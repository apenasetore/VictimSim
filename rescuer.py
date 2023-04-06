##  RESCUER AGENT
### @Author: Tacla (UTFPR)
### Demo of use of VictimSim

import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod
from heap import min_heap

## Classe que define o Agente Rescuer com um plano fixo
class Rescuer(AbstractAgent):
    def __init__(self, env, config_file):
        """ 
        @param env: a reference to an instance of the environment class
        @param config_file: the absolute path to the agent's config file"""

        super().__init__(env, config_file)

        # Specific initialization for the rescuer
        self.plan = []              # a list of planned actions
        self.rtime = self.TLIM      # for controlling the remaining time

        # Starts in IDLE state.
        # It changes to ACTIVE when the map arrives
        self.body.set_state(PhysAgent.IDLE)

        # planning
        self.__planner()
    
    def go_save_victims(self, cost, victims):
        self.map = cost.keys()
        self.victims  = victims
        self.victims_cost = {}
        print(victims)
        self.origin_cost = self.generate_cost((0,0))
        
        for v in self.victims:
            self.victims_cost[v[0]] = self.generate_cost(v[0])
            print(self.victims_cost[v[0]])
            print("\n")
        """ The explorer sends the map containing the walls and
        victims' location. The rescuer becomes ACTIVE. From now,
        the deliberate method is called by the environment"""
        self.body.set_state(PhysAgent.ACTIVE)
    def generate_cost(self, origin):
        
        costs = {}
        frontier = min_heap()
        frontier.insert((0,origin))
        
        while frontier.size > 0:
            least_cost_pos = frontier.pop()
            x = least_cost_pos[1][0]
            y = least_cost_pos[1][1]
            costs[least_cost_pos[1]] = least_cost_pos[0]
            
            for i  in range(-1,2):
                for j  in range(-1,2):
                    if (i+x,j+y) not in costs.keys() and not frontier.is_in((i+x,j+y)) and (i+x,j+y) in self.map:
                        if i != 0 and j != 0:
                            frontier.insert((least_cost_pos[0]+self.COST_DIAG,(x+i,y+j)))
                        else:
                            frontier.insert((least_cost_pos[0]+self.COST_LINE,(x+i,y+j)))
                    
                    if frontier.is_in((x+i,y+j)):
                        if i != 0 and j != 0:
                            frontier.decrease_key((x+i,y+j),least_cost_pos[0]+self.COST_DIAG)
                        else:
                            frontier.decrease_key((x+i,y+j),least_cost_pos[0]+self.COST_LINE)
        return costs
                        
    def __planner(self):
        """ A private method that calculates the walk actions to rescue the
        victims. Further actions may be necessary and should be added in the
        deliberata method"""

        # This is a off-line trajectory plan, each element of the list is
        # a pair dx, dy that do the agent walk in the x-axis and/or y-axis
        self.plan.append((0,1))
        self.plan.append((1,1))
        self.plan.append((1,0))
        self.plan.append((1,-1))
        self.plan.append((0,-1))
        self.plan.append((-1,0))
        self.plan.append((-1,-1))
        self.plan.append((-1,-1))
        self.plan.append((-1,1))
        self.plan.append((1,1))
        
    def deliberate(self) -> bool:
        """ This is the choice of the next action. The simulator calls this
        method at each reasonning cycle if the agent is ACTIVE.
        Must be implemented in every agent
        @return True: there's one or more actions to do
        @return False: there's no more action to do """

        # No more actions to do
        if self.plan == []:  # empty list, no more actions to do
           return False

        # Takes the first action of the plan (walk action) and removes it from the plan
        dx, dy = self.plan.pop(0)

        # Walk - just one step per deliberation
        result = self.body.walk(dx, dy)

        # Rescue the victim at the current position
        if result == PhysAgent.EXECUTED:
            # check if there is a victim at the current position
            seq = self.body.check_for_victim()
            if seq >= 0:
                res = self.body.first_aid(seq) # True when rescued             

        return True


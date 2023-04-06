class darwin:
    def __init__(self,victims,victim_cost, origin_cost,ttime):
        
        self.populacao = []
        self.victims = victims
        self.victim_cost = victim_cost
        self.origin_cost = origin_cost
        self.gene_size = len(self.victim_cost)
        self.ttime = ttime
   
    def gene_fitness(self,gene):
        rescue_factor = 0
        sum_cost = 0
        origin = (0,0)
        for g in gene:
            
            if g > 0 :
                rescue_factor += 1 
                sum_cost += self.victim_cost[self.victims[g-1][0]][origin]
                origin = self.victims[g-1][0]
            
            else:
                if self.victims[-g-1][1][7] == 1:
                    rescue_factor += 0.9
                elif self.victims[-g-1][1][7] == 2:
                    rescue_factor += 0.75
                elif self.victims[-g-1][1][7] == 3:
                    rescue_factor += 0.5
            sum_cost += self.origin_cost[origin]
            
            if self.ttime < sum_cost:
                rescue_factor *= 0.1
        return rescue_factor
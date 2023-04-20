import random
class darwin:
    def __init__(self,victims,victim_cost, origin_cost,ttime):
        
        self.population_size = len(victims)
        self.population = []
        self.population_fitness = []
        self.victims = victims
        self.victim_cost = victim_cost
        self.origin_cost = origin_cost
        self.gene_size = len(self.victim_cost)
        self.ttime = ttime

        #generate initial genes
        #produces rotated sequences
        #e.g.
        #[1, 2, 3, 4, 5] [2, 3, 4, 5, 1] [3, 4, 5, 1, 2] ...

        for i in range(0, self.population_size):
            new_gene = []
            j = i+1
            for k in range(0, self.gene_size):
                new_gene.append(j)
                j+=1
                if j > self.gene_size:
                    j = 1
            self.population.append(new_gene)
            self.population_fitness.append(self.gene_fitness(new_gene))

    def run_generation(self):
        self.crossing_over()
        self.natural_selection()
        #print(self.gene_fitness(self.get_best()))
        return self.gene_fitness(self.get_best())

    def get_best(self):
        if (not self.population):
            return -1
        best = 0
        for j in range(0, len(self.population)): 
            if self.population_fitness[best] < self.population_fitness[j]:
                best = j
        #print(self.population)
        return self.population[best]
   
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

    def crossing_over(self):
        
        gene_probab = []
        gene_son = []
        gene_son_fitness =[]
        rescue_factor_total = 0

        for g in self.population:
            rescue_factor_total += self.gene_fitness(g)
        for g in self.population:
            gene_probab.append(self.gene_fitness(g)/rescue_factor_total)
        
        for i in range(0,self.population_size//2):#create half the population size of childreen
            gene_parents = random.choices(self.population, weights=gene_probab, k = 2)
            gene_son.append(self.mate(gene_parents))
            gene_son_fitness.append(self.gene_fitness(gene_son[i]))
        self.population.extend(gene_son)
        self.population_fitness.extend(gene_son_fitness)
    
    def mate(self,parents):
        
        child = []
        victims_to_be_save = list(range(1,len(self.victims)+1)) 
        for i in range(0, len(parents[0])):#
            choice= random.randrange(0,2)
            c_new = parents[choice][i]            
            if c_new not in child and -c_new not in child:
                child.append(c_new)
                victims_to_be_save.remove(abs(c_new))
            else:
                child.append(0)
        for i in range(0,len(child)):
            if child[i] == 0:
                g = random.choice(victims_to_be_save)
                victims_to_be_save.remove(g)
                genes = [g,-g]
                child[i] = random.choice(genes)      
        mutation = random.randrange(1,11)
        if mutation == 1:
            i = random.randrange(0,len(child))
            j = random.randrange(0,len(child))
            aux = child[i]
            child[i] = child[j]
            child[j] = aux
        
        mutation = random.randrange(1,11)
        if mutation == 1:
            i = random.randrange(0,len(child))
            child[i] = -child[i]
        
        mutation = random.randrange(1,11)
        if mutation == 1:
            i = random.randrange(0,len(child))
            j = random.randrange(0,len(child))
            aux = child[i]
            child[i] = child[j]
            child[j] = aux
        
        mutation = random.randrange(1,11)
        if mutation == 1:
            i = random.randrange(0,len(child))
            child[i] = -child[i]
            

        return child    
    
    def natural_selection(self):
            
        for i in range(0, self.population_size//2): #makes the population size return to the fixed number after reproduction
            worst = 0
            for j in range(0, len(self.population)): 
                if self.population_fitness[worst] > self.population_fitness[j]:
                    worst = j
            del self.population[worst]
            del self.population_fitness[worst] 
                


            

                
                
            
         

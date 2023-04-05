def fronteira(victim):
    
    front = []
    
    for i in range (-1,2):
        for j in range(-1,2):
            if (x+i,y+j) in self.cost.keys() and self.cost.keys((x+i,y+j)) == 1000 and (x+i, y+j) not in front:
                front.append(x+i,y+j)
    
                
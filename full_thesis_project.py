#!/usr/bin/env python
# coding: utf-8

# In[4]:


import random 
import time


start_time = time.process_time()


# getting the original sequence 
f = open("original_sequence.txt","r")
a = []
for lines in f:
    i = int(lines)
    a.append(i)
f.close()

# getting the original makespan
#float original_makespan
f = open("original_makespan.txt","r")
for lines in f:
    original_makespan = float(lines)
f.close()

# generating the original population
#a =[0, 1, 2, 3]
c =[]
e = []
population = 5000
for i in range(population):
    d = []
    e = a.copy()
    for j in range(len(e)):
        b = e.pop(random.randrange(len(e)))
        d.append(b)
    c.append(d)       
#print(c)

def fitness_calculation(given_seq):
    makespan = main(given_seq)
    return makespan

def finding_fitness(fitness_couple):
    makespan_seq = []
    f = open("seq_makespan.txt","w")
    for i in fitness_couple:
        i_makespan = main(i)
        i_couple = (i,i_makespan)
        makespan_seq.append(i_couple)
        f.writelines(str(i_couple)+"\n")
    f.close()
    return(makespan_seq)

def selection(ch):
    # select members for reproduction
    sel_population = []
    for i in range(int(len(ch)/2)):
        f = ch.pop(random.randrange(len(ch)))
        g = ch.pop(random.randrange(len(ch)))
        indx_f = f[1]
        indx_g = f[1]
        if indx_f> indx_g:#fitness
            sel_population.append(f[0])
        else:
            sel_population.append(g[0])
    return sel_population
#print(selection(c))

def crossover(new_population):
    # crossover
    cross_population=[]
    #new_population = selection(ch)
    for i in range(int(len(new_population)/2)):
        parentx = new_population.pop(random.randrange(len(new_population)))
        parenty = new_population.pop(random.randrange(len(new_population)))
        offspring = []
        for i in range(len(parenty)):
            offspring.append(i)
        x = random.randrange(len(parentx))
        y = random.randint(x,len(parentx))
        for i in range((len(parentx)-1),-1,-1):
            if i>y :
                offspring[i] = parenty[i]
            elif i<=y and i>=x:
                offspring[i] = parentx[i]
            elif i<x:
                offspring[i]= parenty[i]
        '''
        for i in range(len(offspring)):
            for j in range(len(offspring)):
                if offspring[i] == offspring[j] and i!=j:
                    if i<x:
                        offspring[i] = parenty[j]
                    elif i>y:
                        offspring[i] = parenty[j]
        cross_population.append(offspring)
        '''
        for i in range(len(offspring)):
            for j in range(i+1,len(offspring)):
                if offspring[i] == offspring[j]:
                    if i < x :
                        if j >= x and j <= y : 
                            if parenty[i] == offspring[i]:
                                to_change = offspring[i]
                                for z in parentx:
                                    if z not in offspring:
                                        offspring[i] = z
                                        break
                    elif i >= x and i <= y:
                        if j > y:
                            if parenty[j] == offspring[j]:
                                if parenty[i] not in offspring:
                                    offspring[j] = parenty[i]
                                else:
                                    for z in parenty:
                                        if z not in offspring:
                                            offspring[j]= z
                                            break
        cross_population.append(offspring)
    return cross_population

def mutation(mutated):
    #mutation
    m_population = []
    m_rate = 0.01
    #mutated = crossover(mutated_population)
    for i in mutated:
        j = random.random()
        if j <= m_rate:
            h = i[random.randrange(len(i))]
            l = i[random.randrange(len(i))]
            temp = i[h]
            i[h]=i[l]
            i[l] = temp
            m_population.append(i) 
        else:
            m_population.append(i)
    return m_population

generations = 3
def genetic_algorithm(initial_pop):
    initial_set = finding_fitness(initial_pop)
    initial_selection = selection(initial_set)
    initial_crossover = crossover(initial_selection)
    initial_mutation = mutation(initial_crossover)
    initial_g = initial_mutation
    return initial_g
    
    
starting_gen = genetic_algorithm(c)
answers_makespan = []
for i in starting_gen:
    find_makespan = fitness_calculation(i)
    answers_makespan.append((i,find_makespan))
print(f"------------for original generation------------")
for il in answers_makespan:
    print(il)
possibles_smallest_couple = answers_makespan[0]
possibles_smallest_couple = list(possibles_smallest_couple)
possibles_smallest = possibles_smallest_couple[1]
for z in range(len(answers_makespan)-1):
    zs_answer = answers_makespan[z]
    zis_answer = answers_makespan[z+1]
    if zs_answer[1] > zis_answer[1]:
        if zs_answer[1] > possibles_smallest:
            possibles_smallest = zs_answer[1]
            possibles_smallest_couple[1] = possibles_smallest
            possibles_smallest_couple[0] = zs_answer[0]
        else:
            possibles_smallest = possibles_smallest
            possibles_smallest_couple[1] = possibles_smallest
            possibles_smallest_couple[0] = possibles_smallest_couple[0]
    else:
        if zis_answer[1] < possibles_smallest:
            possibles_smallest = possibles_smallest
            possibles_smallest_couple[1] = possibles_smallest
            possibles_smallest_couple[0] = possibles_smallest_couple[0]
        else:
            possibles_smallest = zis_answer[1]
            possibles_smallest_couple[1] = possibles_smallest
            possibles_smallest_couple[0] = zis_answer[0]
print(f"------------fittest makespan after original generation------------")
print(possibles_smallest_couple)

answers_makespan.clear()
#print(starting_gen)
for i in range(generations):
        
    next_g = genetic_algorithm(starting_gen)
    print(f" ------------for generation {i+1}------------")
    for j in next_g:
        find_makespan = fitness_calculation(j)
        answers_makespan.append((j,find_makespan))
    #print(next_g)
    for il in answers_makespan:
        print(il)
    possible_smallest_couple = answers_makespan[0]
    possible_smallest_couple = list(possible_smallest_couple)
    possible_smallest = possible_smallest_couple[1]
    for z in range(len(answers_makespan)-1):
        z_answer = answers_makespan[z]
        zi_answer = answers_makespan[z+1]
        if z_answer[1] > zi_answer[1]:
            if z_answer[1] > possible_smallest:
                possible_smallest = z_answer[1]
                possible_smallest_couple[1] = possible_smallest
                possible_smallest_couple[0] = z_answer[0]
            else:
                possible_smallest = possible_smallest
                possible_smallest_couple[1] = possible_smallest
                possible_smallest_couple[0] = possible_smallest_couple[0]
        else:
            if zi_answer[1] < possible_smallest:
                possible_smallest = possible_smallest
                possible_smallest_couple[1] = possible_smallest
                possible_smallest_couple[0] = possible_smallest_couple[0]
            else:
                possible_smallest = zi_answer[1]
                possible_smallest_couple[1] = possible_smallest
                possible_smallest_couple[0] = zi_answer[0]

    print(f"------------fittest makespan after {i+1} generation------------")
    print(possible_smallest_couple)
    answers_makespan.clear()
    starting_gen = next_g    
    
end_time = time.process_time()
print("process time:", end_time-start_time)
        
#genetic_algorithm(c)


# In[1]:


import simpy
import random


hours = 12
days = 100

working_time = hours * days
total_time = float(working_time)

cm=0
dm=0



#containers
    #boards
boards_capacity=50
initial_boards=0 

    #components
components_capacity = 150000
initial_components=50000
components_needed=0

    #reflow
pcb_reflow = 1500 

    #waiting_area
pcb_inspect = 1250
boards_ready_capacity = 2
reflow_ready_capacity = 5
inspection_ready_capacity = 10
packaged_goods = 0

    #critical stocks
components_critical_stock= 1000
boards_critical_stock=10

    #setup_time
setup_coefficient=0
batch_size=0
batch =0


f = open("original_sequence.txt","r")
a = []
for lines in f:
    i = int(lines)
    a.append(i)
f.close()


f = open("specifications.txt","r")
new_pecs = []
for lines in f:
    o = int(lines)
    new_pecs.append(o)    
f.close()

specs = []
under_pecs =[]
li = len(new_pecs)
tli = int(li/4)
for j in range(tli):
    under_pecs.append(new_pecs[0])
    under_pecs.append(new_pecs[1])
    under_pecs.append(new_pecs[2])
    under_pecs.append(new_pecs[3])
    n_under_pecs = under_pecs.copy()
    specs.append(n_under_pecs)
    new_pecs.pop(3)
    new_pecs.pop(2)
    new_pecs.pop(1)
    new_pecs.pop(0)
    #n_under_pecs =[]
    under_pecs.pop(3)
    under_pecs.pop(2)
    under_pecs.pop(1)
    under_pecs.pop(0)

#print(specs)
f = open("simCoefficient.txt","r")
sim = []
for lines in f:
    i = float(lines)
    sim.append(i)
f.close()
#print(nono_trans)
#print(sim)

f = open("coupleCoefficient.txt","r")
#new_l = []
#new_l2 = []
#for lines in f:
    #new_l.append(lines)
#print(new_l)
#for i in new_l:
    
    #new_i = i.replace("\n","")
    #new_l2.append(new_i)
    #print(new_i)
#print(new_l2)
couple = []
#for i in new_l2:
    #ij = int(i[:2])
    #il = int(i[2:])
    #new_t = (ij,il)
    #couple.append(new_t)
for line in f:
    aline =line
    for i in range(len(aline)):
        if line[i]==",":
            first_part = int(line[1:i])
            snd_part = int(line[i+1:-2])
            
        else:
            continue
        new_t = (first_part,snd_part)
        couple.append(new_t)
#print(final_l)
f.close()
#print(couple)





class Pcb_process:
    def __init__(self,env):
        self.boards= simpy.Container(env, capacity = boards_capacity, init = initial_boards)
        self.boards_ready = simpy.Container(env, capacity = boards_ready_capacity, init = 0)
        self.setup=simpy.Container(env, capacity = batch_size, init = batch)
        self.components = simpy.Container(env, capacity = components_capacity, init = initial_components)
        self.components_control = env.process(self.components_stock_control(env))
        self.reflow_ready = simpy.Container(env, capacity = reflow_ready_capacity, init = 0)
        #self.points = simpy.Container(env, capacity = , init = 0)
        self.reflow = simpy.Container(env ,capacity =pcb_reflow , init = 0)
        self.inspection_ready = simpy.Container(env, capacity = inspection_ready_capacity, init = 0)
        self.packaging_ready = simpy.Container(env ,capacity =pcb_inspect , init = 0)
        self.packaging_done = env.process(self.packaging_ready_control(env))
        #self.dispatch_control = env.process(self.dispatch_guitars_control(env))    


    def components_stock_control(self, env):
        yield env.timeout(0)
        while True:
            if self.components.level <= components_critical_stock:
                yield env.timeout(2)
                yield self.components.put(25000)
                yield env.timeout(1)
            else:
                yield env.timeout(0.5)
                
    def packaging_ready_control(self, env):
        global packaged_goods
        yield env.timeout(0)
        while True:
            if self.packaging_ready.level >= 50:
                yield env.timeout(1)
                packaged_goods += self.packaging_ready.level
                yield self.packaging_ready.get(self.packaging_ready.level)
                yield env.timeout(1)
            else:
                yield env.timeout(0.5)
                
def setting_up(env, pcb_process):
    yield env.timeout(1)
    while True:
        yield pcb_process.setup.get(50)
        set_up= 2-2*setup_coefficient
        yield env.timeout(set_up)
        yield pcb_process.boards.put(boards_capacity)

            
            
def boards_solder(env, pcb_process):
    while True:
        yield pcb_process.boards.get(1)
        body_time = 0.05
        yield env.timeout(body_time)
        yield pcb_process.boards_ready.put(1)
        #cm= (env.now%12)
        #dm=(int(env.now/12))
        #print('----- pcb pasted at day {0}, hour {1} -----'.format(dm, cm))

def assembler(env, pcb_process):
    while True:
        yield pcb_process.boards_ready.get(1)
        yield pcb_process.components.get(components_needed)
        assembling_time = 0.002*components_needed+0.001*points_needed
        yield env.timeout(assembling_time)
        yield pcb_process.reflow_ready.put(1)
        #cm= (env.now%12)
        #dm=(int(env.now/12))
        #print('----- pcb components soldered at day {0}, hour {1} -----'.format(dm, cm))
        
def reflow_oven(env, pcb_process):
    while True:
        yield pcb_process.reflow_ready.get(1)
        assembling_time = 0.07
        yield env.timeout(assembling_time)
        yield pcb_process.inspection_ready.put(1)
        #cm= (env.now%12)
        #dm=(int(env.now/12))
        #print('----- pcb dried at day {0}, hour {1} -----'.format(dm, cm))
        
def inspect(env, pcb_process):
    global cm
    global dm
    while True:
        yield pcb_process.inspection_ready.get(1)
        inspection_time = 0.1
        yield env.timeout(inspection_time)
        yield pcb_process.packaging_ready.put(1)
        cm= (env.now%12)
        dm=(int(env.now/12))
        #print('--------------- pcb finished at day {0}, hour {1} ---------------'.format(dm, cm))
    

def main(n_seq):
    a_n = len(n_seq)
    global working_time
    temp_time = 0
    old_seq = a
    for i in range(0,a_n):
        global total_time
        global working_time
        global boards_initial
        global boards_capacity
        global components_needed
        global points_needed
        global setup_coefficient
        global batch_size
        global batch
        global cm
        global dm
        #print(f'-------------------- Starting order {i+1} --------------------')
        old_to_new = old_seq.index(n_seq[i])
        batch_size = specs[old_to_new][0]
        batch = specs[old_to_new][0]
        #boards_capacity = specs[i][0]
        #initial_boards = specs[i][0]
        components_needed = specs[old_to_new][3]
        points_needed = specs[i][2]
        if i+1<a_n:
            el= (specs[i][3], specs[i+1][3])


            if el in couple:
                pst = couple.index(el)
                setup_coefficient= sim[pst]

            else:
                continue


        env = simpy.Environment()
        pcb_process = Pcb_process(env)

        boards_solder_process = env.process(boards_solder(env, pcb_process))
        assembler_process = env.process(assembler(env, pcb_process))
        reflow_oven_process = env.process(reflow_oven(env, pcb_process))
        inspect_process = env.process(inspect(env, pcb_process))
        setup_process = env.process(setting_up(env, pcb_process))

        env.run(until = total_time)
        #end_event = env.event()
        #print(f'-------------------- Dispatch has %d pcb ready to inspect! --------------------' % pcb_process.packaging_ready.level)
        #print('wood supplier arrives at day {0}, hour {1}'.format(int(env.now/8), env.now % 8))

        #total_time=total_time-(initial_boards*(0.05+(components_needed*0.002)+0.07+0.1))#wrong calculation
        total_time = total_time - (dm*12+cm)
        temp_time = total_time
    
    total_time = float(working_time)
    #end_event.succeed()
    #return (f"-------------------- The makespan is: {temp_time} --------------------")
    return temp_time   
    
#print(batch_size)
#print(total_time)


# In[35]:


for i in range(3):
    v = main2([0,1,2])
    d = main2([0,2,1])
print(v)
print(d)


# In[61]:


fe = 100
fr = 30
ft =fe*fr
fy = ft
fy =fy - 400
print(ft)
print(fy)
print(ft)
    


# In[86]:


main([0,1,2])


# In[87]:


main([2,1,0])


# In[88]:


main([0,2,1])


# In[77]:


main([2,0,1])


# In[76]:


main([1,0,2])


# In[39]:


main([1,2,0])


# In[61]:


liste = [1,2,3,4]
for i in range(len(liste)):
    if i != len(liste)-1:
        j = liste[i]+liste[i+1]
        print(j)
    else:
        break


# In[2]:


listr = [(76,87),(87,100),(76,100)]
t_search = (100,87)
t_found = listr.index(t_search)
print(t_found)


# In[33]:


listu = [1,4,2,0,3]
listy = [5,1,2,3,4]
listu_found = listy.index(5)
print(listu_found)


# In[99]:


f = open("original_population.txt","w")
for i in c:
    f.writelines(str(i)+"\n")
f.close()


# In[101]:


def finding_fitness(fitness_couple):
    makespan_seq = []
    f = open("seq_makespan.txt","w")
    for i in fitness_couple:
        i_makespan = main(i)
        i_couple = (i,i_makespan)
        makespan_seq.append(i_couple)
        f.writelines(str(i_couple)+"\n")
    f.close()


# In[102]:


print(makespan_seq)


# In[130]:


whatio = [(4,4),(3,3),(5,5),(6,6),(3,3),(2,2),(7,7),(9,9),(8,8),(0,0)]
whatio_n = 4
for i in range(0,len(whatio)-1):
    io = whatio[i]
    jo = whatio[i+1]
    if io[1] > jo[1]:
        if whatio_n > io[1]:
            whatio_n = whatio_n
        else:
            whatio_n = io[1]
    else:
        if whatio_n < jo[1]:
            whatio_n = jo[1]
        else:
            whation_n = whation_n
    print(f"n:{whatio_n}")


# In[44]:


print(f"------------fittest individual------------")
print([[1, 2, 0], 289.4469518716566])


# In[14]:


main([2,1,0])


# In[6]:


def lanmed(a):
    return(f'--------{a+1}--------')


# In[7]:


lanmed(5)


# In[20]:


for i in range(10):
    print(i)


# In[40]:


flind = finding_fitness(c)
flind_1 = selection(flind)
for i in flind_1:
    print(i)


# In[41]:


flind_3 = crossover(flind_1)
print(f'-----offspring-----')
for i in flind_3:
    print(i)


# In[42]:


flind_4 = mutation(flind_3)
print(f'-----mutation-----')
for i in flind_4:
    print(i)


# In[164]:


print("120. [4,3,2,1,0],",main([4,3,2,1,0]))


# In[172]:


f = open("trytoseelimit.txt", "w")
for i in c:
    line = str(i)
    f.writelines(line)
    f.writelines("\n")
f.close()


# In[14]:


c =[]
e = []
population = 5000
for i in range(population):
    d = []
    e = a.copy()
    for j in range(len(e)):
        b = e.pop(random.randrange(len(e)))
        d.append(b)
    c.append(d)


# In[15]:


finding_fitness(c)


# In[185]:


print(packaged_goods)


# In[ ]:





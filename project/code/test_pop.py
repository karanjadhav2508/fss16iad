import random
import sys
import subprocess
import os,time
import uuid
import logging
import parse
import json
import array
from contextlib import contextmanager
import numpy
import time

from math import sqrt

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence#, hypervolume
from deap import creator
from deap import tools



logging.basicConfig(filename='project.log',filemode='w',format='%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

B_RP = (1000,2000)
S_RP = (1,100)
B_IP = S_RP
S_IP = B_RP
Tb = (50,100)
TbB =(20,40)
Ts = (50,100)
TsB = (48,49)
bCinc = (100,200)
bBinc = (1,3)
sCdec = (100,200)
sBdec = (1,3)
Kb = (1,2)
Ks = (8,9)
Offset = (10000,15000)

prism_path = "/home/adhuri/prism-4.3.1-linux64/bin/prism"
#pop_size = 8

@contextmanager
def duration():
  t1 = time.time()
  yield
  t2 = time.time()
  print("\n" + "-" * 72)
  print("# Runtime: %.3f secs" % (t2-t1))


def ok(decs):
    if(decs[2] >= decs[0]):return False     #B_IP >= B_RP
    if(decs[1] >= decs[3]):return False     #S_RP >= S_IP
    if(decs[4] <= 0):return False           #Tb <= 0
    if(decs[6] <= 0):return False           #Ts <= 0
    if(decs[5] >= decs[4]):return False     # TbB >= Tb
    if(decs[7] >= decs[6]):return False     #TsB >= Ts

    return True

def aop_decs():
    decs = gen_decs()
    while not ok(decs):
        decs = gen_decs
    return decs

def gen_decs():
	b_rp = random.randint(B_RP[0], B_RP[1])
	s_rp = random.randint(S_RP[0], S_RP[1])
	tb = random.randint(Tb[0], Tb[1])
	tbb = random.randint(TbB[0], TbB[1])
	ts = random.randint(Ts[0], Ts[1])
	tsb = random.randint(TsB[0], TsB[1])
	bcinc = random.randint(bCinc[0], bCinc[1])
	bbinc = random.randint(bBinc[0], bBinc[1])
	scdec = random.randint(sCdec[0], sCdec[1])
	sbdec = random.randint(sBdec[0], sBdec[1])
	kb = random.randint(Kb[0], Kb[1])
	ks = random.randint(Ks[0], Ks[1])
	offset = random.randint(Offset[0], Offset[1])
	return [b_rp, s_rp, s_rp, b_rp, tb, tbb, ts, tsb, bcinc, bbinc, scdec, sbdec,  kb, ks, offset]


creator.create("Fitness", base.Fitness, weights=(4.0, -1.0, 1.0),crowding_dist=None)
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("decs", aop_decs)
toolbox.register("gen_one", tools.initIterate, creator.Individual, toolbox.decs)
toolbox.register("population", tools.initRepeat, list, toolbox.gen_one)

#pop = toolbox.population(n=pop_size)


def prism(individual):
	global prism_path
	filename = parse.call_prism(prism_path,individual)
	evaluated_results =parse.Parse(filename).get_output()
	#print evaluated_results
	logging.debug (filename +" : "+ str(evaluated_results))
	if evaluated_results:
		return evaluated_results
	else:
		return (0,0,0)
	"""
	print "Print",individual
	return (random.randint(0,1),random.randint(0,2000),random.randint(0,2000))
	"""

def evaluateInd(individual):
    # Do some computation
	#print "Individual", individual;
	return prism(individual)
	#return random.randint(0,4),random.randint(0,4),random.randint(0,4)



toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low = 0 , up = 1, indpb=0.01)
toolbox.register("select", tools.selNSGA2)
toolbox.register("evaluate", evaluateInd)



def main(seed=None):
    random.seed(seed)

    NGEN = 100       # Generation
    MU = 100      # Population Size
    CXPB = 0.9
	
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)
    
    print ("Algorithm = NSGA2")
    print "Generation = ",NGEN
    print "Population Size = ",MU
    	
    print ("Initial Population")
    for p in pop:
	print p
    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))
    
    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]
        
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

    #print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

    return pop, logbook
        
if __name__ == "__main__":
    # with open("pareto_front/zdt1_front.json") as optimal_front_data:
    #     optimal_front = json.load(optimal_front_data)
    # Use 500 of the 1000 points in the json file
    # optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 2))
    
    with duration():
        pop, stats = main()


    
    import matplotlib.pyplot as plt
    import numpy
    
    print " Final Population "
    for i in pop :
	print i,i.fitness.values
    	   
    front = numpy.array([ind.fitness.values for ind in pop if ind.fitness.values[0]== 1 ])
    #optimal_front = numpy.array(pop)
    #plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
    #plt.scatter(front[:,0], front[:,1], c="b")
    plt.scatter(front[:,2] , front[:,1],c=front[:,0])
    plt.axis("tight")
    plt.xlabel('time', fontsize=18)
    plt.ylabel('utility', fontsize=16)
    plt.show()

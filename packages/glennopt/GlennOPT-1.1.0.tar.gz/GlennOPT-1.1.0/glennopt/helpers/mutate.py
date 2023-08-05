'''
    Defines mutation and crossover 
'''
from dataclasses import dataclass, field
from enum import Enum
import random
import math
import copy
import time
import numpy as np
from typing import List
from ..base import Parameter, Individual
from ..helpers import convert_to_ndarray

class de_mutation_type(Enum):
    """
        differential evolution mutation type. users can select what kind of mutation type to use 
    """
    de_rand_1_bin = 1
    de_best_1_bin = 2
    simple = 3
    de_rand_1_bin_spawn = 4
    de_dmp = 5

@dataclass
class mutation_parameters:
    """
        Data class for storing the mutation parameters used for NSGA and differential evolution problems 

        Properties:
            mutation_type:
            sigma: 
            mu: 
            F:
            C:
    """
    mutation_type: de_mutation_type = field(repr=True,default=de_mutation_type.de_rand_1_bin)
    sigma: float = field(repr=True,default=0.2)
    mu: float = field(repr=True,default=0.02)
    F: float = field(repr=True,default=0.6)
    C: float = field(repr=True,default=0.8)
    nParents:int = field(repr=True,default=16) # this is useful for single objective where you want x parents to spawn all the children
    
def get_eval_param_matrix(individuals:List[Individual]):    
    pop = np.zeros((len(individuals),len(individuals[0].eval_parameters)))
    xmin = individuals[0].eval_parameter_min
    xmax = individuals[0].eval_parameter_max
    for i,ind in enumerate(individuals):
        pop[i,:] = ind.eval_parameters
    return pop,xmin,xmax

def get_objective_matrix(individuals:List[Individual]):
    pop = np.zeros((len(individuals),len(individuals[0].objectives)))
    for i,ind in enumerate(individuals):
        pop[i,:] = ind.objectives
    return pop

def shuffle_population(pop,nIndividuals,nparents):
    index = (1+np.random.permutation(nIndividuals))[0:nparents]     # Pick Random Parents
    rot = convert_to_ndarray([range(0,nIndividuals)])
    a_perm = np.random.permutation(nIndividuals)
    
    a = np.zeros((nIndividuals,len(index)),dtype=int)
    pop_shuffled = list()
    for i in range(len(index)):
        rt = (index[i]+rot) % nIndividuals
        rt = rt.astype(int)
        a[:,i] = a_perm[rt[0]]
        pop_shuffled.append(pop[a[:,i]])                            # List of shuffled population
    return pop_shuffled

def de_best_1_bin(best:Individual,individuals:List[Individual],objectives:List[Parameter],eval_parameters:List[Parameter],performance_parameters:List[Parameter],F:float=0.6, C:float=0.7):
    """
        Applies mutation and crossover using de_1_rand_bin to a list of individuals 
        Inputs:
            individuals - list of individuals. Takes the best individual[0] (sorted lowest to highest)
            objectives - list of objectives List[Parameter]
            performance_parameters - list of parameters List[parameter]
            F - Amplification Factor [0,2]
            C - Crossover factor [0,1]
        Citatons:
            https://gist.github.com/martinus/7434625df79d820cd4d9
            Storn, R., & Price, K. (1997). Differential Evolution -- A Simple and Efficient Heuristic for global Optimization over Continuous Spaces. Journal of Global Optimization, 11(4), 341–359. https://doi.org/10.1023/A:1008202821328 
            Ao, Y., & Chi, H. (2009). Multi-parent Mutation in Differential Evolution for Multi-objective Optimization. 2009 Fifth International Conference on Natural Computation, 4, 618–622. https://doi.org/10.1109/ICNC.2009.149
    """ 
    nIndividuals = len(individuals)
    pop,xmin,xmax = get_eval_param_matrix(individuals)
    
    x1 = best[0].eval_parameters                             # Use the best individual
    #-------------- Mutation --------------
    pop_shuffled = shuffle_population(pop,nIndividuals,2)
    # Generate the new mutated population
    temp = pop*0
    for i in range(0,len(pop_shuffled)-1,2):
        temp += pop_shuffled[i] - pop_shuffled[i+1]
    pop_mutate = x1+F*temp                          
    
    #-------------- Crossover --------------
    cr_part1 = (np.random.rand(nIndividuals,len(x1)) < C)                     # Crossover    
    cr_part2 = np.array([np.random.permutation(pop.shape[1]) for i in range(nIndividuals)]) # cr_part2, randomly selects for each randomly generated individual, which parameter will be automatically true
    cr = np.logical_or(cr_part1,cr_part2==1)

    new_pop = pop*np.logical_not(cr) + pop_mutate*cr
    #------------- Min Max Check -----------
    xmin = xmin.reshape(1,-1)*np.ones((nIndividuals,1))
    xmax = xmax.reshape(1,-1)*np.ones((nIndividuals,1))
    new_pop = np.minimum(new_pop,xmax)
    new_pop = np.maximum(new_pop,xmin)
    #------------- Create The Individuals ------------
    newIndividuals = list()
    for i in range(new_pop.shape[0]): # loop for each individual set (nIndividuals)
        z = new_pop[i,:]
        newIndividuals.append(Individual(eval_parameters=set_eval_parameters(eval_parameters,z),objectives=objectives,performance_parameters=performance_parameters))

    return newIndividuals

def de_dmp_bak(best:Individual,individuals:List[Individual],objectives:List[Parameter],eval_parameters:List[Parameter],performance_parameters:List[Parameter],num_children:int,C:float=0.5):
    '''
    Difference Mean Based Perturbation - less greedy than DE/best/1 = less chance of getting stuck at local minima, prefers exploration. 
    Individuals:
        best - (Single objective) best individual for single objective. (Multi-objective) a random individual from the best front
        individuals - list of individuals 50% best performing. Takes the best individual[0] (sorted lowest to highest)
        objectives - list of objectives List[Parameter]
        eval_parameters - List[glennopt.helpers.Paramameters]
        performance_parameters - List[glennopt.helpers.Paramameters]
        F - Amplification Factor randomly switched from 0.5 to 2 randomly
        C - Crossover factor sampled uniform at random from 0.3 to 1
        b - Crossover blending rate randomly chosen from 0.1, 0.5(median), 0.9

    Citatons:
        Gosh, A., Das, S., Mallipeddi, R., Das, A. K., & Dash, S. S. (2017). A Modified Differential Evolution with Distance-based Selection for Continuous Optimization in Presence of Noise. IEEE Access, 5, 26944–26964. https://doi.org/10.1109/ACCESS.2017.2773825
    '''
    # * Preprocessing Step: Do this first before generating the deisgns 
    Np = len(individuals)   # This is actually Np/2
    pop,xmin,xmax = get_eval_param_matrix(individuals)
    D = pop.shape[1]
    x_best_avg = 2/Np * np.sum(pop,axis=0) # Sum along the rows, each column is an evaluation parameter 
    x_best_avg = np.array([x_best_avg for i in range(Np)])
    x_best,_,_ = get_eval_param_matrix([best])
    newIndividuals = list()

    while len(newIndividuals)<num_children:
        rand_v = np.random.rand(Np,1)           # Generate random vector
        # * Generate all individuals for mutation strategy 1
        #F = np.array([2 if x==0 else 0.5 for x in np.random.randint(2,size=Np)]).reshape(-1,1)
        F = np.random.choice([0.5,2],size=(Np,1))
        pop_shuffled = shuffle_population(pop,Np,3) 
        V1 = pop_shuffled[0] + F*(x_best_avg - pop_shuffled[1])

        # * Generate all individuals for mutation strategy 2
        M = np.random.random(size=pop.shape)
        x_best_dim = 1/D * np.sum(x_best) 
        X_dim = 1/D * np.sum(pop_shuffled[2])
        V2 = (x_best-X_dim)*M
        V2 = np.array([V2[i,:]/np.linalg.norm(M[i,:]) for i in range(V2.shape[0])])
        V2 += pop_shuffled[2]                   

        # * Now we need to select between elements of V1 and V2 using mutation_selection
        V = V1*(rand_v<=0.5) + V2*(rand_v>0.5)                      

        # * Crossover
        Cr = np.random.uniform(low=0.3, high=1, size=pop.shape) <= C                           # sample the value of Cr from interval 0.3 to 1 uniform at random for all individuals
        Cr_j = np.array([np.random.permutation(pop.shape[1]) for i in range(Np)]) == 1  # cr_part2, randomly selects for each randomly generated individual, which parameter will be automatically true        
        Cr = np.logical_or(Cr,Cr_j)
        b = np.random.choice([0.1,0.5,0.9], size=(Np,1), replace=True, p=None)        
            
        u = (b*pop_shuffled[2]+(1-b)*V) * Cr  + pop * np.logical_not(Cr) 

        #------------- Min Max Check -----------
        xmin_reshape = xmin.reshape(1,-1)*np.ones((Np,1))
        xmax_reshape = xmax.reshape(1,-1)*np.ones((Np,1))
        u = np.minimum(u,xmax_reshape)
        u = np.maximum(u,xmin_reshape)

        #------------- Create The Individuals ------------
        for i in range(u.shape[0]): # loop for each individual set (nIndividuals)
            z = u[i,:]
            newIndividuals.append(Individual(eval_parameters=set_eval_parameters(eval_parameters,z),objectives=objectives,performance_parameters=performance_parameters))
        
        
    random.shuffle(newIndividuals)
        
    return newIndividuals[0:num_children]


def de_dmp(individuals:List[Individual],objectives:List[Parameter],eval_parameters:List[Parameter],performance_parameters:List[Parameter]):
    '''
    Difference Mean Based Perturbation - less greedy than DE/best/1 = less chance of getting stuck at local minima, prefers exploration. 
    Individuals:
        individuals - list of all individuals, sorted in terms of best performing
        objectives - list of objectives List[Parameter]
        eval_parameters - List[glennopt.helpers.Paramameters]
        performance_parameters - List[glennopt.helpers.Paramameters]
        F - Amplification Factor randomly switched from 0.5 to 2 randomly
        C - Crossover factor sampled uniform at random from 0.3 to 1
        b - Crossover blending rate randomly chosen from 0.1, 0.5(median), 0.9

    Citatons:
        Gosh, A., Das, S., Mallipeddi, R., Das, A. K., & Dash, S. S. (2017). A Modified Differential Evolution with Distance-based Selection for Continuous Optimization in Presence of Noise. IEEE Access, 5, 26944–26964. https://doi.org/10.1109/ACCESS.2017.2773825
    '''
    # * Preprocessing Step: Do this first before generating the deisgns 
    Np = len(individuals)                       # This is actually Np/2
    pop,xmin,xmax = get_eval_param_matrix(individuals)
    pop_half = pop[:int(Np/2),:]
    D = pop.shape[1]                            # Number of parameters
    x_best_avg = 2/Np * np.sum(pop_half,axis=0) # Sum along the rows, each column is an evaluation parameter         
    x_best_dim = 1/D * np.sum(pop[0,:])
    newIndividuals = list()

    V = pop*0
    U = V
    for i in range(Np):
        if random.random()<=0.5:
            p = get_pairs(pop.shape[0],2,[i])
            xr1 = pop[p[0],:]
            xr2 = pop[p[0],:]
            F = np.random.choice([0.5,2])
            V[i,:] = xr1 + F*(x_best_avg-xr2)
        else:
            xi_dim = 1/D * np.sum(pop[i,:])
            M = np.random.random(size=D)
            V[i,:] = pop[i,:] + (x_best_dim - xi_dim) * M / np.linalg.norm(M)
        Cr = np.random.uniform(0.3,1)
        b = np.random.choice([0.1,0.5,0.9])
        jr = random.randint(0,D-1)
        for j in range(D):
            if (random.random() < Cr or j ==jr):
                U[i,j] = b*pop[i,j]+(1-b)*V[i,j]
            else:
                U[i,j] = pop[i,j]
        
        #------------- Min Max Check -----------
        xmin_reshape = xmin.reshape(1,-1)*np.ones((Np,1))
        xmax_reshape = xmax.reshape(1,-1)*np.ones((Np,1))
        U = np.minimum(U,xmax_reshape)
        U = np.maximum(U,xmin_reshape)

    #------------- Create The Individuals ------------
    for i in range(U.shape[0]): # loop for each individual set (nIndividuals)
        z = U[i,:]
        newIndividuals.append(Individual(eval_parameters=set_eval_parameters(eval_parameters,z),objectives=objectives,performance_parameters=performance_parameters))
        
        
    random.shuffle(newIndividuals)
        
    return newIndividuals


def de_rand_1_bin(individuals:List[Individual],objectives:List[Parameter],eval_parameters:List[Parameter],performance_parameters:List[Parameter],min_parents:int=3,max_parents:int=3,F:float=0.6, C:float=0.7):
    """
        Applies mutation and crossover using de_rand_1_bin to a list of individuals 
        Inputs:
            individuals - list of individuals. Takes the best individual[0] (sorted lowest to highest)
            objectives - list of objectives List[Parameter]
            performance_parameters - list of parameters List[parameter]
            F - Amplification Factor [0,2]
            C - Crossover factor [0,1]
        Citatons:
            https://gist.github.com/martinus/7434625df79d820cd4d9
            Storn, R., & Price, K. (1997). Differential Evolution -- A Simple and Efficient Heuristic for global Optimization over Continuous Spaces. Journal of Global Optimization, 11(4), 341–359. https://doi.org/10.1023/A:1008202821328 
            Ao, Y., & Chi, H. (2009). Multi-parent Mutation in Differential Evolution for Multi-objective Optimization. 2009 Fifth International Conference on Natural Computation, 4, 618–622. https://doi.org/10.1109/ICNC.2009.149
    """ 
    nIndividuals = len(individuals)
    pop,xmin,xmax = get_eval_param_matrix(individuals)
        
    nEvalParams = len(individuals[0].eval_parameters)
    #-------------- Mutation --------------
    pop_shuffled = shuffle_population(pop,nIndividuals,max_parents)
    pop_rand = pop_shuffled.pop()
    # Generate the new mutated population
    temp = pop*0
    for i in range(0,len(pop_shuffled)-1,2):
        temp += pop_shuffled[i] - pop_shuffled[i+1]
    pop_mutate = pop_rand+F*temp                          
    
    #-------------- Crossover --------------
    cr_part1 = (np.random.rand(nIndividuals,nEvalParams) < C)                     # Crossover    
    cr_part2 = np.array([np.random.permutation(nEvalParams) for i in range(nIndividuals)]) # cr_part2, randomly selects for each randomly generated individual, which parameter will be automatically true
    cr = np.logical_or(cr_part1,cr_part2==1)

    new_pop = pop*np.logical_not(cr) + pop_mutate*cr
    #------------- Min Max Check -----------
    xmin = xmin.reshape(1,-1)*np.ones((nIndividuals,1))
    xmax = xmax.reshape(1,-1)*np.ones((nIndividuals,1))
    new_pop = np.minimum(new_pop,xmax)
    new_pop = np.maximum(new_pop,xmin)
    #------------- Create The Individuals ------------
    newIndividuals = list()
    for i in range(new_pop.shape[0]): # loop for each individual set (nIndividuals)
        z = new_pop[i,:]
        newIndividuals.append(Individual(eval_parameters=set_eval_parameters(eval_parameters,z),objectives=objectives,performance_parameters=performance_parameters))

    return newIndividuals


def simple(individuals:List[Individual],nCrossover:int,nMutation:int,objectives:List[Parameter],eval_parameters:List[Parameter],performance_parameters:List[Parameter],mu:float,sigma:float):
    """
        Performs a simple mutation and crossover on the individuals
        Inputs:
            individuals - list of individuals
            objectives - list of objectives List[Parameter]
            eval_parameters
            performance_parameters - list of parameters List[parameter]
            mu - mutation rate 0.2
            sigma - mutation step size 0.1
    """
    nIndividuals = len(individuals)
    # Perform Crossover
    crossover_individuals = []
    for k in range(int(nCrossover/2)):
        rand_indx = np.random.randint(0,nIndividuals-1)
        y1 = individuals[rand_indx].eval_parameters

        rand_indx2 = np.random.randint(0,nIndividuals-1)
        y2 = individuals[rand_indx2].eval_parameters
        [y1_new, y2_new] = crossover(y1, y2)
        
        crossover_individuals.append(Individual(eval_parameters=set_eval_parameters(eval_parameters,y1_new),objectives=objectives,performance_parameters=performance_parameters))        
        crossover_individuals.append(Individual(eval_parameters=set_eval_parameters(eval_parameters,y2_new),objectives=objectives,performance_parameters=performance_parameters))
    
    # Perform Mutation    
    mutation_individuals = list()
    for k in range(nMutation):
        rand_indx = np.random.randint(0,nIndividuals-1)
        y1 = individuals[rand_indx].eval_parameters
        ymin = individuals[rand_indx].eval_parameter_min
        ymax = individuals[rand_indx].eval_parameter_max

        y1_new = mutate(y1,ymin,ymax,mu,sigma)

        mutation_individuals.append(Individual(eval_parameters=set_eval_parameters(eval_parameters,y1_new),objectives=objectives,performance_parameters=performance_parameters))
    crossover_individuals.extend(mutation_individuals)

    return crossover_individuals

# Core functions 
def mutate(x1:np.ndarray,xmin:np.ndarray,xmax:np.ndarray,mu:float=0.02,sigma:float=0.2):
    '''
        Mutate the evaluation parameters
        Simple mutate
        Inputs:
            x1 - array of evaluation parameters
            mu - percentage of population to mutate
            sigma - mutation scale 
    
    '''
    nMu = math.ceil(mu*len(x1))
    j = np.random.randint(0,len(x1)-1,size=nMu)
    y = x1 
    for k in range(len(j)):
        indx = j[k]
        if (indx>0):
            y[indx] = x1[indx]+sigma*np.random.randn(1)

            if (xmin is not None) and (y[indx]<xmin[indx]):
                y[indx]=xmin[indx]
            if (xmax is not None) and (y[indx]>xmax[indx]):
                y[indx]=xmax[indx]
    return y

def crossover(x1:np.ndarray,x2:np.ndarray):
    '''
        Simple crossover
        Inputs:
            x1 - array of evaluation parameters
            x2 - array of evaluation parameters
    '''
    alpha = np.random.rand(len(x1))
    y1=alpha*x1+(1.0-alpha)*x2
    y2=alpha*x2+(1.0-alpha)*x1
    return y1,y2

# Helper functions
def get_pairs(nIndividuals:int,nParents:int,parent_indx_seed=[]):
    """
        Get a list of all the pairing partners for a particular individual
        Inputs:
            nIndividuals - number of individuals
            nParents - number of parents 
            parent_indx_seed - pre-populate the parent index array
    """    
    parent_indicies = list()
    for i in range(nParents):
        rand_indx = random.randint(0,nIndividuals-1)
        while(rand_indx in parent_indx_seed):
            rand_indx = random.randint(0,nIndividuals-1)
        parent_indicies.append(rand_indx)
    return parent_indicies

def set_eval_parameters(eval_parameters:List[Parameter], x:np.ndarray):
    """
        Set the evaluation parameters 
        Inputs:
            eval_parameters - list of parameters as a class. x is mapped to eval_parameter.value
            x - represents an the mutated value/array to be evaluated 
    """
    parameters = copy.deepcopy(eval_parameters)
    for indx in range(len(parameters)):
        parameters[indx].value = x[indx]
    return parameters

def de_rand_1_bin_spawn(individuals:List[Individual],objectives:List[Parameter],eval_parameters:List[Parameter],performance_parameters:List[Parameter],num_children:int,F:float=0.6, C:float=0.7):
    """
        Applies mutation and crossover using de_rand_1_bin to a list of individuals to spawn even more individual combinations
        Inputs:
            individuals - list of individuals. Takes the best individual[0] (sorted lowest to highest)
            objectives - list of objectives List[Parameter]
            performance_parameters - list of parameters List[parameter]
            F - Amplification Factor [0,2]
            C - Crossover factor [0,1]
        Citatons:
           
    """ 
    nIndividuals = len(individuals)
    pop,xmin,xmax = get_eval_param_matrix(individuals)
    nEvalParams = len(individuals[0].eval_parameters)
    newIndividuals = list()

    while (len(newIndividuals)<num_children):
        #-------------- Mutation --------------
        pop_shuffled = shuffle_population(pop,nIndividuals,3)
        pop_rand = pop_shuffled.pop()
        # Generate the new mutated population
        temp = pop*0
        for i in range(0,len(pop_shuffled)-1,2):
            temp += pop_shuffled[i] - pop_shuffled[i+1]
        pop_mutate = pop_rand+F*temp                          
        
        #-------------- Crossover --------------
        cr_part1 = (np.random.rand(nIndividuals,nEvalParams) < C)                     # Crossover    
        cr_part2 = np.array([np.random.permutation(nEvalParams) for i in range(nIndividuals)]) # cr_part2, randomly selects for each randomly generated individual, which parameter will be automatically true
        cr = np.logical_or(cr_part1,cr_part2==1)

        new_pop = pop*np.logical_not(cr) + pop_mutate*cr
        #------------- Min Max Check -----------
        xmin_reshape = xmin.reshape(1,-1)*np.ones((nIndividuals,1))
        xmax_reshape = xmax.reshape(1,-1)*np.ones((nIndividuals,1))
        new_pop = np.minimum(new_pop,xmax_reshape)
        new_pop = np.maximum(new_pop,xmin_reshape)
        #------------- Create The Individuals ------------    
        for i in range(new_pop.shape[0]): # loop for each individual set (nIndividuals)
            z = new_pop[i,:]
            newIndividuals.append(Individual(eval_parameters=set_eval_parameters(eval_parameters,z),objectives=objectives,performance_parameters=performance_parameters))
        
    random.shuffle(newIndividuals)

    return newIndividuals[0:num_children]
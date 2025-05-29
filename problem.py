from individual import Individual
import random
import numpy as np
import pandas as pd
import time


def matrix_and(a, b):
    n = a.shape[0]
    c = np.zeros((n, n), dtype=int)
    for i in range(n):
        c[i] = a[i] & b[i]
    return c


class Problem:

    def __init__(self, objectives, node_num, coverage, coverage_constrain, station_upbound=100):
        self.num_of_objective=len(objectives)
        self.objectives=objectives
        self.node_num=node_num
        self.demand_num= sum(coverage['Demand_sum'])
        self.station_upbound=station_upbound
        # 限制station个数的上界
        self.coverage=coverage
        self.coverage_constrain=coverage_constrain
   




    # @profile
    def generate_individual(self):
        individual=Individual(self.node_num)
        positive_num=random.randint(1,self.station_upbound)
        positive_nodes=random.sample(list(range(self.node_num)),positive_num)
        individual.positive_nodes=positive_nodes

        for i in positive_nodes:
            individual.chromosome[i]=1
        return individual

    def generate_individual_with(self,individual1):
        '''
        create a copy of an Individual

        Parameters
        ----------
        individual1 : TYPE Individual
            DESCRIPTION. An individual to create a copy of.

        Returns
        -------
        individual : TYPE Individual
            DESCRIPTION. An independent copy of individual1

        '''
        individual=Individual(self.node_num)
        individual.chromosome=individual1.chromosome.copy()
        individual.positive_nodes=individual1.positive_nodes.copy()
        return individual


    def generate_individual_with_positive_nodes(self, positive_nodes):
        individual = Individual(self.node_num)
        individual.positive_nodes = positive_nodes
        for i in positive_nodes:
            individual.chromosome[i] = 1
        self.calculate_objectives(individual)

        return individual

    # @profile
    def calculate_objectives(self, individual):
        individual.positive_nodes = np.array(np.where(individual.chromosome == 1))[0].tolist()
        individual.capacity=self.coverage['Station_capacity'].iloc[individual.positive_nodes].tolist()
        individual.coverage_ID=self.coverage['Demand_ID'].iloc[individual.positive_nodes].tolist()
        individual.coverage_distance=self.coverage['Distance'].iloc[individual.positive_nodes].tolist()
        individual.coverage_demandcount=self.coverage['Demand_count'].iloc[individual.positive_nodes].tolist()
        individual.coverage_total_distance=self.coverage['Total_Distance'].iloc[individual.positive_nodes].tolist()
        individual.coverage_demand_sum=self.coverage['Demand_sum'].iloc[individual.positive_nodes].tolist()

        individual.objectives=[self.objectives[0](individual),self.objectives[1](individual)]
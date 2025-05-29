import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import pickle
import argparse
import os
import time

from evolution import Evolution
from problem import Problem
import objective


'''
Params
--mp mutation parameter
--cp crossover parameter
--iter interation number of NSGA-II
--upbound maximum station number
--cc minimum coverage constraint, default 0
--netdir input data directory
--outdir output directory
'''


def pre_read(parent_dir="D:/study/Master y2s1/URBP6865/localdata/output_pkl/"):

    with open(parent_dir+"land_high_50m_cover.pkl","rb") as tf:
        coverage= pickle.load(tf)
        node_num=len(coverage)
    tf.close()



    return coverage, node_num


def run_case(mp=0.1, cp=0.9, gen_num=100, station_upbound=150,
             coverage_constrain=0.2,
             network_dir="D:/study/Master y2s1/URBP6865/localdata/output_pkl/", 
             output_dir="D:/study/Master y2s1/URBP6865/localdata/output_nsga/land_high_50m_cover/"): 

    # get data
    coverage, node_num=pre_read(parent_dir=network_dir)
    
    problem = Problem(objectives=[objective.neg_max_coverage, objective.min_cost],
                      node_num=node_num, coverage=coverage,
                      station_upbound=station_upbound,
                      coverage_constrain=coverage_constrain)

    fig_path = os.path.join(output_dir, 'gen_' + str(gen_num) + '_mp' + '{:.2f}'.format(mp) + '_cp' + '{:.2f}'.format(cp) + '_up' + str(node_num) + '_cc' + str(coverage_constrain) + '/')

    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    cnt = len(os.listdir(fig_path))
    fig_path = os.path.join(fig_path, str(cnt))

    evo = Evolution(problem, node_num=node_num, num_of_generations=gen_num, num_of_individuals=200, num_of_tour_particips=2,
                    tournament_prob=0.8,
                    crossover_param=cp, mutation_param=mp, 
                    #input_fn=r'../../DATA/best_initialized_popu.pkl', # can specify filename to load existing initial population
                    fig_path=fig_path
                    )

    solution = evo.evolve()


if __name__=='__main__': 

    start=time.time()
    run_case()
    end=time.time()
    cost_time=end-start
    
   # dir_path = os.path.join(output_dir, f'gen_{gen_num}_mp{mp:.2f}_cp{cp:.2f}_up{station_upbound}_cc{coverage_constrain}')
   # os.makedirs(dir_path, exist_ok=True)
   # file_path = os.path.join(dir_path, "cost_time.txt")
   # with open(file_path, "a") as tf:
       # tf.write(f"mp:{mp} cp:{cp} iter:{gen_num} cc:{coverage_constrain} upbound:{station_upbound} cost_time:{cost_time}\n")
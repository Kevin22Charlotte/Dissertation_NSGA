import math
import numpy as np


def subtract_common(pre, temp):
    return pre-temp


def neg_max_coverage(individual):
    
    required_demand = individual.coverage_demand_sum
    real_cover = [min(i, j) for i, j in zip(individual.capacity, required_demand)]
    average_cover= sum(real_cover)

    return -average_cover

def min_cost(individual):
    one_supply_station_cost=1157.49
    station_cost= sum([one_supply_station_cost*len(individual.positive_nodes)])

    operation_cost_per_meter=0.011
    trips_per_day=6
    operation_cost=sum([operation_cost_per_meter*dis*trips_per_day for dis in individual.coverage_total_distance])

    cost=station_cost+operation_cost

    return cost



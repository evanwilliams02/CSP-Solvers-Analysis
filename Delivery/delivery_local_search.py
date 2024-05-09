import random, time, sys

def fill_random_variables(graph, packages):

    # Fills the distance between locations
    for i in graph:
        for j in graph[i]:
            if graph[i][j] == 1:
                graph[i][j] = random.randint(7, 50)
            
        
    # Fills the delivery times of packages
    for d in packages:
        if packages[d]['delivery_time'] == 1:
            packages[d]['delivery_time'] = random.randint(25, 90)

def generate_neighbors(current_solution):
    global generator_num

    neighbors = []
    
    copy_of = current_solution.copy()

    solution = copy_of[1:]

    generator_num = 2000
    

    for i in range(generator_num):
        random.shuffle(solution)

        
        neighbors.append(['start'] + solution)

    return neighbors

def stopping_condition(iterations, max_iterations):
    # Define the stopping condition based on the number of iterations
    if iterations >= max_iterations:
        print()
        print()
        print('Achieved Iterations:      ', max_iterations)
        print('Neighbors Per Iteration:  ', generator_num)
        print()
        print()
        return True
    else:
        return False
    
def validate_neighbors(graph, solution, total_distance, current_time, delivery_distance, packages_list):


    if not solution and not packages_list:
        return total_distance, delivery_distance


    curr_loc = solution[0]

    if len(solution) >= 2:
        next_loc = solution[1]
    else:
        next_loc = None

    if next_loc is None:
        time_to_go = 0
    else:
        time_to_go = graph[curr_loc][next_loc]
        delivery_time = packages[next_loc]['delivery_time']

        total_distance  +=  current_time + time_to_go
        delivery_distance   +=  current_time + delivery_time
        

    copy_solution = solution.copy()
    copy_solution.remove(curr_loc)

    copy_packages = packages_list.copy()
    
    copy_packages.remove(curr_loc)
    

    return validate_neighbors(graph, copy_solution, total_distance, total_distance, delivery_distance, copy_packages)

def calculate_total_distance(graph, solution, total_distance):

    
    if not solution:
        return total_distance


    curr_loc = solution[0]

    if len(solution) >= 2:
        next_loc = solution[1]
    else:
        next_loc = None

    if next_loc is None:
        distance = 0
    else:
        
        distance = graph[curr_loc][next_loc]

    copy_solution = solution.copy()
    copy_solution.remove(curr_loc)

    return calculate_total_distance(graph, copy_solution, total_distance + distance)

def generate_initial_solution():

    graph = {
        'start':   {'david':1,'frank':1,'charlie':1,'bob':26,'issac': 1},
        'eve':     {'start': 1,'charlie':24,'bob':1},
        'david':   {'start': 1,'issac': 1,'bob':1},
        'issac':   {'start': 1,'eve': 33,'grace':1,'charlie':1,'david':1},
        'alice':   {'frank':1,'charlie':1,'grace':1},
        'frank':   {'start': 1,'eve': 1,'alice':1},
        'charlie': {'start': 1,'issac': 31,'alice':1,'frank':1,'grace':1},
        'grace':   {'issac': 1,'alice':1,'charlie':1, 'david':1},
        'bob':     {'david':1,'alice':50,'eve': 1}
    } 

    packages = {
            'start': {'delivery_time': 0},
            'alice': {'delivery_time': 210},
            'bob': {'delivery_time': 70},
            'david': {'delivery_time':1},
            'grace': {'delivery_time': 120},
            'frank': {'delivery_time': 1},
            'eve': {'delivery_time': 1},
            'issac': {'delivery_time': 1},
            'charlie': {'delivery_time': 1}
        }

    solution = ['start', 'bob', 'david', 'issac', 'grace', 'alice', 'frank', 'eve', 'charlie']

    fill_random_variables(graph, packages)
        
    return graph, packages, solution

def local_search(graph, current_solution, neighbors):

    iterations = 0

    fitni = {}
    orig_time = 0

    # Hill Climbing Algorithm
    while not stopping_condition(iterations, max_iterations):
        # Evaluate current solution 
        current_fitness = calculate_total_distance(graph, current_solution, 0)
        if iterations == 0:
            orig_time = current_fitness
            print()
            print('Original Time:  ', round(int(current_fitness) / 60, 2), 'hour(s)')
            print('Original Route: ', current_solution)
        
        

        for i in range(len(neighbors)):
            neighbor_fitness = calculate_total_distance(graph, neighbors[i], 0)
            
            fitni[neighbor_fitness] = neighbors[i]

        
        iterations += 1

    try:
        mini = min(fitni.keys())
    except ValueError:
        print('FOUND VALID NEIGHBORS')
        print('RUN PROGRAM AGAIN')
        sys.exit()

    best_neighbor = fitni[mini]
    best_fitness = mini

    
    return best_neighbor, best_fitness, orig_time

start_time = time.time()

max_iterations = 100

graph, packages, solution = generate_initial_solution()

temp = generate_neighbors(solution)

neighbors = []


for n in temp:
    
    
    try:
        total_distance, delivery_distance = validate_neighbors(graph, n, 0, 0, 0, list(packages.keys()))
    except KeyError:
        continue
    
    if total_distance <= delivery_distance:
        neighbors.append(n)


final_solution, best_fitness, orig_time = local_search(graph, solution, neighbors)
end_time = time.time()

print('Shortest Solution:')
print()
print('Route:', final_solution)
print('Total Delivery Time:', round(int(best_fitness) / 60, 2), 'hour(s)')

if orig_time > best_fitness:
    print()
    print('Solution Imporved !')
    print()
else:
    print()
    print('Solution did not improve :(, try increasing search size variables (max_iterations or generator_num)')
    print()

elapsed_time = end_time - start_time

print("Elapsed time: {:.2f} seconds".format(elapsed_time))
print()
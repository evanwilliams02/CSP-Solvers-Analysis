import random
random.seed(10)

# Don't mind the 1s here, they are later replaced with random numbers
graph = {
    'start': {'david': 1, 'eve': 1, 'bob':1, 'alice': 1,'issac': 1},
    'eve': {'start': 1, 'alice':1, 'david':1},
    'david': {'start': 1, 'issac': 1, 'bob':1,'alice': 1,'eve': 1,},
    'issac': {'alice': 1, 'charlie':1, 'bob':1},
    'alice': {'issac':1, 'frank':1, 'eve':1},
    'frank': {'alice':1, 'eve':1, 'grace':1, 'charlie':1},
    'charlie': {'frank':1, 'grace':1, 'alice':1},
    'grace': {'charlie':1, 'bob':1, 'issac':1},
    'bob': {'grace':1, 'david':1, 'start': 1,}
}
packages = {
    'P4': {'location': 'alice', 'delivery_time': 1},
    'P8': {'location': 'bob', 'delivery_time': 1},
    'P2': {'location': 'david', 'delivery_time':1},
    'P7': {'location': 'grace', 'delivery_time': 1},
    'P5': {'location': 'frank', 'delivery_time': 1},
    'P1': {'location': 'eve', 'delivery_time': 1},
    'P3': {'location': 'issac', 'delivery_time': 1},
    'P6': {'location': 'charlie', 'delivery_time': 1}
}

# Initialize variables
shortest_route = []
shortest_time = float('inf')
frontier = ['start']

def backtrack(current_location, remaining_packages, current_route, current_time, frontier):
    global shortest_time, shortest_route
    
    # Base case: all packages delivered
    if not remaining_packages:
        if current_time < shortest_time:
            shortest_time = current_time
            shortest_route = current_route
        return
    

    for next_location in graph[current_location]:
        distance = graph[current_location][next_location]
        new_time = current_time + distance
        # print('next location:  ',next_location)
        # print('remaining_packages:  ',remaining_packages)
        # print('current_location:  ',current_location)
        # print('current_time:  ',current_time)
        # print('distance:  ',distance)
        # print('current_route:  ',current_route)
        # print('AHHHHHHHHHHHHH:  ', frontier)
        
        
        # Check if delivery time for next package can be met
        for next_package in remaining_packages:
            
            # print('next_package:  ',next_package)
            # print('new_time:  ',new_time)
            # print('next_package delivery time:  ',packages[next_package]['delivery_time'])
            # print()
            # print()
            # print()
            # print()
            # # print('boolean check to see if the time it would take to get to next')
            # # print('package is shorter than the time i have to delivery the next package:  ')
            # # print(new_time <= packages[next_package]['delivery_time'])
            # print()
            # print()

            #  and packages[next_package]['location'] == current_location
        
            if new_time <= packages[next_package]['delivery_time'] and next_location not in frontier and packages[next_package]['location'] == next_location:
                
                remaining = remaining_packages.copy()
                remaining.remove(next_package)
                backtrack(next_location, remaining, current_route + [next_location], new_time, frontier + [next_location])

def fill_random_variables(graph, packages):

    # Fills the distance between locations
    for i in graph:
        for j in graph[i]:
            graph[i][j] = random.randint(3, 25)
            
        
    # Fills the delivery times of packages
    for d in packages:
        packages[d]['delivery_time'] = random.randint(80, 720)

fill_random_variables(graph, packages)

while not shortest_route:

    # Start backtracking from the starting location
    backtrack('start', list(packages.keys()), ['start'], 0, frontier)
    print('still searching..')

# Output the shortest route and delivery time
print()
print('Found Solution !')
print('Shortest Route:', shortest_route)
print('Total Delivery Time:', shortest_time)
import random, time

# Initialize variables
shortest_route = []
shortest_time = 0
frontier = ['start']

# Don't mind the 1s here, they are later replaced with random numbers
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
# An alternate version of graph, works, but less effecient 
# in finding a solution
# graph = {
#     'start':   {'david':1,'frank':1,'charlie':1,'bob':26,'issac': 1},
#     'eve':     {'start': 1,'charlie':24,'bob':1},
#     'david':   {'start': 1,'issac': 1,'bob':1},
#     'issac':   {'start': 1,'eve': 33,'grace':1,'charlie':1,'david':1},
#     'alice':   {'frank':1,'charlie':1,'grace':1},
#     'frank':   {'start': 1,'eve': 1,'alice':1},
#     'charlie': {'start': 1,'issac': 1,'alice':1,'frank':1,'grace':1},
#     'grace':   {'issac': 1,'alice':1,'charlie':1, 'david':25},
#     'bob':     {'david':1,'alice':50,'eve': 1}
# } 
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

def backtrack(current_location, remaining_packages, current_route, frontier):
    global shortest_time, shortest_route
    
    current_time = 1
    count = 0
    

    
    while remaining_packages and current_time > shortest_time:
        
        print(' **** New while loop iteration **** ')

        neighbors_copy = graph[current_location].copy()

        for next_location in neighbors_copy:

            try:
                distance = neighbors_copy[next_location]
            except KeyError:
                continue
            
            time_so_far = current_time + distance
            

            temp = []
            for i in remaining_packages:
                temp.append(packages[i]['location'])

            
            print()
            print('time_so_far:        ',time_so_far)
            print('current_location:   ',current_location)
            print('next location:      ',next_location)
            print('remaining_packages: ',temp)
            print('current_time:       ',current_time)
            print('distance:           ',distance)
            print('current_route:      ',current_route)
            print('frontier:           ', frontier)
            
            
            # Check if delivery time for next package can be met
            for package_to_deliver in range(0, len(remaining_packages)):
                print()
                print('    next_package:                 ',remaining_packages[package_to_deliver])
                print('    next_package location:        ',packages[remaining_packages[package_to_deliver]]['location'])
                print('    next_package delivery time:   ',packages[remaining_packages[package_to_deliver]]['delivery_time'])
                print('    driver can meet:              ', next_location, time_so_far <= packages[remaining_packages[package_to_deliver]]['delivery_time']+ current_time)
                print('    customer not in frontier      ',next_location not in frontier)
                print('    on customer:                  ', next_location, packages[remaining_packages[package_to_deliver]]['location'] == next_location)

                package_belongs = False

                if time_so_far <= packages[remaining_packages[package_to_deliver]]['delivery_time'] + current_time and next_location not in frontier and packages[remaining_packages[package_to_deliver]]['location'] == next_location:
                    
                    package_belongs = True
                    current_location = packages[remaining_packages[package_to_deliver]]['location']
                    current_route.append(next_location)
                    frontier.append(next_location)
                    current_time += distance
                    remaining_packages.remove(remaining_packages[package_to_deliver])
                    print()
                    print('        Things after Inserted into route:')
                    print('            current_location: ',current_location)
                    print('            current_route:    ',current_route)
                    print('            frontier:         ',frontier)
                    print('            current_time:     ',current_time)
                    break
            print()
            print('        package_to_deliver + 1   ', package_to_deliver+1)
            print('        package_belongs          ', package_belongs)
            print('        len(remaining_packages)  ', len(remaining_packages))
            print('        full statement bool      ', not package_belongs and (package_to_deliver+1) == len(remaining_packages))
            print()

            if not package_belongs and (package_to_deliver + 1) == len(remaining_packages):
                count += 1
                
                if count == len(neighbors_copy):
                    print(" ### Couldn't get to", packages[remaining_packages[package_to_deliver]]['location'], 'from', current_location, '### ')
                    current_location = next_location
                    current_route.append(next_location + '*')
                    current_time += distance
                    
                    print()
                    print('Now going to next customer, but not deliverying... ')
                    print('Destination: ', next_location)
                
                continue
            else:
                break
        
        count = 0

        broken = False
        if len(current_route) == 30:
            print()
            broken = True
            print('**** SEARCHED FAILED ****')
            break
   
        
        
           
    shortest_time = current_time - 1
    shortest_route = current_route

    if broken:
        return False
    
    return True

def fill_random_variables(graph, packages):

    # Fills the distance between locations
    for i in graph:
        for j in graph[i]:
            if graph[i][j] == 1:
                graph[i][j] = random.randint(5, 50)
            
        
    # Fills the delivery times of packages
    for d in packages:
        if packages[d]['delivery_time'] == 1:
            packages[d]['delivery_time'] = random.randint(25,90)


# Takes graph and packages and fills them with randomvariables
# Some values are preset to facilitate shortcuts that will take
# a longe time to go from one end of map to the other
fill_random_variables(graph, packages)

start_time = time.time()

if backtrack('start', list(packages.keys()), ['start'], frontier):
    print()
    print()
    print('Found Solution !')
    print()
    print('Shortest Route:', shortest_route)
    print('Total Delivery Time:', round(int(shortest_time) / 60, 2), 'hour(s)')
    print()
else:
    print('END')
    print()

end_time = time.time()

elapsed_time = end_time - start_time

print("Elapsed time: {:.2f} seconds".format(elapsed_time))
print()
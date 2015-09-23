import fileinput as fi
import random as rand
from operator import itemgetter
import math
import sys
import time 

# ======== Functions ========

# ==== Initialization ====

# Genererate initial population
def gen_init_pop(puzzle, fd, pop_size):
    # Gene pool
    GP = []
    for i in fd:
        GP.append(i)

    # Population of strings
    population = []
    # Generate random strings
    for i in range(0, pop_size):
        string = rand_string(puzzle, GP)
        population.append(string)

    return population

# Generate random string
def rand_string(puzzle, GP):
    chars = [e for e in GP]
    string = []
    string_len = -1
    
    # Puzzle 1
    if puzzle == 1:
        string_len = rand.randint(1, len(chars))
        for i in range(0, string_len):
            c = rand.choice(chars)
            string.append(c)
            chars.remove(c)
    # Puzzle 2
    elif puzzle == 2:
        string_len = 30
        for i in range(0, string_len):
            c = rand.choice(chars)
            string.append(c)
            chars.remove(c)
    # Puzzle 3
    elif puzzle == 3:
        doors = []
        lookouts = []
        for i in chars:
            if i[0] == "Door":
                doors.append(i)
                chars.remove(i)
            elif i[0] == "Lookout":
                lookouts.append(i)
                chars.remove(i)

        # First layer is a door
        door = rand.choice(doors)
        string.append(door)

        string_len = rand.randint(0, len(chars))
        for i in range(0, string_len):
            c = rand.choice(chars)
            string.append(c)
            chars.remove(c)

        # Last layer is a lookout
        lookout = rand.choice(lookouts)
        string.append(lookout)
    # Invalid puzzle
    else:
        print "Error: In rand_string() - Invalid Puzzle Number"
    
    return string

# ==== Genetic Algorithm ====

# Fitness functions
def fitness_function(puzzle, target, population):
    raw_pop = []
    total_value = 0.0

    # Puzzle 1
    if puzzle == 1:
        for element in population:
        # Calculate fitness value of element
            fitness_val = 0
            diff = target - float(sum(element))
            if diff <= 0:
                fitness_val = 0
            else:
                fitness_val = -1.0*((diff/target)**2)*100.0 + 100.0
            
            total_value += fitness_val
            element_tup = [fitness_val, element]

            # Add tuple (e, value) to ordered_pop
            raw_pop.append(element_tup)
    # Puzzle 2
    elif puzzle == 2:
        print '2'
    # Puzzle 3
    elif puzzle == 3:
        print '3'
    else: 
        print "Error: In fitness_function() - Invalid Puzzle Number"

    # Normalize element fitness values
    for i in range(0, len(raw_pop)):
        raw_pop[i][0] /= total_value
    # Organize elements by fitness values
    raw_pop.sort(key = lambda x: x[0])
    print "Before Accum: " + str(raw_pop)
    print ""
    # Accumulate element fitness values
    for i in range(1, len(raw_pop)):
        raw_pop[i][0] += raw_pop[i - 1][0]
    print "After Accum: " + str(raw_pop)
    print ""
    return raw_pop

# Evaluate fitness of strings
def evaluate(puzzle, target, population):
    ordered_list = fitness_function(puzzle, target, population)
    
    return ordered_list

# Select strings from old population to create new population

# Crossover between strings in population

# Mutate strings in population


# ======== Format Input ========

puzzle_num = int(sys.argv[1])
fd = [line for line in fi.input(sys.argv[2])]
fi.close()
# Runtime in seconds
run_time = int(sys.argv[3])
rand.seed(5)

# Set target value
T = 0
if puzzle_num == 1:
    T = float(fd[0])
    del fd[0]
elif puzzle_num == 2:
    print '2' 
elif puzzle_num == 3:
    print '3'
else:
    print 'else'

# Format fd
if puzzle_num == 1:
    # Format layers
    for i in range(0, len(fd)):
        fd[i] = int(fd[i])

# ======== Run Genetic Algorithm ========
cur_time = 0
start_time = time.time()
a_list = []
population = gen_init_pop(puzzle_num, fd, 50)

while cur_time <= run_time:
    # Time in seconds
    cur_time = time.time() - start_time
    a_list = evaluate(puzzle_num, T, population)
    # run code

print a_list

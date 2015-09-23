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

# Puzzle 1 rules
def no_repeats(element, genes):
    string = [e for e in element]
    chars = [g for g in genes]
    for i in string:
        try:
            chars.remove(i)
        except ValueError:
            return False
    return True

# Evaluate fitness of strings
def evaluate(puzzle, target, population, genes):
    raw_pop = []
    total_value = 0.0

    # Puzzle 1
    if puzzle == 1:
        for element in population:
        # Calculate fitness value of element
            fitness_val = 0.0
            diff = target - float(sum(element))
            if diff < 0:
                fitness_val = 0.0
            else:
                if no_repeats(element, genes):
                    fitness_val = (target**2) - (diff**2)
                else:
                    fitness_val = 0.0
            
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

    # print raw_pop
    # Organize elements by fitness values
    raw_pop.sort(key = lambda x: x[0])
    # Accumulate element fitness values
    for i in range(1, len(raw_pop)):
        raw_pop[i][0] += raw_pop[i - 1][0]
    # Normalize element fitness values
    for i in range(0, len(raw_pop)):
        try:
            raw_pop[i][0] /= total_value
        except ZeroDivisionError:
            print "Error: In fitness_function() - Divide by Zero"
            print "Exit Population:"
            print population
            sys.exit()

    return raw_pop

# Select strings from old population to create new population
# Roulette selection
def select(ordered_pop):
    selected_pop = []
    cutoff = rand.random()
    for x in range(0, 10):
        selected_pop.append(ordered_pop[-1][1])
    for x in range(10, len(ordered_pop)):
        for i in ordered_pop:
            if i[0] > cutoff:
                selected_pop.append(i[1])
                cutoff = rand.random()
                break
    # print selected_pop
    # print ""
    return selected_pop

# Crossover between strings in population
def crossover(parent_pop, temperature):
    children_pop = []
    string_buf = []
    flag = 0
    for i in range(0, 2):
        children_pop.append(parent_pop[0])
    rand.shuffle(parent_pop)
    for string in parent_pop:
        if flag < 2:
            flag += 1
            continue
        co_chance = rand.random()
        if co_chance > 1 - temperature:
            if not string_buf:
                string_buf = string
            else:
                a_string = string_buf
                b_string = string
                
                a_index = rand.randint(0, len(a_string))
                b_index = rand.randint(0, len(b_string))

                c_string = a_string[:a_index] + b_string[b_index:]
                d_string = a_string[a_index:] + b_string[:b_index]

                children_pop.append(c_string)
                children_pop.append(d_string)
                
                string_buf = []
        else:
            children_pop.append(string)

    if string_buf:
        children_pop.append(string_buf)

    return children_pop

# Mutate strings in population
def mutate(children_pop, genes, temperature):
    print "Before: " + str(len(children_pop))
    print children_pop
    mutated_pop = []
    flag = 0
    for string in children_pop:
        if flag < 2:
            flag += 1
            mutated_pop.append(children_pop[0])
            continue
        m_index = 0
        if string:
            m_index = rand.randint(0, len(string) - 1)
        m_chance = rand.random()
        string_buf = []
        if m_chance > 1 - temperature:
            new_gene = rand.choice(genes)
            string_buf += string[:m_index]
            string_buf.append(new_gene)
            string_buf += string[m_index + 1:]
            mutated_pop.append(string_buf)
        else:
            mutated_pop.append(string)
    print "After: " + str(len(mutated_pop))
    print mutated_pop
    return mutated_pop

# ==== Print Stats ====
def print_stats(top_score, ts_gen, total_gen):
    # best score
    print "Top Score: " + str(top_score)
    # best score gen
    print "Top Score Generation: " + str(ts_gen)
    # total gen
    print "Total Generations: " + str(total_gen)

# ======== Format Input ========

puzzle_num = int(sys.argv[1])
fd = [line for line in fi.input(sys.argv[2])]
fi.close()
# Runtime in seconds
run_time = int(sys.argv[3])

# Set target value
target = 0
if puzzle_num == 1:
    target = float(fd[0])
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
        fd[i] = float(fd[i])

# ======== Run Genetic Algorithm ========
time_elapsed = 0
temperature = 0
record = -1
record_gen = 0
total_gen = 0
start_time = time.time()
a_list = []
b_list = []
c_list = []
d_list = []
population = gen_init_pop(puzzle_num, fd, 100)

while time_elapsed <= run_time:
    # Time in seconds
    time_elapsed = time.time() - start_time
    temperature = math.exp(-0.4*time_elapsed - 0.3)
    a_list = evaluate(puzzle_num, target, population, fd)

    if sum(a_list[-1][1]) > record:
        record = sum(a_list[-1][1])
        record_gen = total_gen
    b_list = select(a_list)
    c_list = crossover(b_list, temperature)
    # print c_list
    # print ""
    d_list = mutate(c_list, fd, temperature)
    population = d_list
    # print temperature
    total_gen += 1
    # run code

print_stats(record, record_gen, total_gen)

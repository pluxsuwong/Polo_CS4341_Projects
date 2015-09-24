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

# Check if genes are repeated in string
def no_repeats(element, genes):
    string = [e for e in element]
    chars = [g for g in genes]
    for i in string:
        try:
            chars.remove(i)
        except ValueError:
            return False
    return True

# Calculate score for puzzle 2
def puzzle_2_score_calc(string):
    score = 0.0
    bin1 = string[:10]
    bin2 = string[10:20]
    m_buf = 1.0
    s_buf = 0.0
    for e in bin1:
        m_buf *= e
    for e in bin2:
        s_buf += e

    score = (m_buf + s_buf) / 2.0
    return score

# Calculate score for puzzle 3
def puzzle_3_score_calc(tower):
    score = 0.0
    w_limit = 999999
    s_limit = 999999
    total_cost = 0.0
    total_height = len(tower)

    if total_height >= 2:
        for i in range(0, total_height):
            floor_type = tower[i][0]
            floor_width = tower[i][1]
            floor_strength = tower[i][2]
            # Check rules 1 - 3
            if i == 0:
                if floor_type != "Door":
                    return 0.0
            elif i == total_height - 1:
                if floor_type != "Lookout":
                    return 0.0
            else:
                if floor_type != "Wall":
                    return 0.0
            
            # Check rule 4
            if floor_width > w_limit:
                return 0.0

            # Check rule 5
            if floor_strength < len(tower[i + 1:]):
                return 0.0

            # Update limit values and total cost
            w_limit = floor_width
            s_limit = floor_strength
            total_cost += floor[3]

    score = 10 + total_height**2 - total_cost
    return score

# Evaluate fitness of strings
def evaluate(puzzle, target, population, genes):
    raw_pop = []
    total_value = 0.0

    for element in population:
        fitness_val = 0.0
        score = 0.0
        
        if puzzle == 1:
            score = target - float(sum(element))
        elif puzzle == 2:
            score = puzzle_2_score_calc(element)
        elif puzzle == 3:
            score = puzzle_3_score_calc(element)
        else:
            print "Error: In fitness_function() - Invalid Puzzle Number"
            sys.exit()
        
        if score >= 0:
            if no_repeats(element, genes):
                if puzzle == 1:
                    fitness_val = (target**2) - (score**2)
                else:
                    fitness_val = score**2
        total_value += fitness_val

        element_tup = [fitness_val, element]
        raw_pop.append(element_tup)

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
def select(ordered_pop, puzzle):
    if puzzle == 1:
    selected_pop = []
    cutoff = rand.random()
    for x in range(0, 5):
        selected_pop.append(ordered_pop[-1][1])
    for x in range(5, len(ordered_pop)):
        for i in ordered_pop:
            if i[0] > cutoff:
                selected_pop.append(i[1])
                cutoff = rand.random()
                break
    # print selected_pop
    # print ""
    return selected_pop

    elif puzzle == 2:
        # Will write this <---------------------------------------------------------------------------
    elif puzzle == 3:
        # Will write this <---------------------------------------------------------------------------
    else:
        print "Error: invalid puzzle in Select"


# Crossover between strings in population
def crossover(parent_pop, temperature, puzzle):
    if puzzle == 1:
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

    elif puzzle == 2:
        # Tri write this (using partial crossover )    <---------------------------------------------------------------------------
    elif puzzle == 3:
        # Tri write this                               <---------------------------------------------------------------------------
    else:
        print "Error: Invalid puzzle in Crossover"

# Mutate strings in population
def mutate(children_pop, genes, temperature, puzzle):
    # print "Before: " + str(len(children_pop))
    # print children_pop
    if puzzle == 1:
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
    # print "After: " + str(len(mutated_pop))
    # print mutated_pop
    return mutated_pop
    elif puzzle == 2:
        # Jetro write this part <---------------------------------------------------------------------------
    elif puzzle == 3:
        # Jetro wirte this part (similar to 1) <---------------------------------------------------------------------------
    else:
        print "Error: Invalid Puzzle in Mutation"

# ==== Print Stats ====
def print_stats(top_score, top_str, f_top_str, ts_gen, total_gen):
    # best score
    print "Top Score: " + str(top_score)
    # first best string
    print "First Top String: " + str(top_str)
    # first best score gen
    print "First Top Score Generation: " + str(ts_gen)
    # final best string
    print "Final Top String: " + str(f_top_str)
    # total gen
    print "Total Generations: " + str(total_gen)
    '''
    # stable solutions over time
    print "Stable Strings v.s. Time"
    for e in data_set:
        print "Generation " + str(e[0]) + ":\t",
        for i in range(0, e[1]):
            print "*",
        print ''
    '''
# ======== Format Input ========

puzzle_num = int(sys.argv[1])
fd = [line for line in fi.input(sys.argv[2])]
fi.close()
# Runtime in seconds
run_time = int(sys.argv[3])

# Set target value
target = -1
if puzzle_num == 1:
    target = float(fd[0])
    del fd[0]

# Format fd
if puzzle_num == 1 or puzzle_num == 2:
    for i in range(0, len(fd)):
        fd[i] = float(fd[i])
elif puzzle_num == 3:
    for i in range(0, len(fd)):
        tmp = fd[i].split('\t')
        fd[i] = (tmp[0], int(tmp[1]), int(tmp[2]), int(tmp[3]))
else:
    print "Error: Invalid puzzle_num argument [1 - 3]"
    sys.exit()

# ======== Run Genetic Algorithm ========
time_elapsed = 0
temperature = 0
record = -1
record_string = []
record_gen = 0
total_gen = 0
start_time = time.time()
a_list = []
b_list = []
c_list = []
d_list = []
population = gen_init_pop(puzzle_num, fd, 20)

while time_elapsed <= run_time:
    # Time in seconds
    time_elapsed = time.time() - start_time
    temperature = math.exp((-4*time_elapsed/run_time)- 0.3)
    # Evaluate
    a_list = evaluate(puzzle_num, target, population, fd)
    
    # Record statistics
    score = 0.0
    if puzzle_num == 1:
        score = sum(a_list[-1][1])
    elif puzzle_num == 2:
        score = puzzle_2_score_calc(a_list[-1][1])
    elif puzzle_num == 3:
        score = puzzle_3_score_calc(a_list[-1][1])
    else:
        print "Error: Invalid Puzzle in main()"
        sys.exit()
    if score > record:
        record = score
        record_string = a_list[-1][1]
        record_gen = total_gen
    
    # Selection
    # b_list = select(a_list)
    # Crossover
    # c_list = crossover(b_list, temperature)
    # Mutation
    # d_list = mutate(c_list, fd, temperature)
    population = a_list
    print population
    '''
    sol_num = 0
    for e in population:
        if sum(e) == record:
            sol_num += 1
    # print temperature
    if total_gen % 2000 == 0:
        sol_tup = (total_gen, sol_num)
        sol_tally.append(sol_tup)
    '''
    total_gen += 1

print ''
final_string = population[0]
print_stats(record, record_string, final_string, record_gen, total_gen)

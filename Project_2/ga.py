import fileinput as fi
import random as rand
from operator import itemgetter
import os.path
import math
import sys
import time 
import csv

# ======== Program Constants ========

P_SIZE = 100 # USER INPUT
# 3 - both, 2 - elitism, 1 - culling, 0 - none
FIT_MODE = 3 # USER INPUT

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

# == Helper Functions ==

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

# Calculate score for puzzle 1
def puzzle_1_score_calc(string, chars, target):
    score = 0.0
    score = float(sum(string)) 
    diff = target - score
    if diff < 0:
        score = 0.0
    if not no_repeats(string, chars):
        score = 0.0
    return score

# Calculate score for puzzle 2
def puzzle_2_score_calc(string, chars):
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
    if not no_repeats(string, chars):
        score = 0.0
    return score

# Calculate score for puzzle 3
def puzzle_3_score_calc(tower, chars):
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
            total_cost += tower[i][3]

    score = 10 + total_height**2 - total_cost
    if not no_repeats(tower, chars):
        score = 0.0
    return score

# == Primary GA Functions ==

# Evaluate fitness of strings
def evaluate(puzzle, target, population, genes, fit_num):
    raw_pop = []
    total_value = 0.0

    for element in population:
        fitness_val = 0.0
        score = 0.0
        
        # Calculate string score
        if puzzle == 1:
            score = puzzle_1_score_calc(element, genes, target)
            fitness_val = score**2 + 0.0001
        elif puzzle == 2:
            score = puzzle_2_score_calc(element, genes)
            if score < 0.0:
                score = 0.0
            fitness_val = score**3 + 0.0001
        elif puzzle == 3:
            score = puzzle_3_score_calc(element, genes)
        else:
            print "Error: In evaluate() - Invalid Puzzle Number"
            sys.exit()
        
        # fitness_val = score**2 + 0.0001
        total_value += fitness_val

        element_tup = [fitness_val, element]
        raw_pop.append(element_tup)

    # Organize elements by fitness values
    raw_pop.sort(key = lambda x: x[0])
    # Cull bad strings
    for i in range(0, fit_num):
        total_value -= raw_pop[i][0]
        raw_pop[i][0] = 0
    # Accumulate element fitness values
    for i in range(1, len(raw_pop)):
        raw_pop[i][0] += raw_pop[i - 1][0]
    # Normalize element fitness values
    for i in range(0, len(raw_pop)):
        try:
            raw_pop[i][0] /= total_value
        except ZeroDivisionError:
            print "Error: In evaluate() - Divide by Zero"
            print "Exit Population:"
            print population
            sys.exit()

    return raw_pop

# Select strings from old population to create new population
# Roulette selection
def select(ordered_pop, fit_num):
    selected_pop = []
    cutoff = rand.random()
    
    # Elitism guarantees survival of fittest
    for x in range(0, fit_num):
        selected_pop.append(ordered_pop[-x-1][1])
    for x in range(fit_num, len(ordered_pop)):
        for i in ordered_pop:
            if i[0] > cutoff:
                selected_pop.append(i[1])
                cutoff = rand.random()
                break
    
    return selected_pop

# Crossover between strings in population
def crossover(parent_pop, temperature, puzzle, fit_num):
    children_pop = []
    for i in range(0, fit_num):
        children_pop.append(parent_pop.pop(0))

    if puzzle == 1 or puzzle == 3:
        string_buf = []
        rand.shuffle(parent_pop)
        for string in parent_pop:
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

    elif puzzle == 2:
        string_buf = []
        rand.shuffle(parent_pop)
        for string in parent_pop:
            co_chance = rand.random()
            if co_chance > 1 - temperature:
                if not string_buf:
                    string_buf = string
                else:
                    a_string = string_buf # parent a
                    b_string = string # parent b

                    # Partial crossover so get a beginning and end index in a
                    begin_index = rand.randint(0, len(a_string) - 1)
                    end_index = rand.randint(begin_index, len(a_string))
                    
                    # Substring from parent a
                    sub_a_string_1 = a_string[begin_index:end_index]
                    sub_b_string_1 = []
                    
                    sub_b_string_2 = b_string[begin_index:end_index]
                    sub_a_string_2 = []
                    
                    while len(sub_b_string_1) < begin_index:
                        index = rand.randint (0, len(b_string) - 1)
                        s = b_string[index]
                        if sub_b_string_1.count(s) + sub_a_string_1.count(s) < a_string.count(s):
                            sub_b_string_1.append(s)

                    while len(sub_a_string_2) < begin_index:
                        index = rand.randint (0, len(a_string) - 1)
                        s = a_string[index]
                        if sub_a_string_2.count(s) + sub_b_string_2.count(s) < b_string.count(s):
                            sub_a_string_2.append(s)

                    result_string_1 = sub_b_string_1 + sub_a_string_1
                    result_string_2 = sub_a_string_2 + sub_b_string_2

                    while len(result_string_1) < len(a_string):
                        index = rand.randint (0, len(b_string) - 1)
                        s = b_string[index]
                        if result_string_1.count(s) < a_string.count(s):
                            result_string_1.append(s)

                    while len(result_string_2) < len(b_string):
                        index = rand.randint (0, len(a_string) - 1)
                        s = a_string[index]
                        if result_string_2.count(s) < b_string.count(s):
                            result_string_2.append(s)
                    
                    children_pop.append(result_string_1)
                    children_pop.append(result_string_2)
                    
                    string_buf = []
            else:
                children_pop.append(string)
                    
        if string_buf:
            children_pop.append(string_buf)

#    elif puzzle == 3:
#        # Tri write this                               <---------------------------------------------------------------------------
#        string_buf = []
#        rand.shuffle(parent_pop)
#        for string in parent_pop:
#            if co_chance > 1 - temperature:
#                if not string_buf:
#                    string_buf = string
#                else:
#                    a_string = string_buf
#                    b_string = string
#                        
#                    a_index = rand.randint(0, len(a_string))
#                    b_index = rand.randint(0, len(b_string))
#                        
#                    c_string = a_string[:a_index] + b_string[b_index:]
#                    d_string = a_string[a_index:] + b_string[:b_index]
#
#                    children_pop.append(c_string)
#                    children_pop.append(d_string)
#        
#                    string_buf = []
#            else:
#                children_pop.append(string)
#
#        if string_buf:
#            children_pop.append(string_buf)
    else:
        print "Error: Invalid puzzle in Crossover"
        return

    return children_pop

# Mutate strings in population
def mutate(children_pop, genes, temperature, puzzle, fit_num):
    mutated_pop = []
    for i in range(0, fit_num):
        mutated_pop.append(children_pop.pop(0))
    
    if puzzle == 1:
        for string in children_pop:
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
    
    elif puzzle == 2:
        # Jetro write this part <---------------------------------------------------------------------------
        #puzzle 2 has to shuffle
        for string in children_pop:
            m_index1 = 0
            m_index2 = 0
            if string:
                #create first random index and second random index
                m_index1 = rand.randint(0, 9) #for bin 1
                m_index2 = rand.randint(10, 19) #for bin 2
            m_chance = rand.random()
            string_buf = []
            if m_chance > 1 - temperature:
                #take out two random gene in the genes sequence
                #this is for bin 1
                string_buf = string
                temporary_value = string_buf[m_index1]
                string_buf[m_index1] = string_buf[m_index1+20]
                string_buf[m_index1+20] = temporary_value

                #this is for bin 2
                temporary_value2 = string_buf[m_index2]
                string_buf[m_index2] = string_buf[m_index2+10]
                string_buf[m_index2+10] = temporary_value2

                mutated_pop.append(string_buf)
            else:
                mutated_pop.append(string)
        
    elif puzzle == 3:
         for string in children_pop:
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
                
    else:
        print "Error: Invalid Puzzle in Mutation"

    return mutated_pop

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

# ==== Collect Statistics ====

def collect_stats(generation, puzzle_num, genes, population):
    stat_entry = []
    b_performance = 0
    w_performance = 0
    m_performance = 0
    m_index = int(len(population)/2)
    scores = []
    for i in range(0, len(population)):
        entry_string = population[i]
        if puzzle_num == 1:
            entry_score = puzzle_1_score_calc(entry_string, genes, target)
        elif puzzle_num == 2:
            entry_score = puzzle_2_score_calc(entry_string, genes)
        elif puzzle_num == 3:
            entry_score = puzzle_3_score_calc(entry_string, genes)
        scores.append(entry_score)
    scores.sort()

    b_performance = scores[-1]
    w_performance = scores[0]
    m_performance = scores[m_index]

    stat_entry.append(generation)
    stat_entry.append(b_performance)
    stat_entry.append(w_performance)
    stat_entry.append(m_performance)
    return stat_entry

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

elite_num = 0
cull_num = 0
if FIT_MODE == 1:
    cull_num = int(P_SIZE/5) + 1
elif FIT_MODE == 2:
    elite_num = int(P_SIZE/5) + 1
elif FIT_MODE == 3:
    cull_num = int(P_SIZE/5) + 1
    elite_num = cull_num

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
stat_sheet = []

population = gen_init_pop(puzzle_num, fd, P_SIZE)

while time_elapsed <= run_time:
    # Time in seconds
    time_elapsed = time.time() - start_time
    temperature = math.exp((-4*time_elapsed/run_time) - 0.3)
    # Evaluate
    a_list = evaluate(puzzle_num, target, population, fd, cull_num)
    
    # Record statistics
    score = 0.0
    if puzzle_num == 1:
        score = puzzle_1_score_calc(a_list[-1][1], fd, target)
    elif puzzle_num == 2:
        score = puzzle_2_score_calc(a_list[-1][1], fd)
    elif puzzle_num == 3:
        score = puzzle_3_score_calc(a_list[-1][1], fd)
    else:
        print "Error: Invalid Puzzle in main()"
        sys.exit()
    if score > record:
        record = score
        record_string = a_list[-1][1]
        record_gen = total_gen

    # Selection
    b_list = select(a_list, elite_num)
    # Crossover
    c_list = crossover(b_list, temperature, puzzle_num, elite_num)
    # Mutation
    d_list = mutate(c_list, fd, temperature, puzzle_num, elite_num)
    population = d_list
    print population
    print ''
    # Collect statistics
    if total_gen % 50 == 0:
        stat_sheet.append(collect_stats(total_gen, puzzle_num, fd, population))
    # print temperature
    total_gen += 1

print ''
final_string = population[0]
print_stats(record, record_string, final_string, record_gen, total_gen)
# Generate csv data file
file_num = 0
file_name = "P_" + str(puzzle_num) + "_N_" + str(file_num)  + ".csv"
while os.path.isfile(file_name):
    file_num += 1
    file_name = "P_" + str(puzzle_num) + "_N_" + str(file_num)  + ".csv"

csv_file = open(file_name, 'w')
col_0 = "Generation"
col_1 = "Best Score"
col_2 = "Worst Score"
col_3 = "Median Score"
field_names = [col_0, col_1, col_2, col_3]
writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=field_names)

writer.writeheader()
for entry in stat_sheet:
    writer.writerow({col_0: entry[0], col_1: entry[1], col_2: entry[2], col_3: entry[3]})

csv_file.close()

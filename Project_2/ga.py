import fileinput as fi
import sys
import random as rand

# ==== Functions ====

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

def rand_string(puzzle, GP):
    chars = GP
    string = []
    string_len = -1

    # Puzzle 1
    if puzzle == 1:
        string_len = rand.randint(1, len(chars))
    # Puzzle 2
    elif puzzle == 2:
        string_len = 30
    # Puzzle 3
    elif puzzle == 3:
        string_len = rand.randint(1, len(chars))
    else:
        print "Error: Invalid Puzzle Number"
    
    for i in range(0, string_len):
        c = rand.choice(chars)
        string.append(c)
        chars.remove(c)

    print "Generated: " + string
    return string

# Evaluate fitness of strings

# Select strings from old population to create new population

# Crossover between strings in population

# Mutate strings in population

# ==== Format Input ====

puzzle_num = int(sys.argv[1])
fd = [line for line in fi.input(sys.argv[2])]
fi.close()
run_time = int(sys.argv[3])

# Only for puzzle 1
T = 0
if puzzle_num == 1:
    T = int(fd[0])
    del fd[0]

# ==== Run Genetic Algorithm ====


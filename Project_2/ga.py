import fileinput
import sys

# ==== Functions ====

# Genererate initial population

# Evaluate fitness of strings

# Select strings from old population to create new population

# Crossover between strings in population

# Mutate strings in population

# ==== Format Input ====

puzzle_num = int(sys.argv[1])
fd = [line for line in fileinput.input(sys.argv[2])]
fileinput.close()
run_time = int(sys.argv[3])

# ==== Run Genetic Algorithm ====


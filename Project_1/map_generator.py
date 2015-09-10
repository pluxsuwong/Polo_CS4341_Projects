import sys
import random

# run this program as such:
# python map_generator.py <new_file_name> <table_width> <table_height>

col = int(sys.argv[2])
row = int(sys.argv[3])
f_name = './' + sys.argv[1]
fd = open(f_name, 'w+')
map_str = ""

start = [random.randint(0, col - 1), random.randint(0, row - 1)]
goal = [random.randint(0, col - 1), random.randint(0, row - 1)]
if start[0] == goal [0] and start[1] == goal[1]:
    goal = [random.randint(0, col - 1), random.randint(0, row - 1)]

for j in range(0, row):
    for i in range(0, col):
        if i == start[0] and j == start[1]:
            map_str += 'S'
        elif i == goal[0] and j == goal[1]:
            map_str += 'G'
        else:
            map_str += str(random.randint(1, 9))

        if i == col - 1:
            map_str += '\r\n'
        else:
            map_str += '\t'
fd.write(map_str)

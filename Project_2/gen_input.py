import random as rand
import sys

puzzle = int(sys.argv[1])
name = ""
if puzzle == 1:
    name = "file_input_1.txt" 
elif puzzle == 2:
    name = "file_input_2.txt" 
elif puzzle == 3:
    name = "file_input_3.txt" 
else:
    print "Invalid Puzzle Number"
    sys.exit()

fh = open(name, 'w')

if puzzle == 1:
    gene_pool_size = rand.randint(4, 51)
    target = rand.randint(gene_pool_size, 4*gene_pool_size)
    fh.write(str(target) + '\n')
    for i in range(0, gene_pool_size):
        tmp = rand.randint(1, gene_pool_size)
        fh.write(str(tmp) + '\n')
elif puzzle == 2:
    for i in range(0, 30):
        tmp = rand.uniform(-10, 10)
        fh.write(str(tmp) + '\n')
elif puzzle == 3:
    floor_types = ["Door", "Wall", "Lookout"]
    gene_pool_size = rand.randint(4, 20) 
    for i in range(0, gene_pool_size):
        tmp_t = rand.choice(floor_types)
        tmp_w = rand.randint(1, 9)
        tmp_s = rand.randint(1, 9)
        tmp_c = rand.randint(1, 5)
        tmp = tmp_t + '\t' + str(tmp_w) + '\t' \
            + str(tmp_s) + '\t' + str(tmp_c) + '\n' 
        fh.write(tmp)

fh.close()
    

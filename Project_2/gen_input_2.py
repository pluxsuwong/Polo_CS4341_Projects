import random as rand

fh = open("file_input_2.txt", "w")

for i in range(0, 30):
    tmp = rand.uniform(-10, 10)
    tmp = round(tmp, 1)
    fh.write(str(tmp) + "\n")

fh.close()
    

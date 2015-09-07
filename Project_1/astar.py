import fileinput
import re


fd = [line for line in fileinput.input()]


terrain = []    # 2-D list of lists
for line in fd:
    raw_row = re.split(r'\t+', line.rstrip('\t\r\n'))
    new_row = []
    for c in raw_row:
        try:
            new_row.append(int(c))
        except ValueError:
            new_row.append(c)
    terrain.append(new_row)



print terrain

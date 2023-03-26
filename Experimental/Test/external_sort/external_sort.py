import numpy as np

# User defined
memory_size = 16
intermediate = "intermediate_files/"

# Variables for code
starting_file = 0
memory_size = memory_size // 2 #so we can merge with two whole files

def read_in_chunks(file_object, chunk_size=8):
    """Lazy function (generator) to read a file piece by piece."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

# First, load in each chunk of memory_size, and sort in place

file1 = open("arr.txt", "r")

for piece in read_in_chunks(file1):
    data = piece.replace('\n', '').replace(',','')
    data = [int(d) for d in str(data)]

    # Sort array peice
    data.sort()

    # write to new file
    f = open(intermediate + "arr_" + str(starting_file) + ".txt", "w")
    f.write(str(data))
    starting_file += 1
    f.close()
        
file1.close()

# Now merge all arrays together

# Naive method, open all files at the same time and output smallest first

output_file = open("sorted_arr.txt", "w")

interm_files = []

# Open all intermediate files
for i in range(starting_file):
    interm_files.append(open(intermediate + "arr_" + str(i) + ".txt", "r"))

cur_read_values = [int(interm_files[i].read(3).replace('\n', '').replace(',','').replace('[','').replace(']','')) for i in range(len(interm_files))]

print(any(cur_read_values))
while any(cur_read_values):
    # Get smallest value and index
    print(cur_read_values)
    index_min = np.argmin(np.array(cur_read_values))
    min_val = min(cur_read_values)

    if min_val == np.inf:
        break

    # Write the min value
    output_file.write(str(min_val) + ',')

    # Update cur_read_values
    try:
        new_val = int(interm_files[index_min].read(3).replace('\n', '').replace(',','').replace('[','').replace(']','').replace(' ',''))
    except:
        new_val = np.inf
    
    if new_val == '':
        break
    
    cur_read_values[index_min] = new_val

# Close all intermediate files
for i in range(len(interm_files)):
    interm_files[i].close()

output_file.close()
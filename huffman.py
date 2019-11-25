import heapq
import sys

if len(sys.argv) < 2:
    print("Usage: python3 pa5.py <book_name>")
    sys.exit(1)

filename = sys.argv[1]
file = open(filename, 'r')
text = file.read()

# Generate the frequencies of all characters that belong to ASCII table (0-127)
D = {}

for i in text:
    if ord(i) < 128:
        if i in D:
            D[i] += 1
        else:
            D[i] = 1

# Create an array of tuples that have the following scheme
# (frequency, character, left, right)
char_heap = [
    (D[i], i, None, None, None)
    for i in D]
# Heapify the created array
heapq.heapify(char_heap)

# Merge least frequencies and create a superTuple
while len(char_heap) > 1:
    left = heapq.heappop(char_heap)
    right = heapq.heappop(char_heap)
    # print(left[0])
    node = (left[0] + right[0], left[1] + right[1], left, right)
    heapq.heappush(char_heap, node)


lut = {}

# Function for populating a look-up table of the character and its corresponding code
def traverse_tuple(root, str):
    curr_char = root[1]
    left = root[2]
    right = root[3]
    if left is None and right is None:
        lut[curr_char] = str
    else:
        traverse_tuple(left, str + '0')
        traverse_tuple(right, str + '1')
    return

# Traverse superTuple and populate the look-up table
traverse_tuple(char_heap[0], '')

# Print the character and its corresponding code
for i in lut:
    # Edge case of newline character handled differently
    if i == '\n':
        print('\'' + '\\n' + '\'' + ':', lut[i])
    else:
        print('\'' + str(i) + '\'' + ':', lut[i])


encoded_text = ''
# Encode the entire book using our look-up table
for i in text:
    if ord(i) < 128:
        encoded_text += lut[i]

# Calculate and compare savings with 7-bit fixed encoding
encoding_cost = len(encoded_text)
original_cost = len(text) * 7
savings = original_cost - encoding_cost
print("Original:", original_cost, "Encoded:", encoding_cost, "Savings:", savings)
print("Original(Kb):", original_cost/(1024*8), "Encoded(Kb):", encoding_cost/(1024*8), "Savings(Kb):", savings/(1024*8))

print("Compression factor:", savings / original_cost)

# Test my recursive seat allocation algorithm using 'bitstring'
# Passed all the tests I submitted

from bitstring import BitArray
from random import randint

CAPACITY = 96  # Number of seats in the aircraft
LEFT_BIT_POS = CAPACITY - 1  # I.E. 95


def row_of_N_seats(number_needed, allocated, available):
    """ Find a 'row' of 'number_needed' seats """
    zeros = "0b" + "0"*number_needed
    result = available.find(zeros)
    if not result:
        return (False, allocated, available)

    # Set the bits to 1 to represent 'taken' seats
    bitrange = range(result[0], result[0] + number_needed)
    available.invert(bitrange)

    """
    Airlines generally seat passengers from the back of the aircraft
    So interpret the leftmost bit as position 95
    95 94 93 ... 2 1 0
     0  0  0 ... 0 0 0

    Then add that range of seats to the 'allocated' list
    """

    """
    Determine the range of seat positions
    e.g. 6 seats at position 77
    77-6+1 = 72
    so range(72, 78) = 72, 73, 74, 75, 76, 77
    """
    end = LEFT_BIT_POS - result[0]
    start = end - number_needed + 1
    seat_range = range(start, end + 1)
    allocated += [*seat_range]
    return (True, allocated, available)


def find_N_seats(number_needed, allocated, available):
    """
    Find 'N' number of seats
    N being 'number_needed'
    'allocated' are all the seats found so far
    'available' is a bitstring depicting what is available
    This is a recursive algorithm
    """

    result = row_of_N_seats(number_needed, allocated, available)
    if result[0]:
        # Successfully found a row of N seats - so allocation is done!
        return result

    # if N = 1 then no available seats i.e. the flight is full
    if number_needed == 1:
        return (False, allocated, available)

    # Otherwise, starting with M=N-1,
    # see if it is possible to find a row of M seats
    # if so, allocate that row of seats
    # then see if the remainder can be allocated
    minus1 = number_needed - 1
    count = number_needed - 1
    while count != 1:
        result = row_of_N_seats(count, allocated, available)
        if not result[0]:
            # Try a smaller row allocation
            count -= 1
            continue

        remainder_needed = number_needed - count
        remainder = find_N_seats(remainder_needed,
                                 allocated + result[1], result[2])
        if remainder[0]:
            # Found all the seats!
            return remainder

    # Not successful in finding any 'row' > 1
    # Therefore, allocate one seat
    # Then repeat 'find_N_seats' for the remainder

    result = row_of_N_seats(1, allocated, available)
    # Finding one seat at this stage should not fail
    if not result[0]:
        print("BUG: FAILED TO ALLOCATE ONE SEAT WHEN "
              "THERE OUGHT TO BE AVAILABILITY")
        print(available)
        print(available.bin)
        quit()

    return find_N_seats(minus1,
                        allocated + result[1], result[2])


def seat_number(number):
    """
    Convert the number into its corresponding 'Seat Number'
    That is,
    0 is 1A, 1 is 1B , 2 is 1C, 3 is 1D, 4 is 2A, ...
    91 is 23D, 92 is 24A, 93 is 24B, 94 is 24C, 95 is 24D

    So each row has 4 seats
    """

    try:
        # raise ValueError if 'Non numeric value'
        # Strictly speaking, this shouldn't happen!
        number = int(number)
        if number < 0 or number > LEFT_BIT_POS:
            raise ValueError
        divided_by4 = divmod(number, 4)
        result = f"{divided_by4[0] + 1}{chr(divided_by4[1] + 65)}"
    except ValueError:
        result = ""
    finally:
        return result


# VARIOUS TESTS
# Empty Plane - All zeros
seatmap = BitArray(bin="0" * CAPACITY)

# TEST 1
# Find one seat
result = find_N_seats(1, [], seatmap)
print("TEST 1")
print(result)
print(result[2].bin)
"""
TEST 1
(True, [95], BitArray('0x800000000000000000000000'))
100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""

# Find another seat
seatmap = result[2]
allocated = result[1]
result = find_N_seats(1, allocated, seatmap)
print(result)
print(result[2].bin)

"""
(True, [95, 94], BitArray('0xc00000000000000000000000'))
110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""

# Find 3 more seats
seatmap = result[2]
allocated = result[1]
result = find_N_seats(3, allocated, seatmap)
print(result)
print(result[2].bin)

"""
(True, [95, 94, 91, 92, 93], BitArray('0xf80000000000000000000000'))
111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""

# TEST 2
# Randomly set 20 seats
# Then allocate seats until there are no more available
# The number of seats allocated should be 96-20 = 76

# Empty Plane - All zeros
seatmap = BitArray(bin="0" * CAPACITY)
count = 20
bits_set = set()

print("TEST 2")

while count:

    # random.randint(a, b)
    # Return a random integer N such that a <= N <= b.
    # Alias for randrange(a, b+1).
    r = randint(0, CAPACITY)
    # Ensure this position hasn't been used prior
    if r in bits_set:
        continue

    # Unused position
    # set the bit to '1'
    seatmap.overwrite("0b1", r)
    # Indicate used
    bits_set.add(r)
    count -= 1
print(seatmap.bin)

"""
TEST 2
110000010010000100000011000110000010001000100000000000000011001010001000001100000000000000100000
"""
twenty_random_bits = seatmap.copy()  # Keep for later
count = 0
allocated = []
while True:
    result = find_N_seats(1, allocated, seatmap)
    if not result[0]:
        break
    count += 1
    allocated = result[1]
    seatmap = result[2]
print(count)
print(result)
print(result[2].bin)  # BINARY
print(result[2])  # HEX

"""
76
(False, [93, 92, 91, 90, 89, 87, 86, 84, 83, 82, 81, 79, 78, 77, 76, 75, 74,
71, 70, 69, 66,
65, 64, 63, 62, 60, 59, 58, 56, 55, 54, 52, 51, 50, 49, 48, 47, 46, 45, 44,
43, 42, 41, 40, 39,
38, 35, 34, 32, 30, 29, 28, 26, 25, 24, 23, 22, 19, 18, 17, 16, 15, 14, 13,
12, 11,
10, 9, 8, 7, 6, 4, 3, 2, 1, 0],
BitArray('0xffffffffffffffffffffffff'))

111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

0xffffffffffffffffffffffff
"""

"""
TEST 2 AGAIN:
000001100000000000000000101010100000000000101100100000000000000001001110000010000000001010010011
76
(False, [95, 94, 93, 92, 91, 88, 87, 86, 85, 84, 83, 82, 81, 80,
79, 78, 77, 76, 75,74, 73, 72, 70, 68, 66, 64, 63, 62, 61, 60, 59,
58, 57, 56, 55, 54, 52, 49, 48, 46, 45, 44, 43, 42, 41, 40, 39, 38,
37, 36, 35, 34, 33, 32, 31, 29, 28, 24, 23, 22, 21, 20, 18, 17, 16,
15, 14, 13, 12, 11, 10, 8, 6, 5, 3, 2], BitArray('0xffffffffffffffffffffffff'))

111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
0xffffffffffffffffffffffff
"""

# TEST 3 - same as TEST 2 above however show the entire 96 seats
# Randomly set 20 seats
# Then allocate seats until there are no more available
# The number of seats allocated should be 96-20 = 76


# 20 seats randomly chosen
seatmap = twenty_random_bits
allocated = list(bits_set)
print("TEST 3")
print(seatmap.bin)
print(allocated)

"""
TEST 3
100000000010000101110001000010000000010000000100000000001011001001010000000001010000000100000001
[0, 10, 15, 17, 18, 19, 23, 28, 37, 45, 56, 58, 59, 62, 65, 67, 77, 79, 87, 95]
"""
count = 0
while True:
    result = find_N_seats(1, allocated, seatmap)
    if not result[0]:
        break
    count += 1
    allocated = result[1]
    seatmap = result[2]
print(count)
print(result)
print(len(result[1]))
print(result[2].bin)  # BINARY
print(result[2])  # HEX
s = result[2]
print(type(s))  # <class 'bitstring.bitarray.BitArray'>
print(str(s.hex).startswith("0x"))
print(str(s.hex.upper()), len(s.hex))

"""
76
(False, [0, 10, 15, 17, 18, 19, 23, 28, 37, 45,
56, 58, 59, 62, 65, 67, 77, 79, 87,
95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 84, 83,
82, 81, 79, 75, 74, 73, 71, 70, 69,
68, 66, 65, 64, 63, 62, 61, 60, 59, 57, 56, 55,
54, 53, 52, 51, 49, 48, 47, 46, 45,
44, 43, 42, 41, 40, 38, 35, 34, 32, 31, 29, 27,
26, 25, 24, 23, 22, 21, 20, 19, 17,
15, 14, 13, 12, 11, 10, 9, 7, 6, 5, 4, 3, 2, 1],
BitArray('0xffffffffffffffffffffffff'))
96
111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
0xffffffffffffffffffffffff
<class 'bitstring.bitarray.BitArray'>
False
FFFFFFFFFFFFFFFFFFFFFFFF 24
"""

"""
TEST 3 AGAIN:
100000100010001010000000000001000001101011011000000000100100000000000001100001000000100001000000
[0, 6, 10, 14, 16, 29, 35, 36, 38, 40, 41, 43, 44, 54, 57, 71, 72, 77, 84, 89]
76

(False, [0, 6, 10, 14, 16, 29, 35, 36, 38, 40, 41, 43, 44, 54, 57, 71, 72, 77,
84, 89, 94, 93, 92, 91, 90, 88, 87, 86, 84, 83, 82, 80, 78, 77, 76, 75, 74, 73,
72, 71, 70, 69, 68, 67, 65, 64, 63, 62, 61, 58, 56, 53, 50, 49, 48, 47, 46, 45,
44, 43, 42, 40, 39, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 22, 21,
20, 19, 17, 16, 15, 14, 13, 12, 10, 9, 8, 7, 5, 4, 3, 2, 1, 0],
BitArray('0xffffffffffffffffffffffff'))

96
111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
0xffffffffffffffffffffffff
<class 'bitstring.bitarray.BitArray'>
False
FFFFFFFFFFFFFFFFFFFFFFFF 24
"""

"""
TEST 4
Randomly attempt to allocate 20 different rows of seats
beginning with an empty seat map
After that fill the plane and the number of allocated seats ought to be 96

RAN TEST 4 AGAIN - THIS TIME DOING 10 ROWS INSTEAD OF 20 - CALLED TEST4A
"""

print("TEST 4")

# Empty Plane - All zeros
available = BitArray(bin="0" * CAPACITY)
allocated = []
count = 10  # count = 20

while count:

    # random.randint(a, b)
    # Return a random integer N such that a <= N <= b.
    # Alias for randrange(a, b+1).
    # rows of 2 to 10 seats at a time
    rowsize = randint(2, 10)
    print(rowsize)
    result = row_of_N_seats(rowsize, allocated, available)
    if result[0]:
        allocated = result[1]
        available = result[2]
    count -= 1

# Up to 20 rows allocated
print(available.bin)  # BINARY
print(available)  # HEX
print(allocated)
print(len(allocated))

# Fill the rest

while True:
    result = find_N_seats(1, allocated, available)
    if not result[0]:
        break

    allocated = result[1]
    available = result[2]

print(available.bin)  # BINARY
print(available)  # HEX
print(allocated)
print(len(allocated))  # should be 96

"""
TEST 4
9
4
3
7
8
5
9
10
10
3
7
7
9
3
7
4
10
6
9
10
111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100
0xfffffffffffffffffffffffc
[87, 88, 89, 90, 91, 92, 93, 94, 95, 83, 84, 85, 86, 80, 81, 82, 73, 74, 75,
76, 77, 78, 79, 65,
66, 67, 68, 69, 70, 71, 72, 60, 61, 62, 63, 64, 51, 52, 53, 54, 55, 56, 57, 58,
59, 41, 42, 43, 44,
45, 46, 47, 48, 49, 50, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 28, 29, 30, 21,
22, 23, 24, 25, 26, 27,
14, 15, 16, 17, 18, 19, 20, 5, 6, 7, 8, 9, 10, 11, 12, 13, 2, 3, 4]
94

*** The above bitstring confirms that there is indeed two slots left
Numbers 0 and 1 which are 'not' in the 'allocated' list above!

111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
0xffffffffffffffffffffffff
[87, 88, 89, 90, 91, 92, 93, 94, 95, 83, 84, 85, 86, 80, 81, 82, 73, 74, 75,
76, 77, 78, 79, 65,
66, 67, 68, 69, 70, 71, 72, 60, 61, 62, 63, 64, 51, 52, 53, 54, 55, 56, 57, 58,
59, 41, 42, 43, 44,
45, 46, 47, 48, 49, 50, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 28, 29, 30, 21,
22, 23, 24, 25, 26, 27,
14, 15, 16, 17, 18, 19, 20, 5, 6, 7, 8, 9, 10, 11, 12, 13, 2, 3, 4,
1, 0] <=== Confirms that the last two available slots were 0 and 1

96
"""

"""
TEST 4 AGAIN WITH 10 ROWS:
TEST4A

3
10
3
5
10
3
10
7
2
10
111111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000
0xfffffffffffffffe00000000

[93, 94, 95, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 80, 81, 82, 75, 76,
77, 78, 79, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 62, 63, 64, 52, 53, 54,
55, 56, 57, 58, 59, 60, 61, 45, 46, 47, 48, 49, 50, 51, 43, 44, 33, 34, 35,
36, 37, 38, 39, 40, 41, 42]

63

*** The above bitstring confirms that there should be (96 - 63 = 33) zeros
That is, 33 available slots left - I count 33!

111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
0xffffffffffffffffffffffff
[93, 94, 95, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 80, 81, 82, 75, 76,
77, 78, 79, 65, 66, 67,68, 69, 70, 71, 72, 73, 74, 62, 63, 64, 52, 53, 54,
55, 56, 57, 58, 59, 60, 61, 45, 46, 47, 48, 49, 50, 51, 43, 44, 33, 34, 35,
36, 37, 38, 39, 40, 41, 42,

*** What follows are indeed 33 new numbers! ***

32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21,
20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

96
"""

# TEST 5 - Allocate one seat at a time until full
# The number of allocated seats ought to be 96
# Ensure 'Allocated' is a 24-character string

print("TEST 5")

# Empty Plane - All zeros
available = BitArray(bin="0" * CAPACITY)
allocated = []

while True:
    result = find_N_seats(1, allocated, available)
    if not result[0]:
        break

    allocated = result[1]
    available = result[2]

# Show full flight
print(available.bin)  # BINARY
print(available)  # HEX
print(allocated)
print(len(allocated))  # should be 96

s = str(s.hex.upper())
print(s)
print(type(s))
print(len(s))


"""
TEST 5
111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
0xffffffffffffffffffffffff
[95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77,
76, 75, 74, 73, 72,
71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53,
52, 51, 50, 49, 48, 47,
46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28,
27, 26, 25, 24, 23, 22,
21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
96
FFFFFFFFFFFFFFFFFFFFFFFF
<class 'str'>
24
"""


"""
TEST 6 - Allocate one seat at a time until full
The number of allocated seats ought to be 96
Convert all numbers into actual 'Seat Numbers'
That is,
0 is 1A, 1 is 1B , 2 is 1C, 3 is 1D, 4 is 2A, ...
91 is 23D, 92 is 24A, 93 is 24B, 94 is 24C, 95 is 24D

So each row has 4 seats
"""

print("TEST 6")
print("-1", seat_number(-1))
print("ABC", seat_number("ABC"))
print(CAPACITY, seat_number(CAPACITY))
print(0, seat_number(0))

"""
TEST 6
-1
ABC
96
0 1A
"""

# Empty Plane - All zeros
available = BitArray(bin="0" * CAPACITY)
allocated = []

while True:
    result = find_N_seats(1, allocated, available)
    if not result[0]:
        break

    allocated = result[1]
    available = result[2]

# Show full flight
print(available.bin)  # BINARY
print(available)  # HEX
all_seat_numbers = set()
allocated.sort()
seats_list = [seat_number(number) for number in allocated]
print(seats_list)
print(len(seats_list))  # should be 96


"""
111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
0xffffffffffffffffffffffff
['1A', '1B', '1C', '1D', '2A', '2B', '2C', '2D', '3A', '3B', '3C', '3D',
'4A', '4B', '4C', '4D',
'5A', '5B', '5C', '5D', '6A', '6B', '6C', '6D', '7A', '7B', '7C', '7D',
'8A', '8B', '8C', '8D',
'9A', '9B', '9C', '9D', '10A', '10B', '10C', '10D', '11A', '11B', '11C', '11D',
'12A', '12B',
'12C', '12D', '13A', '13B', '13C', '13D', '14A', '14B', '14C', '14D',
'15A', '15B', '15C', '15D',
'16A', '16B', '16C', '16D', '17A', '17B', '17C', '17D',
'18A', '18B', '18C', '18D', '19A', '19B',
'19C', '19D', '20A', '20B', '20C', '20D', '21A', '21B', '21C', '21D',
'22A', '22B', '22C', '22D',
'23A', '23B', '23C', '23D', '24A', '24B', '24C', '24D']

96
"""

# TEST 7
# Ensure that I can convert from a String to a BitArray and back again!
print("TEST 7")
thestring = "0"*24  # empty flight
print(thestring)
bit_array = BitArray(length=96)
bit_array.overwrite("0x" + thestring, 0)
print(bit_array)
print(bit_array.bin)

# Fill the flight
allocated = []
available = bit_array

while True:
    result = find_N_seats(1, allocated, available)
    if not result[0]:
        break

    allocated = result[1]
    available = result[2]

# All bits should be set
print(bit_array)
print(bit_array.bin)

keep_a_copy = bit_array.copy()

# Convert to a string
new_string = str(bit_array.hex.upper())
print(len(new_string))
print(new_string)

bit_array = BitArray(length=96)
bit_array.overwrite("0x" + new_string, 0)

# This should be true?
print(bit_array == keep_a_copy)
# This should be 96
print(bit_array.count(1))
quit()

"""
TEST 7
000000000000000000000000
0x000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0xffffffffffffffffffffffff
111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
24
FFFFFFFFFFFFFFFFFFFFFFFF
True
96
"""

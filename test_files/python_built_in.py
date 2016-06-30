'''
File to test all of the
python builtin functions
'''

# Absolute value
value = -10
abs_value = abs(value)
print("Absolute {0}".format(abs_value))

# All bools
iteral = [True, True, True, True, False]
all_true = all(iteral)
print("All {0}".format(all_true))

# Any bool
any_true = any(iteral)
print("Any {0}".format(any_true))

# Ascii repr
nonscii = "\U00000394"
ascii_ver = ascii(nonscii)
print("Ascii {0}".format(ascii_ver))

# Bin
integer = 0x0FF
bin_str = bin(integer)
print("Bin {0}".format(bin_str))

# Bool (Bad way)
value = 0
boolean = bool(value)
print("Bool1 {0}".format(boolean))

# Bool best for ints
value = 1
boolean = not not value
print("Bool {0}".format(boolean))

# Byte array
arr = "Hello"
byters = bytearray(arr, "ascii")
byters = byters.upper()
byters = byters.decode()
print("Bytearray {0}".format(byters))

# Bytes
byters = bytes(arr, "ascii")
lists = [(lambda x: byters[x])(v) for v in len(list(byters))]
print("Bytes " + str(lists))

# Whatever i'm bored




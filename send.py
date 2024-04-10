def encode_string(s, num):
    encoded_sequence = []

    for char in s:
        if char in "aeiou":
            encoded_value = ord(char) * (num + 2)
        else:
            encoded_value = ord(char) * (num + 1)
        encoded_sequence.append(str(encoded_value))

    return ' '.join(encoded_sequence)

# Input
input_string = input()
input_integer = int(input())

# Encode the string
result = encode_string(input_string, input_integer)

# Output
print(result)

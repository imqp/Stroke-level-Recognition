def read_vietnamese_characters(file_path):
    """Read Vietnamese-Characters.txt and convert it to a dictionary."""
    char_to_num = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            char, num = line.strip().split()
            char_to_num[char] = int(num)
    return char_to_num

def encode_vietnamese_character(char, char_to_num):
    """Encode a character to its corresponding number."""
    return char_to_num.get(char, None)

def decode_vietnamese_character(num, char_to_num):
    """Decode a number to its corresponding character."""
    for char, value in char_to_num.items():
        if value == num:
            return char
    return None


def encode_word(word, char_to_num):
    """Encode a word to a list of numbers."""
    return [encode_vietnamese_character(char, char_to_num) for char in word]

def decode_word(numbers, char_to_num):
    """Decode a list of numbers to a word."""
    return ''.join([decode_vietnamese_character(num, char_to_num) for num in numbers])
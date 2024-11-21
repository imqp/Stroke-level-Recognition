# Generate single words from a text file

import os

if not os.path.exists('unique_words.txt'):
    with open('unique_words.txt', 'w') as file:
        file.write('')

# read unique words from a file
with open('unique_words.txt', 'r') as file:
    unique_words = set(file.read().split())

with open('unique_words.txt', 'w') as file:
    for word in unique_words:
        file.write(word + '\n')

# read the file
# with open('.txt', 'r') as file:
#     text = file.read()
text = ''
# format the text
def remove_special_characters(text):
    for c in text:
        if not c.isalpha():
            text = text.replace(c, ' ')

    # remove vn characters
    text = text.replace('vn', ' ')

    return text



text = remove_special_characters(text)

# split the text into words
words = text.split()
# print(words)

# remove empty strings
words = [word for word in words if word]

# convert to lowercase
words = [word.lower() for word in words]

# print the number of words
print(f'Total words: {len(words)}')

unique_words_from_text = set(words)


# combine old and new unique words
combined_unique_words = unique_words.union(unique_words_from_text)
new_unique_words = unique_words_from_text - unique_words

# print the number of unique words
print(f'New unique words: {len(new_unique_words)}')
print(f'Unique words: {len(combined_unique_words)}')


# Write the combined unique words to a file
with open('unique_words.txt', 'a') as file:
    for word in new_unique_words:
        file.write(word + '\n')
import random
import sys

def display_random_tamil_word(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
        random_word = random.choice(words)
        return random_word

# Set encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Example usage:
file_path = 'words.txt'  # Update with the path to your text file
random_tamil_word = display_random_tamil_word(file_path)
print("Randomly selected Tamil word:", random_tamil_word)





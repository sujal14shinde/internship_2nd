import random

WORDS = [
    "PYTHON", "DATHEON", "HANGMAN", "COMPUTER", "KEYBOARD",
    "PROGRAM", "DEVELOPER", "FUNCTION", "VARIABLE", "STRING",
    "NETWORK", "DATABASE", "ALGORITHM", "INTERFACE", "MODULE"
]

HANGMAN_STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========""",
]

def display_word(secret_word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in secret_word])

def play_hangman():
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    correct_letters = set()
    mistakes = 0
    max_mistakes = 6

    print("=" * 45)
    print("  HANGMAN - Word Guessing Game (Console)")
    print("=" * 45)
    print(f"Guess the hidden word letter by letter.")
    print(f"You have {max_mistakes} mistakes allowed.")
    print(f"Word length: {len(secret_word)} letters")

    while mistakes < max_mistakes:
        print(HANGMAN_STAGES[mistakes])
        print(f"\nWord: {display_word(secret_word, correct_letters)}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
        print(f"Attempts left: {max_mistakes - mistakes}")

        guess = input("\nEnter a letter: ").strip().upper()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (A-Z).")
            continue

        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. No penalty. Try another letter.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            correct_letters.add(guess)
            print(f"Correct! '{guess}' is in the word.")
            if all(letter in correct_letters for letter in secret_word):
                print(HANGMAN_STAGES[mistakes])
                print(f"\nWord: {display_word(secret_word, correct_letters)}")
                print(f"\nYOU WIN! The word was: {secret_word}")
                return
        else:
            mistakes += 1
            print(f"Wrong! '{guess}' is not in the word. Mistakes: {mistakes}/{max_mistakes}")

    print(HANGMAN_STAGES[mistakes])
    print(f"\nGAME OVER! You ran out of attempts.")
    print(f"The hidden word was: {secret_word}")

if __name__ == "__main__":
    while True:
        play_hangman()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break
import random
import csv
import os

# Function to read the default word list from CSV file
def get_word_list():
    word_list = []
    try:
        with open("words.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and len(row) >= 3:  # Ensure row has required columns
                    word_list.append({"word": row[0], "difficulty": row[1], "hint": row[2]})
    except FileNotFoundError:
        print("Error: words.csv file not found.")
        return []
    return word_list

# Function to read custom words added by the user
def get_custom_word_list():
    word_list = []
    try:
        with open("custom_words.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and len(row) >= 3:  # Ensure row has required columns
                    word_list.append({"word": row[0], "difficulty": row[1], "hint": row[2]})
    except FileNotFoundError:
        # Create the custom words file if it doesn't exist
        print("No custom words file found. Creating a new one.")
        with open("custom_words.csv", "w", newline="") as file:
            writer = csv.writer(file)
            # Optional header row is commented out
            # writer.writerow(["word", "difficulty", "hint"])
        return []
    return word_list

# Function to retrieve a random word with its hint based on difficulty level
def get_word_with_hint(difficulty, is_custom=False):
    # Select which word list to use based on user preference
    if is_custom:
        all_words = get_custom_word_list()
    else:
        all_words = get_word_list()
    
    if not all_words:
        return None, None
    
    # Filter the word list to match requested difficulty
    filtered_words = []
    for word_data in all_words:
        if word_data["difficulty"] == difficulty:
            filtered_words.append(word_data)
    
    # Handle case where no words match the difficulty
    if not filtered_words:
        return None, None
    
    # Select a random word from the filtered list
    word_data = random.choice(filtered_words)
    return word_data["word"].upper(), word_data["hint"]

# Function to allow users to add their own custom words
def add_custom_word():
    print("\n===== Add Custom Word =====")
    word = input("Enter the word: ").strip()
    
    if not word:
        print("Word cannot be empty.")
        return False
    
    # Difficulty selection menu
    print("Select difficulty level:")
    print("(E) Easy")
    print("(M) Medium")
    print("(H) Hard")
    difficulty_choice = input("Enter choice (E/M/H): ").upper()
    
    # Validate difficulty input
    while difficulty_choice not in ["E", "M", "H"]:
        difficulty_choice = input("Invalid choice. Enter (E/M/H): ").upper()
    
    # Convert single-letter choice to full difficulty name
    if difficulty_choice == "E":
        difficulty = "EASY"
    elif difficulty_choice == "M":
        difficulty = "MEDIUM"
    else:
        difficulty = "HARD"
    
    hint = input("Enter a hint for the word: ").strip()
    
    # Append the new word to custom_words.csv
    with open("custom_words.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([word, difficulty, hint])
    
    print(f"Word '{word}' added successfully!")
    return True

# Helper function to display the current game state
def display_progress(word_completion, guessed_letters):
    print("Guessed letters: ", " ".join(guessed_letters))
    print("Current word: ", word_completion)

# Main gameplay function
def play(word, hint, score=100):
    word_completion = "_" * len(word)  # Initialize with underscores for each letter
    guessed = False
    guessed_letters = []
    guessed_words = []
    remaining_attempts = 6  # Player has 6 incorrect guesses before losing
    wrong_guesses = 0
    hint_shown = False
    
    # Display initial game state
    print(display_hangman(remaining_attempts))
    display_progress(word_completion, guessed_letters)
    print("\n")
    
    # Main game loop
    while not guessed and remaining_attempts > 0:
        # Offer hint after 3 wrong guesses
        if wrong_guesses >= 3 and not hint_shown:
            hint_choice = input("Would you like a hint? (Y/N): ").upper()
            if hint_choice == "Y":
                print("Hint:", hint)
                hint_shown = True
        
        # Get the player's guess
        guess = input("Please guess a letter or word: ").upper()
        
        # Process a single letter guess
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in word:
                print(guess, "is not in the word.")
                remaining_attempts -= 1
                wrong_guesses += 1
                score -= 10  # Penalty for wrong guess
                guessed_letters.append(guess)
            else:
                print("Good job,", guess, "is in the word!")
                guessed_letters.append(guess)
                
                # Update the word completion display
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                score += 10  # Reward for correct guess
                
                # Check if the word is complete
                if "_" not in word_completion:
                    guessed = True
        
        # Process a full word guess
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                remaining_attempts -= 1
                wrong_guesses += 1
                score -= 10  # Penalty for wrong guess
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
                score += 10  # Reward for correct guess
        else:
            print("Not a valid guess.")
        
        # Update display after each guess
        print(display_hangman(remaining_attempts))
        display_progress(word_completion, guessed_letters)
        print("\n")
    
    # Display end-game message
    if guessed:
        print("Congrats, you guessed the word! You win! Your score is:", score)
    else:
        print("Sorry, you ran out of attempts. The word was " + word + ". Maybe next time! Your score is:", score)
    
    return score

# Function to display the hangman figure based on remaining attempts
def display_hangman(remaining_attempts):
    stages = [  # Array of hangman drawing stages
                # final state: head, torso, both arms, and both legs (0 attempts left)
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg (1 attempt left)
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     /
                   -
                """,
                # head, torso, and both arms (2 attempts left)
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |
                   -
                """,
                # head, torso, and one arm (3 attempts left)
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |
                   -
                """,
                # head and torso (4 attempts left)
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |
                   -
                """,
                # head only (5 attempts left)
                """
                   --------
                   |      |
                   |      O
                   |
                   |
                   |
                   -
                """,
                # initial empty state (6 attempts left)
                """
                   --------
                   |      |
                   |
                   |
                   |
                   |
                   -
                """
    ]
    return stages[remaining_attempts]

# Function to set up and start a game session
def play_game(is_custom=False):
    score = 100  # Initialize starting score
    
    # Game settings menu
    print("\n===== Game Settings =====")
    difficulty = input("Select difficulty level: Easy (E), Medium (M), Hard (H): ").upper()
    while difficulty not in ["E", "M", "H"]:
        difficulty = input("Invalid choice. Please select difficulty level: Easy (E), Medium (M), Hard (H): ").upper()
    
    # Convert single-letter input to full difficulty name
    if difficulty == "E":
        csv_difficulty = "EASY"
    elif difficulty == "M":
        csv_difficulty = "MEDIUM"
    else:
        csv_difficulty = "HARD"
    
    # Get a word based on the selected difficulty and word list
    word, hint = get_word_with_hint(csv_difficulty, is_custom)
    
    # Handle case where no words match the criteria
    if word is None:
        if is_custom:
            print(f"No {csv_difficulty} words found in custom words list.")
            return False
        else:
            print(f"No {csv_difficulty} words found in the default word list.")
            return False
    
    # Start the game with the selected word
    score = play(word, hint, score=score)
    
    # Ask if player wants to play again
    play_again = input("Play Again? (Y/N) ").upper()
    if play_again == "Y":
        return play_game(is_custom)
    else:
        return True

# Function to display the main menu
def display_menu():
    print("\n=========================")
    print("     HANGMAN MENU       ")
    print("=========================")
    print("(1) Play")
    print("(2) Play with Custom Words")
    print("(3) Add to Custom Words")
    print("(4) Exit")
    print("=========================")
    menu_choice = input("Enter your choice (1-4): ")
    return menu_choice

# Main function that runs the game
def main():
    print("Welcome to Hangman!")
    
    # Main program loop
    while True:
        menu_choice = display_menu()
        
        if menu_choice == "1":
            play_game(is_custom=False)  # Play with default words
        elif menu_choice == "2":
            result = play_game(is_custom=True)  # Play with custom words
            if not result:
                print("Returning to menu...")
        elif menu_choice == "3":
            add_custom_word()  # Add new custom words
        elif menu_choice == "4":
            print("Thank you for playing Hangman! Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

# Program entry point
if __name__ == "__main__":
    main()
import random
import time
import os
import sys
import pandas as pd
import socket
from datetime import datetime

# Simple English dictionary - keeping it simple as requested
DICTIONARY = [
    "cat", "dog", "car", "book", "house", "tree", "bird", "fish", "hand", "eye",
    "sun", "moon", "star", "water", "fire", "earth", "wind", "snow", "rain", "ice",
    "man", "woman", "child", "baby", "mom", "dad", "boy", "girl", "food", "milk",
    "bread", "cake", "apple", "egg", "meat", "rice", "tea", "box", "cup", "bag",
    "chair", "table", "bed", "door", "room", "wall", "floor", "roof", "key", "lock",
    "phone", "watch", "clock", "light", "lamp", "pen", "paper", "money", "coin", "bank",
    "shop", "store", "park", "road", "path", "beach", "hill", "lake", "river", "sea",
    "city", "town", "home", "work", "job", "boss", "team", "group", "party", "game",
    "toy", "ball", "bike", "boat", "plane", "train", "bus", "truck", "wheel", "seat",
    "hat", "shoe", "shirt", "coat", "dress", "pants", "sock", "belt", "ring", "watch"
]


def clear_console():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def colored_text(text, color):
    """Return colored text for console output"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"


def get_random_words(n):
    """Get n random words from dictionary"""
    return random.sample(DICTIONARY, n)


def full_display(words, question_delay):
    """Display all words at once for specified seconds"""
    print("Remember these words:")
    print("-" * 30)
    print(" ".join(words))
    print("-" * 30)
    time.sleep(question_delay)
    clear_console()


def sequential_display(words, question_delay):
    """Display words one at a time for specified seconds each"""
    print("Remember these words (one at a time):")
    for i, word in enumerate(words, 1):
        clear_console()
        print(f"Word {i}/{len(words)}:")
        print(f"\n{word}")
        time.sleep(question_delay)
    clear_console()


def quiz_ordered(correct_words):
    """Ordered quiz - sequence and order matter"""
    print("ORDERED QUIZ")
    print("Enter the words in the EXACT order they appeared, separated by spaces:")
    user_input = input("Your answer: ").strip().lower().split()

    correct_words_lower = [word.lower() for word in correct_words]

    print("\nComparison:")
    print("-" * 50)

    max_len = max(len(correct_words), len(user_input))

    for i in range(max_len):
        if i < len(correct_words):
            correct_word = correct_words_lower[i]
        else:
            correct_word = "(missing)"

        if i < len(user_input):
            user_word = user_input[i]
        else:
            user_word = "(missing)"

        if correct_word == user_word and i < len(correct_words):
            print(f"{i+1}. {colored_text(user_word, 'green')} ✓")
        else:
            print(f"{i+1}. {colored_text(user_word, 'red')
                            } (correct: {colored_text(correct_word, 'green')})")

    # Calculate score
    correct_count = sum(1 for i, word in enumerate(user_input)
                        if i < len(correct_words_lower) and word == correct_words_lower[i])
    score = correct_count / len(correct_words) * 100

    print(f"\nScore: {score:.1f}% ({correct_count}/{len(correct_words)})")

    return user_input, score


def quiz_unordered(correct_words):
    """Unordered quiz - only the words matter, not the order"""
    print("UNORDERED QUIZ")
    print("Enter all the words (order doesn't matter), separated by spaces:")
    user_input = input("Your answer: ").strip().lower().split()

    correct_words_lower = [word.lower() for word in correct_words]
    correct_set = set(correct_words_lower)
    user_set = set(user_input)

    print("\nComparison:")
    print("-" * 50)

    # Show correct words
    print("Words you got RIGHT:")
    correct_guesses = user_set.intersection(correct_set)
    if correct_guesses:
        for word in sorted(correct_guesses):
            print(f"  {colored_text(word, 'green')} ✓")
    else:
        print("  None")

    print("\nWords you MISSED:")
    missed_words = correct_set - user_set
    if missed_words:
        for word in sorted(missed_words):
            print(f"  {colored_text(word, 'red')} ✗")
    else:
        print("  None")

    print("\nWRONG words you entered:")
    wrong_words = user_set - correct_set
    if wrong_words:
        for word in sorted(wrong_words):
            print(f"  {colored_text(word, 'red')} ✗")
    else:
        print("  None")

    # Calculate score
    score = len(correct_guesses) / len(correct_words) * 100
    print(f"\nScore: {score:.1f}% ({
          len(correct_guesses)}/{len(correct_words)})")

    return user_input, score


def save_individual_quiz(quiz_record):
    """Save individual quiz data to a separate CSV file"""
    # Create DataFrame from single quiz record
    df = pd.DataFrame([quiz_record])
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Generate unique filename with timestamp
    # Include milliseconds for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
    hostname = socket.gethostname()
    filename = f"{dir_path}/data/{hostname}_quiz_{timestamp}.csv"

    directory = f"{dir_path}/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save to file
    df.to_csv(filename, index=False)
    print(f"Quiz data saved to: {filename}")


def generateMathQuestion() -> (str, int):
    # Question as first tuple answer, second is the answer
    operations = ['plus', 'minus', 'multiply']
    operation = random.choice(operations)

    if operation == 'plus':
        # 4 digits: 1000-9999
        num1 = random.randint(1000, 9999)
        num2 = random.randint(1000, 9999)
        answer = num1 + num2
        question = f"{num1} + {num2}"

    elif operation == 'minus':
        # 3 digits: 100-999
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        # Ensure positive result by making num1 >= num2
        if num1 < num2:
            num1, num2 = num2, num1
        answer = num1 - num2
        question = f"{num1} - {num2}"

    else:  # multiply
        # 2 digits: 10-99
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        answer = num1 * num2
        question = f"{num1} × {num2}"

    return (question, answer)


def doMath() -> (str, int):
    # The math questio and how many failed attempts
    question, correct_answer = generateMathQuestion()
    attempts = 0

    print(f"Solve this problem: {question}")

    while True:
        attempts += 1
        try:
            user_answer = int(input("Your answer: "))

            if user_answer == correct_answer:
                if attempts == 1:
                    print("Correct! Well done!")
                else:
                    print(f"Correct! You got it in {attempts} attempts.")
                return (question, attempts-1)
            else:
                print(f"Incorrect. Try again!")

        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


def main():
    """Main program loop"""
    isFirstTime = True
    display_choice = None
    quiz_choice = None
    question_delay = None
    mathBeforeAnswer = None
    amount = None
    while True:
        clear_console()
        if isFirstTime:
            print("=== WORD MEMORY GAME ===")
            print("\nDisplay Options:")
            print("1. Full display (show all words at once)")
            print("2. Sequential display (show words one at a time)")

            while True:
                try:
                    display_choice = int(
                        input("\nChoose display type (1 or 2): "))
                    if display_choice in [1, 2]:
                        break
                    else:
                        print("Please enter 1 or 2")
                except ValueError:
                    print("Please enter a valid number")

            print("\nQuiz Options:")
            print("1. Ordered quiz (order matters)")
            print("2. Unordered quiz (order doesn't matter)")

            while True:
                try:
                    quiz_choice = int(input("\nChoose quiz type (1 or 2): "))
                    if quiz_choice in [1, 2]:
                        break
                    else:
                        print("Please enter 1 or 2")
                except ValueError:
                    print("Please enter a valid number")

            print("\nSelect delay:")
            while True:
                try:
                    question_delay = float(input("\nDelay in seconds: "))
                    break
                except ValueError:
                    print("Please enter a valid number")

            print("\nSelect amount:")
            while True:
                try:
                    amount = int(input("\nWords to display: "))
                    break
                except ValueError:
                    print("Please enter a valid number")

            print("\nInclude math question?")
            while True:
                response = input(
                    "\nMath question before answer? (y/n) ").lower().strip()
                if response in ['y', 'yes']:
                    mathBeforeAnswer = True
                    break
                elif response in ['n', 'no']:
                    mathBeforeAnswer = False
                    break
                else:
                    print("Please select either y or n")

            print("\n30 sec delay?")
            while True:
                response = input(
                    "\nDelay before answer? (y/n) ").lower().strip()
                if response in ['y', 'yes']:
                    delayBeforeAnswer = True
                    break
                elif response in ['n', 'no']:
                    delayBeforeAnswer = False
                    break
                else:
                    print("Please select either y or n")

            print("\nletters only?")
            while True:
                response = input(
                    "\nuse letters instead of words? (y/n) ").lower().strip()
                if response in ['y', 'yes']:
                    global DICTIONARY
                    DICTIONARY = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                                  "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
                    lettersOnly = True
                    break
                elif response in ['n', 'no']:
                    lettersOnly = False
                    break
                else:
                    print("Please select either y or n")

            clear_console()
            print()
            print()
            print("Starting in 2 seconds...")
            time.sleep(2)
            isFirstTime = False

        # Get random words
        words = get_random_words(amount)

        # Record the start time
        session_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        clear_console()

        # Display words based on choice
        display_type = "full" if display_choice == 1 else "sequential"
        if display_choice == 1:
            full_display(words, question_delay)
        else:
            sequential_display(words, question_delay)

        if delayBeforeAnswer:
            timeoutLeft = 30
            while timeoutLeft > 0:
                print(f"Waiting... ({timeoutLeft}s left)")
                timeoutLeft -= 1
                time.sleep(1)

        if mathBeforeAnswer:
            math_question, failed_attempts = doMath()  # Sorry :(
            clear_console()

        # Run quiz based on choice
        quiz_type = "ordered" if quiz_choice == 1 else "unordered"
        if quiz_choice == 1:
            user_input, score = quiz_ordered(words)
        else:
            user_input, score = quiz_unordered(words)

        # Create quiz record
        quiz_record = {
            'timestamp': session_timestamp,
            'display_type': display_type,
            'quiz_type': quiz_type,
            'math_question': mathBeforeAnswer,
            'delay_seconds': question_delay,
            'num_words': amount,
            'generated_words': ' '.join(words),
            'user_input': ' '.join(user_input),
            'score_percentage': round(score, 1),
            'hostname': socket.gethostname(),
            'lettersOnly': lettersOnly
        }

        if mathBeforeAnswer:
            quiz_record["math_question"] = math_question
            quiz_record["failed_math_attempts"] = failed_attempts

        # Save this quiz immediately
        save_individual_quiz(quiz_record)

        # Ask if user wants to play again
        print("\n" + "="*50)
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y' and play_again != 'yes':
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()

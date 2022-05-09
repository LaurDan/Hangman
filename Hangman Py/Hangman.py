from os import system
from time import sleep
import random

gallow_list = []


def clear():
    _ = system('cls')


def game_progress(word_to_guess, actually_guessed_letters):
    current_progress = []

    for letter in word_to_guess:
        if str.lower(letter) in actually_guessed_letters:
            current_progress.append(letter)
        elif letter == " ":
            current_progress.append(" ")
        else:
            current_progress.append("_")
    return current_progress


def progress_display(actually_progress):
    return " ".join(actually_progress)


def user_letter_input():
    while True:
        user_letter = input("Please, provide a letter: ")
        if (user_letter.isalpha() and len(user_letter) == 1):
            return user_letter
        elif user_letter == "quit":
            return user_letter
        else:
            print("It's not a letter.")


def used_letters_display(used_letters_set):
    print(" ".join(used_letters_set))


def load_hangman_graphic():
    hangman_file = open("Hangman_graphic.txt", "r")
    file_content = hangman_file.read()
    hangman_file.close()
    return file_content


def list_hangman_string(hangman_string):
    return list(reversed(hangman_string.split(",")))


def load_words_string():
    hangman_words_file = open("countries-and-capitals.txt", "r")
    file_words_content = hangman_words_file.read()
    hangman_words_file.close()
    return file_words_content


def list_countries(words_string):
    countries_and_capitals = words_string.split("\n")
    return [element.split(" | ")[0] for element in countries_and_capitals]


def difficulty_setting(words_list):
    while True:
        difficulty_level = difficulty_picker()

        if difficulty_level == "0":
            return [word for word in words_list if len(word) < 5], 7
        elif difficulty_level == "1":
            return [word for word in words_list if (len(word) >= 5) and (len(word) < 7)], 6
        elif difficulty_level == "2":
            return [word for word in words_list if (len(word) >= 7) and (len(word) < 9)], 5
        elif difficulty_level == "3":
            return [word for word in words_list if (len(word) >= 9) and (len(word) < 12)], 4
        elif difficulty_level == "4":
            return [word for word in words_list if len(word) > 12], 3
        else:
            print("Incorrect input.")
            continue


def difficulty_picker():
    return input("""Choose one difficulty level:
    0 - very easy
    1 - easy
    2 - medium
    3 - hard
    4 - very hard
    Your pick: """)


def main_menu():
    word_list = list_countries(load_words_string())
    words_by_difficulty_list, lives = difficulty_setting(word_list)
    drawn_word = words_by_difficulty_list[random.randint(0, len(words_by_difficulty_list) - 1)]
    clear()
    play(drawn_word, lives)


def play(word, lives):
    word_to_guess = str.lower(word)
    amount_lives = lives
    guessed_letters_set = set()
    tried_letters_set = set()
    current_progress = game_progress(word, guessed_letters_set)
    gallow_list = list_hangman_string(load_hangman_graphic())

    while True:
        if amount_lives == 0:
            print(gallow_list[amount_lives])
            print(f"You loose! Answer word: {word}")
            break
        elif "".join(current_progress) == word:
            print(f"You win! Answer word: {word}")
            break

        print(gallow_list[amount_lives])
        print(progress_display(current_progress))
        print(f"Lives left: {amount_lives}")
        user_guess = str.lower(user_letter_input())

        if user_guess == "quit":
            print("Thank you for game!")
            break

        if (user_guess in guessed_letters_set) or (user_guess in tried_letters_set):
            print("This is repeated. Tried letters: ")
            used_letters_display(guessed_letters_set | tried_letters_set)
            sleep(3)
            clear()

        elif user_guess in word_to_guess:
            guessed_letters_set.add(user_guess)
            current_progress = game_progress(word, guessed_letters_set)
            print("Good shot!")
            sleep(1)
            clear()

        else:
            tried_letters_set.add(user_guess)
            amount_lives -= 1
            print("Wrong letter! Tried letters: ")
            used_letters_display(guessed_letters_set | tried_letters_set)
            sleep(1)
            clear()

if __name__ == "__main__":
    main_menu()
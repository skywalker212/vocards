"""Script to turn a list of words into flashcards supported by Anki"""
import sys
import argparse
import logging
import requests
from db import create_words_table, drop_words_table

""" function to print the helper info which helps in choosing the right option """
def get_user_input ():
    print("""
    Choose any of the below
    ----------------------------
    create: Create words table
    drop: Drop words table
    .exit: Exit the dungeon
    """)
    inp = input("$: ")
    return inp

""" function to evaluate and take action upon the input provided by user """
def evaluate_user_input (option):
    if "." in option:
        process_meta_command(option)
    else:
        execute_command(option)

""" function to process meta commands like exit.. """
def process_meta_command (command):
    command = command[1:]
    if command == "exit":
        print ("goodbye")
        sys.exit(0)
    else:
        print ("invalid meta command")

""" function to execute the general commands like insert and create """
def execute_command (command):
    if command == "create":
        create_words_table()
    elif command == "drop":
        drop_words_table()
    else:
        print("invalid operation")

""" function to setup the appropriate flags provided from command-line """
def parse_cla ():
    parser = argparse.ArgumentParser("A script to turn words into wisdom")
    parser.add_argument("--verbose", "-v", action="store_true", help="shows detailed information about what is going on", required=False)
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

def main ():
    print("welcome to the dungeon of words")
    while (True):
        option = get_user_input()
        evaluate_user_input(option)

if __name__ == '__main__':
    parse_cla()
    sys.exit(main())
"""Script to turn a list of words into flashcards supported by Anki"""
import sys
import argparse
import logging
import requests
from re import match
from db import create_words_table, drop_words_table, insert_words

""" function to print the helper info which helps in choosing the right option """
def get_user_input ():
    # if __verbose__:
    #     print("""
    #     Choose any of the below
    #     ----------------------------
    #     create: Create words table
    #     drop: Drop words table
    #     .exit: Exit the dungeon
    #     """)
    inp = input("$: ")
    return inp

""" function to evaluate and take action upon the input provided by user """
def evaluate_user_input (option):
    match_obj = match(r'^(\.?)(.*)$', option)
    if match_obj:
        is_meta = match_obj.group(1)
        actual_command = match_obj.group(2)
        if is_meta:
            process_meta_command(actual_command)
        else:
            execute_command(actual_command)

""" function to process meta commands like exit.. """
def process_meta_command (command):
    if command == "exit":
        print ("goodbye")
        sys.exit(0)
    else:
        print ("invalid meta command")

def execute_insert_input (arguments):
    if arguments:
        match_obj = match(r'^(.+\.txt)|(\d+)$', arguments)
        if match_obj:
            file_name = match_obj.group(1)
            word_count = match_obj.group(2)
            if file_name:
                try:
                    f = open(file_name, 'r')
                    word_list = f.read().split("\n")
                    insert_words(word_list)
                    f.close()
                except IOError as e:
                    print("Error while reading from file")
            else:
                insert_words([ word for word in [input(str(index+1)+": ") for index in range(int(word_count))]])
        else:
            print("pleae provide arguments in valid format")
    else:
        print("insert command requires additional arguments. Usage: insert [filename.txt|wordcount]")

""" function to execute the general commands like insert and create """
def execute_command (command):
    match_obj = match(r'^(create|drop|insert)( (.*))?$', command)
    if match_obj:
        actual_command = match_obj.group(1)
        additional_arguments = match_obj.group(3)
        if actual_command == "create":
            create_words_table()
        elif actual_command == "drop":
            drop_words_table()
        elif actual_command == "insert":
            execute_insert_input(additional_arguments)
    else:
        print("invalid operation")

""" function to setup the appropriate flags provided from command-line """
def parse_cla ():
    parser = argparse.ArgumentParser("A script to turn words into wisdom")
    parser.add_argument("--verbose", "-v", action="store_true", help="shows detailed information about what is going on", required=False)
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        __verbose__ = args.verbose

def main ():
    print("welcome to the dungeon of words")
    while (True):
        option = get_user_input()
        evaluate_user_input(option)

if __name__ == '__main__':
    parse_cla()
    sys.exit(main())
import pickle
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))


def ensure_number(new_number, repeat_text):
    is_number = False
    while not is_number:
        try:
            new_number = int(new_number)
            is_number = True
        except:
            print("You must enter a number...")
            new_number = input(repeat_text)
            continue
    return new_number


def save_to_database(filename, data):
    with open(current_directory + '\model_files\\'+filename+'.db', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_database(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)


def close_program():
    """
    Function for closing connection with database before exiting.
    """
    print("Closing program...")
    sys.exit()


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

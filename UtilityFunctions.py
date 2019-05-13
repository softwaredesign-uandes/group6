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


def get_reblock_params(limits):
    reblock_params = [None, None, None]
    reblock_axis = ["x", "y", "z"]
    axis_index = 0
    print("Leave blank to go back...")
    while None in reblock_params:
        message = "input the amount to reblock {} axis: ".format(reblock_axis[axis_index])
        param_value = input(message)
        if not param_value:
            return None
        param_value = ensure_number(param_value, message)
        if param_value <= 0:
            input("Invalid input: only can input a positive value...")
            continue
        if not (0 < param_value <= limits[axis_index]+1):
            input("Invalid input: max value to reblock in {} axis is {}".format(reblock_axis[axis_index],
                                                                                limits[axis_index]+1))
            continue
        reblock_params[axis_index] = param_value
        axis_index += 1
    return reblock_params


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

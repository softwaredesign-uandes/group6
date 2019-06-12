import pickle
import sys
import os
import glob
from Block import *

current_directory = os.path.dirname(os.path.abspath(__file__))


def save_to_api(filename, data):
    with open(current_directory + '\API\\'+filename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_from_api(filename):
    with open(current_directory + '\API\\'+filename, 'rb') as handle:
        return pickle.load(handle)


def read_mineral_deposit_block_models_ids(mineral_deposit="*"):
    os.chdir(current_directory + '\API\\')
    mineral_deposit_block_model_files = list(map(lambda file: file, glob.glob("*."+mineral_deposit)))
    if "mineral_deposits.mds" in mineral_deposit_block_model_files:
        mineral_deposit_block_model_files.remove("mineral_deposits.mds")
    mineral_deposit_block_model_ids = [int(x[:x.index(".")]) for x in mineral_deposit_block_model_files]
    return mineral_deposit_block_model_ids


def read_mineral_deposit_block_models_files(mineral_deposit="*"):
    os.chdir(current_directory + '\API\\')
    mineral_deposit_block_model_files = list(map(lambda file: file, glob.glob("*."+mineral_deposit)))
    mineral_deposit_block_model_files.remove("mineral_deposits.mds")
    return mineral_deposit_block_model_files


def parse_blocks(blocks_quantity, block_model_request):
    model_blocks = []
    for i in range(blocks_quantity):
        x_coordinate = block_model_request.json['block_model']['x_indices'][i]
        y_coordinate = block_model_request.json['block_model']['y_indices'][i]
        z_coordinate = block_model_request.json['block_model']['z_indices'][i]
        weight = block_model_request.json['block_model']['weights'][i]
        grades = {}
        for grade in block_model_request.json['block_model']['grades']:
            grades[grade] = {
                "value": block_model_request.json['block_model']['grades'][grade]['values'][i],
                "grade_type": block_model_request.json['block_model']['grades'][grade]['type']
            }
        new_block = Block("{},{},{}".format(x_coordinate, y_coordinate, z_coordinate),
                          x_coordinate, y_coordinate, z_coordinate, weight, grades)
        model_blocks.append(new_block)
    return model_blocks


def load_mineral_deposits():
    try:
        mineral_deposits = read_from_api("mineral_deposits.mds")
    except:
        mineral_deposits = {}
    return mineral_deposits


def check_response_contains_headers(request, request_object, headers):
    if request.data:
        if request_object not in request.json:
            return "Missing {}.".format(request_object)
        for header in headers:
            if header not in request.json[request_object]:
                return "Missing header {}.".format(header)
        return None
    else:
        return "Missing POST arguments."


def one_to_three_dimensions(block_id, borders):
    z = int(block_id / ((borders[0]+1) * (borders[1]+1)))
    block_id -= z * (borders[0]+1) * (borders[1]+1)
    y = int(block_id / (borders[0]+1))
    x = block_id - y * (borders[0]+1)
    return [x, y, z]


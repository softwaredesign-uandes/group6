from BlockModel import *
from Block import *
from MineralDeposit import *
from flask import Flask, request, abort, jsonify
from APIUtility import *
app = Flask(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))

"""
Mineral Deposits Routes.
"""


@app.route('/mineral_deposits', methods=['GET'])
def get_mineral_deposits():
    mineral_deposits_ids_and_names = []
    mineral_deposits = load_mineral_deposits()
    for mineral_deposit in mineral_deposits:
        mineral_deposits_ids_and_names.append({
            "id": mineral_deposit,
            "name": mineral_deposits[mineral_deposit].name
        })
    return jsonify({"mineral_deposits": mineral_deposits_ids_and_names})


@app.route('/mineral_deposits/<mineral_deposit_id>', methods=['GET'])
def get_mineral_deposit(mineral_deposit_id):
    try:
        mineral_deposit_id = int(mineral_deposit_id)
    except:
        return jsonify({'Error': "ID must be numerical."}), 400

    mineral_deposits = load_mineral_deposits()
    if mineral_deposit_id in mineral_deposits:
        mineral_deposit_block_models = read_mineral_deposit_block_models_ids(mineral_deposits[mineral_deposit_id].name)
        mineral_deposit_block_models_ids = []
        for mineral_deposit_block_model in mineral_deposit_block_models:
            mineral_deposit_block_models_ids.append({"id": mineral_deposit_block_model})
        return jsonify({"mineral_deposit": {
            "id": mineral_deposit_id,
            "name": mineral_deposits[mineral_deposit_id].name,
            "block_models": mineral_deposit_block_models_ids
        }})
    else:
        return jsonify({'Error': "ID not found"}), 404


@app.route('/mineral_deposits', methods=['POST'])
def post_mineral_deposit():

    answer = check_response_contains_headers(request, 'mineral_deposit', ['name'])
    if answer is not None:
        return jsonify({'Error': answer}), 400

    mineral_deposits = load_mineral_deposits()

    new_mineral_deposit_name = request.json['mineral_deposit']['name']
    for mineral_deposit in mineral_deposits:
        if new_mineral_deposit_name == mineral_deposits[mineral_deposit].name:
            return jsonify({'Error': "mineral deposit already exists on the database"}), 400
    new_mineral_deposit = MineralDeposit(new_mineral_deposit_name, 0, 0, 0, 0, {
        "new": {"mineral_column": 0,
                "grade_type": 0}
    })
    if len(mineral_deposits) == 0:
        mineral_deposits[0] = new_mineral_deposit
    else:
        mineral_deposit_biggest_id = max(mineral_deposits)
        mineral_deposits[mineral_deposit_biggest_id + 1] = new_mineral_deposit
    save_to_api("mineral_deposits.mds", mineral_deposits)
    return jsonify({'Success': "Ok."})


"""
Block Models Routes.
"""


@app.route('/block_models', methods=['GET'])
def get_block_models():
    block_model_ids = sorted(read_mineral_deposit_block_models_ids())
    block_model_ids_list = []
    for block_model_id in block_model_ids:
        block_model_ids_list.append({"id": block_model_id})
    return jsonify({'block_models': block_model_ids_list})


@app.route('/block_models/<block_model_id>', methods=['GET'])
def get_block_model(block_model_id):
    try:
        block_model_id = int(block_model_id)
    except:
        return jsonify({'Error': "ID must be numerical."}), 400
    block_model_files = read_mineral_deposit_block_models_files()
    block_model_ids = [int(x[:x.index(".")]) for x in block_model_files]
    if block_model_id in block_model_ids:
        block_model_file = block_model_files[block_model_ids.index(block_model_id)]
        block_model = read_from_api(block_model_file)
        return jsonify({"block_model": {
            "id": block_model_id,
            "total_weight": block_model.total_weight(),
            "num_blocks": block_model.count_blocks(),
            "air_blocks_percentage": block_model.air_blocks_percentage(),
            "mineral_weight": block_model.total_mineral_weight()
        }})
    else:
        return jsonify({'Error': "ID not found"}), 404


@app.route('/block_models', methods=['POST'])
def post_block_model():
    needed_block_model_headers = ["mineral_deposit_id", "name", "x_indices", "y_indices", "z_indices", "weights",
                                  "grades"]
    needed_reblock_model_headers = ["base_block_model_id", "reblock_x", "reblock_y", "reblock_z"]

    block_model_answer = check_response_contains_headers(request, 'block_model', needed_block_model_headers)
    reblock_model_answer = check_response_contains_headers(request, 'block_model', needed_reblock_model_headers)

    if (block_model_answer is not None) and (reblock_model_answer is not None):
        return jsonify({'Error': "block_model doesn't follow either allowed format."}), 400

    if not block_model_answer:
        mineral_deposits = load_mineral_deposits()

        if int(request.json['block_model']['mineral_deposit_id']) not in mineral_deposits:
            return jsonify({'Error': "mineral_deposit_id {} "
                                     "not found.".format(request.json['block_model']['mineral_deposit_id'])}), 404
        if len(request.json['block_model']['name']) == 0:
            return jsonify({'Error': "Name must not be empty"}), 400

        needed_block_headers = ["x_indices", "y_indices", "z_indices", "weights"]
        block_info_length = []
        for needed_block_header in needed_block_headers:
            length = len(request.json['block_model'][needed_block_header])
            block_info_length.append(length)
        for grade in request.json['block_model']['grades']:
            length = len(request.json['block_model']['grades'][grade]['values'])
            block_info_length.append(length)
        if "extras" in request.json['block_model']:
            for extra in request.json['block_model']["extras"]:
                length = len(request.json['block_model']["extras"][extra])
                block_info_length.append(length)

        if len(set(block_info_length)) > 1:
            return jsonify({'Error': "Block values must all be of same length"}), 400

        try:
            model_blocks = parse_blocks(block_info_length[0], request)
        except:
            return jsonify({'Error': "Block x,y,z, weight, grade values must be numeric"}), 400

        new_block_model = BlockModel(request.json['block_model']['name'],
                                     model_blocks,
                                     mineral_deposits[request.json['block_model']['mineral_deposit_id']].name)

        block_model_ids = read_mineral_deposit_block_models_ids()
        block_model_next_id = len(block_model_ids)

        save_to_api("{}.{}".format(block_model_next_id,
                                   mineral_deposits[request.json['block_model']['mineral_deposit_id']].name),
                    new_block_model)
    else:
        block_model_files = read_mineral_deposit_block_models_files()
        block_model_ids = [int(x[:x.index(".")]) for x in block_model_files]
        base_block_model_id = request.json['block_model']['base_block_model_id']
        if base_block_model_id not in block_model_ids:
            return jsonify({'Error': "ID not found"}), 404
        try:
            x_factor = int(request.json['block_model']['reblock_x'])
            y_factor = int(request.json['block_model']['reblock_y'])
            z_factor = int(request.json['block_model']['reblock_z'])
        except:
            return jsonify({'Error': "Reblock Factors must be numeric."}), 400

        if x_factor < 1 or y_factor< 1 or z_factor < 1:
            return jsonify({'Error': "Reblock Factors must equal or bigger than 1."}), 400

        base_block_model_file = block_model_files[block_model_ids.index(base_block_model_id)]
        base_block_model = read_from_api(base_block_model_file)
        base_block_model.reblock_model(x_factor, y_factor, z_factor, False)
        block_model_next_id = len(block_model_ids)
        save_to_api("{}.{}".format(block_model_next_id,
                                   base_block_model.mineral_deposit),
                    base_block_model)
    return jsonify({'Success': "Ok."})


@app.route('/block_models/<block_model_id>', methods=['PATCH'])
def update_block_model(block_model_id):
    try:
        block_model_id = int(block_model_id)
    except:
        return jsonify({'Error': "ID must be numerical."}), 400

    answer = check_response_contains_headers(request, 'block_model', ['edit_type', 'column_name'])
    if answer is not None:
        return jsonify({'Error': answer}), 400

    block_model_files = read_mineral_deposit_block_models_files()
    block_model_ids = [int(x[:x.index(".")]) for x in block_model_files]
    if block_model_id in block_model_ids:
        block_model_file = block_model_files[block_model_ids.index(block_model_id)]
        block_model = read_from_api(block_model_file)
        block_template = block_model.blocks[0]

        if request.json['block_model']['edit_type'] == "add":
            new_column_name = request.json['block_model']['column_name']
            if new_column_name in block_template.extras:
                return jsonify({'Error': "Block model already has a '{}' column.".format(new_column_name)}), 400
            else:
                if "values" not in request.json['block_model']:
                    return jsonify({'Error': "Request to add column is missing values"}), 400
                else:
                    if len(request.json['block_model']['values']) != block_model.count_blocks():
                        return jsonify({'Error': "To add a column, you need a values quantity equal to "
                                                 "the blocks quantity of the model"}), 400
                    else:
                        new_values = request.json['block_model']['values']
                        for block_index in range(len(block_model.blocks)):
                            block = block_model.blocks[block_index]
                            block.extras[new_column_name] = new_values[block_index]
        elif request.json['block_model']['edit_type'] == "remove":
            remove_column_name = request.json['block_model']['column_name']
            if remove_column_name not in block_template.extras:
                return jsonify({'Error': "Block model lacks a '{}' column.".format(remove_column_name)}), 400
            else:
                for block in block_model.blocks:
                    del block.extras[remove_column_name]
        else:
            return jsonify({'Error': "Unknown type of edition"}), 400
        save_to_api(block_model_file, block_model)
        return jsonify({'Success': "Update successful."})
    else:
        return jsonify({'Error': "ID not found"}), 404


"""
Block Routes.
"""


@app.route('/block_models/<block_model_id>/blocks/', methods=['GET'])
def get_block_model_blocks(block_model_id):
    try:
        block_model_id = int(block_model_id)
    except:
        return jsonify({'Error': "ID must be numerical."}), 400
    block_model_files = read_mineral_deposit_block_models_files()
    block_model_ids = [int(x[:x.index(".")]) for x in block_model_files]
    if block_model_id in block_model_ids:
        block_model_file = block_model_files[block_model_ids.index(block_model_id)]
        block_model = read_from_api(block_model_file)
        blocks = []
        block_model_borders = block_model.get_border_limits()
        for block in block_model.blocks:
            blocks.append({
                'block_id': three_to_one_dimensions(block.x_coordinate, block.y_coordinate, block.z_coordinate,
                                                    block_model_borders),
                'x_index': block.x_coordinate,
                'y_index': block.y_coordinate,
                'z_index': block.z_coordinate,
                'weight': block.weight,
                'grades': block.grades,
                'extras': block.extras
            })

        return jsonify({"blocks": blocks})
    else:
        return jsonify({'Error': "ID not found"}), 404


@app.route('/block_models/<block_model_id>/blocks/<block_id>', methods=['GET'])
def get_block_model_block(block_model_id, block_id):
    try:
        block_model_id = int(block_model_id)
        block_id = int(block_id)
    except:
        return jsonify({'Error': "IDs must be numerical."}), 400
    block_model_files = read_mineral_deposit_block_models_files()
    block_model_ids = [int(x[:x.index(".")]) for x in block_model_files]
    if block_model_id in block_model_ids:
        block_model_file = block_model_files[block_model_ids.index(block_model_id)]
        block_model = read_from_api(block_model_file)
        block_model_borders = block_model.get_border_limits()
        coordinates = one_to_three_dimensions(block_id, block_model_borders)
        query_blocks = list(filter(lambda block: block.id == "{},{},{}".format(coordinates[0], coordinates[1],
                                                                               coordinates[2]),
                                   block_model.blocks))
        if len(query_blocks) > 0:
            query_block = query_blocks[0]

            return jsonify({"block": {
                'x_index': query_block.x_coordinate,
                'y_index': query_block.y_coordinate,
                'z_index': query_block.z_coordinate,
                'weight': query_block.weight,
                'grades': query_block.grades,
                'extras': query_block.extras}
            })
        else:
            return jsonify({'Error': "Block ID not found"}), 404
    else:
        return jsonify({'Error': "Block Model ID not found"}), 404


@app.route('/block_models/<block_model_id>/blocks/<block_id>', methods=['PATCH'])
def update_block_model_block(block_model_id, block_id):
    try:
        block_model_id = int(block_model_id)
        block_id = int(block_id)
    except:
        return jsonify({'Error': "IDs must be numerical."}), 400

    if request.data:
        if "block" not in request.json:
            return jsonify({'Error': "Missing block parameter"}), 400
    else:
        return jsonify({'Error': "Missing PATCH arguments."}), 400

    block_model_files = read_mineral_deposit_block_models_files()
    block_model_ids = [int(x[:x.index(".")]) for x in block_model_files]
    if block_model_id in block_model_ids:
        block_model_file = block_model_files[block_model_ids.index(block_model_id)]
        block_model = read_from_api(block_model_file)
        block_model_borders = block_model.get_border_limits()
        coordinates = one_to_three_dimensions(block_id, block_model_borders)
        query_blocks = list(filter(lambda block: block.id == "{},{},{}".format(coordinates[0], coordinates[1],
                                                                               coordinates[2]),
                                   block_model.blocks))
        if len(query_blocks) > 0:
            query_block = query_blocks[0]
            if "weight" in request.json["block"]:
                try:
                    query_block.weight = float(request.json["block"]["weight"])
                except:
                    return jsonify({'Error': "Weight must be a number"}), 400
            if "grades" in request.json["block"]:
                for grade in request.json["block"]["grades"]:
                    if grade in query_block.grades:
                        try:
                            query_block.grades[grade]["value"] = float(request.json["block"]["grades"][grade])
                        except:
                            return jsonify({'Error': "{} must have a numerical value".format(grade)}), 400
                    else:
                        return jsonify({'Error': "Block doesn't have {} mineral grade.".format(grade)}), 400

            save_to_api(block_model_file, block_model)
            return jsonify({'Success': "Block {} successfully updated".format(block_id),
                            "block": {
                                'x_index': query_block.x_coordinate,
                                'y_index': query_block.y_coordinate,
                                'z_index': query_block.z_coordinate,
                                'weight': query_block.weight,
                                'grades': query_block.grades
                            }
                            })
        else:
            return jsonify({'Error': "Block ID not found"}), 404
    else:
        return jsonify({'Error': "Block Model ID not found"}), 404




if __name__ == '__main__':
    if not os.path.exists('API'):
        os.mkdir('API')
    app.run(host='0.0.0.0', port=80, debug=True)
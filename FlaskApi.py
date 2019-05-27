from BlockModel import *
from Block import *
from flask import Flask, request, abort, jsonify
app = Flask(__name__)


class ApiVariables:
    def __init__(self):
        self.block_model = None


api_variables = ApiVariables()


@app.route('/api/block_model/statistics', methods=['GET'])
def get_task():
    if api_variables.block_model:
        block_count = api_variables.block_model.count_blocks()
        total_weight = api_variables.block_model.total_weight()
        mineral_weight = api_variables.block_model.total_mineral_weight()
        air_percentage = api_variables.block_model.air_blocks_percentage()
        return jsonify({'block_count': block_count,
                        'total_weight': total_weight,
                        'mineral_weight': mineral_weight,
                        'air_percentage': air_percentage})
    else:
        return jsonify({'Error': "No Block Model."}), 404


@app.route('/api/block_model', methods=['POST'])
def load_block_model():
    needed_request_headers = ['blocks']
    if request.data:
        for needed_request_header in needed_request_headers:
            if needed_request_header not in request.json:
                return jsonify({'Error': "Request Missing Blocks."}), 400
    else:
        return jsonify({'Error': "No data."}), 400

    blocks = []
    for block in request.json['blocks']:
        x = block['x']
        y = block['y']
        z = block['z']
        new_block_id = str(x)+","+str(y)+","+str(z)
        weight = float(block['weight'])
        minerals = block['grades'].keys()
        mineral_grades = {}
        for mineral in minerals:
            mineral_grades[mineral] = {"value": float(block['grades'][mineral]['value']),
                                       "grade_type": block['grades'][mineral]['grade_type']}
        new_block = Block(new_block_id, x, y, z, weight, mineral_grades)
        blocks.append(new_block)

    block_model = BlockModel("Api_Block_Model", blocks, "Api_Block_Model")
    api_variables.block_model = block_model
    return jsonify({'Success': "Ok."})


@app.route('/api/block_model/reblock', methods=['POST'])
def reblock_loaded_block_model():
    needed_request_headers = ['x', 'y', 'z']
    if request.data:
        for needed_request_header in needed_request_headers:
            if needed_request_header not in request.json:
                return jsonify({'Error': "Request Missing Reblock Parameters."}), 400
    else:
        return jsonify({'Error': "No Reblock Parameters."}), 400

    x = request.json['x']
    y = request.json['y']
    z = request.json['z']

    try:
        api_variables.block_model.reblock_model(x, y, z, False)
    except:
        return jsonify({'Error': "Invalid reblock parameters."}), 400

    reblocked_blocks = []
    for block in api_variables.block_model.blocks:
        block_x_coordinate = block.x_coordinate
        block_y_coordinate = block.y_coordinate
        block_z_coordinate = block.z_coordinate
        block_weight = block.weight
        block_minerals = block.grades.keys()
        block_mineral_weights = {}
        for mineral in block_minerals:
            block_mineral_weights[mineral] = block.grades[mineral]['value']
        formatted_block = {
            'x': block_x_coordinate,
            'y': block_y_coordinate,
            'z': block_z_coordinate,
            'weight': block_weight,
            'mineral_weights': block_mineral_weights
        }
        reblocked_blocks.append(formatted_block)
    return jsonify(reblocked_blocks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
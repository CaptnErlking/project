from flask import Flask, jsonify, request, render_template
import os
import subprocess

app = Flask(__name__, template_folder='visualizer/templates')  # Explicitly set the template folder

# Absolute path to the static json folder where the sorting steps will be saved
JSON_FOLDER_PATH = os.path.abspath("sortVis/visualizer/static/json/sorting/")

# Ensure the directory for JSON files exists, create it if not
if not os.path.exists(JSON_FOLDER_PATH):
    os.makedirs(JSON_FOLDER_PATH)

@app.route('/')
def index():
    return render_template('visualizer/index.html')


@app.route('/generateSortingSteps/<algorithm>', methods=['GET'])
def generate_sorting_steps(algorithm):
    # Get the array size from the request
    size = int(request.args.get('size'))

    # Path to the corresponding C++ program for each algorithm
    cpp_file_map = {
        'bubble_sort': os.path.join(os.getcwd(), 'sortVis/visualizer/cpp/bubble_sort.cpp'),
        'insertion_sort': os.path.join(os.getcwd(), 'sortVis/visualizer/cpp/insertion_sort.cpp'),
        'selection_sort': os.path.join(os.getcwd(), 'sortVis/visualizer/cpp/selection_sort.cpp'),
        'merge_sort': os.path.join(os.getcwd(), 'sortVis/visualizer/cpp/merge_sort.cpp'),
        'quick_sort': os.path.join(os.getcwd(), 'sortVis/visualizer/cpp/quick_sort.cpp'),
    }

    # Make sure the algorithm exists
    if algorithm not in cpp_file_map:
        return jsonify({"error": "Invalid algorithm"}), 400

    cpp_file = cpp_file_map[algorithm]

    # Path for the output JSON file
    output_json_file = os.path.join(JSON_FOLDER_PATH, f"{algorithm}.json")

    try:
        # Compile the C++ code with g++ and run it
        compile_command = ["g++", cpp_file, "-o", "sortProgram", "-std=c++11"]
        subprocess.run(compile_command, check=True)

        # Run the C++ program with size as an argument and the output file path
        run_command = ["./sortProgram", str(size), output_json_file]
        subprocess.run(run_command, check=True)

        # Optionally remove the compiled C++ program after running
        os.remove("sortProgram")

        # Return the path to the generated JSON file
        return jsonify({"jsonFile": f"/static/json/sorting/{algorithm}.json"})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Error while running the sorting algorithm: {str(e)}"}), 500
    except FileNotFoundError as e:
        return jsonify({"error": f"File not found: {str(e)}"}), 404


if __name__ == '__main__':
    app.run(debug=True)

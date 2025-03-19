from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Container 2 URL using Kubernetes service name
CONTAINER_2_URL = "http://container2-service:7000/calculate"

@app.route('/store-file', methods=['POST'])
def store_file():
    print('test_trigger')
    data = request.get_json()
    if not data or 'file' not in data or 'data' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    filename = data['file']
    file_data = data['data']
    file_path = os.path.join('/ritvik_PV_dir', filename)

    try:
        with open(file_path, 'w') as f:
            f.write(file_data)
        return jsonify({"file": filename, "message": "Success."})
    except Exception as e:
        return jsonify({"file": filename, "error": "Error while storing the file to the storage."}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    filename = data['file']
    product = data.get('product')
    full_path = os.path.join('/ritvik_PV_dir', filename)

    try:
        response = requests.post(CONTAINER_2_URL, json={"file": full_path, "product": product})
        return jsonify(response.json())
    except requests.exceptions.RequestException:
        return jsonify({"error": "Failed to communicate with Container 2."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
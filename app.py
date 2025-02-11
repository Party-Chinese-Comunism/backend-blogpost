from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_data():
    data = {"message": "TESte get"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
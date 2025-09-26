from flask import Flask, jsonify
from workflow import run_workflow

app = Flask(__name__)

@app.route("/run", methods=["GET"])
def run():
    new_records, total_records = run_workflow()
    return jsonify({
        "status": "ok",
        "new_records": new_records,
        "total_records": total_records
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
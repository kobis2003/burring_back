from flask import abort, request

import config
from owkin.blurring.process import blurr
from owkin.models.run import burning_run_schema
from owkin.repository.runs import read_one

app = config.connex_app


@app.route('/run/<run_id>', methods=['GET'])
def get_one(run_id: int):
    run = read_one(run_id)
    if run is not None:
        return burning_run_schema.dump(run)
    else:
        abort(404, f"Run with {run_id} not found")


@app.route('/run/burring_process', methods=['POST'])
def launch_burring_process():
    try:
        run = blurr(request.json)
        return burning_run_schema.dump(run), 200
    except ValueError as e:
        abort(400, str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9660, debug=True)

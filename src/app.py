from flask import abort, request
from flask_cors import CORS

import config
from owkin.blurring.process import blurr
from owkin.models.run import burning_run_schema, BlurringRun
from owkin.repository.runs import read_one

app = config.connex_app
CORS(app.app)


@app.route("/run/<run_id>", methods=["GET"])
def get_one(run_id: int):
    """
    Called every 500ms to update the progress bar and to get the result of the blurring process
    :param run_id: The id of the run
    :return: The corresponding entity (useful for result, nb of completed process or error_message)
    """
    run = read_one(run_id)
    if run is not None:
        return burning_run_schema.dump(run)
    else:
        abort(404, f"Run with {run_id} not found")


@app.route("/run/burring_process", methods=["POST"])
def launch_burring_process():
    """
    Launch the burring process corresponding to the JSON in the body
    :return: The newly created entity (useful for the id and the nb of total process)
    """
    try:
        run = blurr(request.json)
        return burning_run_schema.dump(run), 200
    except ValueError as e:
        abort(400, str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9660, debug=True)

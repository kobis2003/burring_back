import json
import time

from PIL import ImageFilter

from blurring.test_json_reader import TEST_DIRECTORY
from config import app
from owkin.blurring.process import __get_filter_class, blurr
from owkin.models.input import Filter
from owkin.repository.runs import read_one, Status


def test_get_filter_class():
    result_class = __get_filter_class(Filter("BLUR", None))
    assert result_class == ImageFilter.BLUR


def test_get_filter_class_with_params():
    result_class = __get_filter_class(Filter("BoxBlur", {"radius": 4}))
    assert isinstance(result_class, ImageFilter.BoxBlur)
    assert result_class.radius == 4


def test_full_blurring_regular_case():
    with app.app_context():
        with open(f"{TEST_DIRECTORY}/input/input-lenna-bee.json") as json_file:
            result = blurr(json.load(json_file))

        assert result.status == Status.RUNNING.name
        assert result.nb_of_completed_process == 0
        assert result.nb_of_total_process == 33
        should_continue = True
        count = 0
        while should_continue:
            current_run = read_one(result.id)
            if (
                current_run.status == Status.FAILED.name
                or current_run.status == Status.SUCCESS.name
            ):
                should_continue = False
            current_progress = current_run.nb_of_completed_process
            print(f"current_progress => {current_progress} ")
            count = count + 1
            time.sleep(1)
        print(f" count => {count}")
        assert current_run.status == Status.SUCCESS.name
        assert current_run.result is not None
        assert current_run.nb_of_completed_process == 33

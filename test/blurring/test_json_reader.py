import json
import os

from owkin.blurring.process import __parse_blurring_input

TEST_DIRECTORY = os.environ.get("TEST_DIRECTORY", ".")


def test_regular_case():
    with open(f"{TEST_DIRECTORY}/input/input-lenna-bee.json") as json_file:
        input_dict = json.loads(json_file.read())
    result = __parse_blurring_input(input_dict, 41)
    assert len(result.images) == 2
    print(result.images[0])
    assert result.images[0].name == "Lenna"
    assert len(result.filters) == 2
    assert result.filters[0].name == "BLUR"
    assert result.filters[1].params["radius"] == 4

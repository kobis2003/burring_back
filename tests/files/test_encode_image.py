import base64
import os

TEST_DIRECTORY = os.environ.get("TEST_DIRECTORY", ".")


def test_encode_image():
    """
    Use only to get test image to put in the JSON
    """
    image_name = "voiture_image"
    image_file_name = f"{image_name}.png"
    image_file_txt = f"{image_name}.txt"
    image_path = f"{TEST_DIRECTORY}/files/{image_file_name}"
    with open(image_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    with open(f"{TEST_DIRECTORY}/files/{image_file_txt}", "w") as file:
        file.write(data.decode("utf-8"))

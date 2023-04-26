from typing import List

from owkin.models.input import BlurringImage, Filter


class ImageResult:
    def __init__(self, image_result: BlurringImage, image_filter: Filter):
        self.result_image = image_result
        self.image_filter = image_filter


class Output:
    def __init__(
        self, image_results: List[ImageResult], initial_images: List[BlurringImage]
    ):
        self.result_images = image_results
        self.initial_images = initial_images

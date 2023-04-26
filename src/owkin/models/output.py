from typing import List

from owkin.models.input import BlurringImage, Filter


class ImageResult:
    def __init__(self, image_result: BlurringImage, image_filter: Filter):
        self.image_result = image_result
        self.image_filter = image_filter

    def to_dict(self):
        return {
            "image_result": self.image_result.__dict__,
            "image_filter": self.image_filter.__dict__,
        }


class Output:
    def __init__(
        self, image_results: List[ImageResult], initial_images: List[BlurringImage]
    ):
        self.result_images = image_results
        self.initial_images = initial_images

    def to_dict(self):
        image_results_in_dict = []
        initial_images_in_dict = []
        for result_image in self.result_images:
            image_results_in_dict.append(result_image.to_dict())
        for initial_image in self.initial_images:
            initial_images_in_dict.append(initial_image.__dict__)
        return {
            "image_results": image_results_in_dict,
            "initial_images": initial_images_in_dict,
        }

"""
Entities of the input of the blurring process
"""

from typing import List, Optional


class Filter:
    def __init__(self, name: str, params: Optional[dict] = None):
        self.name = name
        self.params = params


class BlurringImage:
    def __init__(self, name: str, data: str):
        self.name = name
        self.data = data


class Input:
    def __init__(self, filters: List[dict], images: List[dict]):
        _images_in_obj = []
        _filters_in_obj = []
        for f in filters:
            _filters_in_obj.append(Filter(**f))
        for i in images:
            _images_in_obj.append(BlurringImage(**i))
        self.filters = _filters_in_obj
        self.images = _images_in_obj

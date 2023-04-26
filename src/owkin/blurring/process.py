import base64
import inspect
import json
import time
from enum import Enum
from io import BytesIO
from multiprocessing import Process, Queue

from PIL import ImageFilter, Image

from config import app
from owkin.models.input import Input, Filter, BlurringImage
from owkin.models.output import ImageResult, Output
from owkin.models.run import BlurringRun
from owkin.repository.runs import (
    progress,
    finish,
    failure,
    create_new_run,
    change_total_nb_of_process,
    count_running_process,
)


class ProcessError(Exception):
    pass


class FilterNames(Enum):
    BLUR = ImageFilter.BLUR.name
    GREEN = 2
    BLUE = 3


def blurr(json_content: dict) -> BlurringRun:
    run = create_new_run()
    blurring_input = __parse_blurring_input(json_content, run.id)
    run = change_total_nb_of_process(run.id, __get_total_nb_of_process(blurring_input))
    queue = Queue()
    p = Process(target=__process_blurring, args=(blurring_input, run.id))
    time_spent_waiting = 0
    # before starting the process, we make sure that the number of CPU is enough
    while count_running_process() > 5:
        time.sleep(1)
        time_spent_waiting = time_spent_waiting + 1
        # limit at 20 minutes
        if time_spent_waiting > 20 * 60:
            raise TimeoutError("The CPU are to busy!")
    # I used Thread. In Prod context, I would have try to launch one AWS batch job
    # for each image if possible (letting AWS deal with the thread problem). If not AWS
    # specific service can be used, I would probably try to find the equivalent application
    # in it's kubernete version
    p.start()
    return run


def __get_total_nb_of_process(blurring_input: Input) -> int:
    return len(blurring_input.images) * len(blurring_input.filters)


def __parse_blurring_input(input_content: dict, run_id: int) -> Input:
    """
    used to parse the JSON content into an object
    :param input_content: The content of the JSON
    :return: The input object corresponding
    """
    try:
        input_obj = Input(**input_content)
        return input_obj
    except:
        error_message = "Error when parsing the JSON"
        failure(run_id, error_message)
        raise ValueError(error_message)


def __process_blurring(blurring_input: Input, run_id: int) -> Output:
    image_results = []
    images = []
    try:
        for image in blurring_input.images:
            images.append(image)
            for blurring_filter in blurring_input.filters:
                result_data = __process_blurring_for_image(image, blurring_filter)
                image_result = ImageResult(
                    BlurringImage(image.name, result_data), blurring_filter
                )
                image_results.append(image_result)
                progress(run_id)
        result = Output(image_results, images)
        finish(run_id, str(Output(image_results, images).to_dict()))
    except ValueError as e:
        failure(run_id, str(e))
        raise ProcessError(str(e))
    except Exception as e:
        print(f"Exception => {str(e)} ")
        error_message = f"error at the image: {image.name} with the filter: {str(blurring_filter.__dict__)} "
        failure(run_id, error_message)
        raise ProcessError(error_message)
    return result


def __process_blurring_for_image(image: BlurringImage, blurring_filter: Filter) -> str:
    to_process_image = Image.open(BytesIO(base64.b64decode(image.data)))
    # we get all the classes of the image filter file:
    filter_class = __get_filter_class(blurring_filter)
    blurred_image = to_process_image.filter(filter_class)
    buffered = BytesIO()
    blurred_image.save(buffered, format="PNG")
    return (base64.b64encode(buffered.getvalue())).decode("utf-8")


def __get_filter_class(blurring_filter: Filter) -> any:
    class_members = inspect.getmembers(ImageFilter, inspect.isclass)
    for filter_class_name in class_members:
        if filter_class_name[0] == blurring_filter.name:
            if blurring_filter.params is not None:
                return filter_class_name[1](**blurring_filter.params)
            else:
                return filter_class_name[1]
    raise ValueError(
        f"No filter with this name:{blurring_filter.name} exists in the ImageFilter class"
    )

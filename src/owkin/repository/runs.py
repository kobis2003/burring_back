"""
module where all the action to the DB are described
"""
from datetime import datetime
from enum import Enum, auto

from config import db
from owkin.models.run import BlurringRun, burning_run_schema


class Status(Enum):
    RUNNING = auto()
    FAILED = auto()
    SUCCESS = auto()


class RecordNotFoundException(Exception):
    pass


def create_new_run() -> BlurringRun:
    """
    create a new run in the DB
    :return: The BlurringRun newly created (usefull especially for it's id)
    """
    new_run = burning_run_schema.load(
        BlurringRun(Status.RUNNING.name, 0, 0).to_dict(), session=db.session
    )
    db.session.add(new_run)
    db.session.commit()
    return BlurringRun(**burning_run_schema.dump(new_run))


def read_one(run_id: int) -> BlurringRun:
    """
        read one entity
    :param run_id: the id of the run we want to get
    :return: the BlurringRun entity corresponding (throw RecordNotFoundException if doesn't exist)
    """
    existing_run = BlurringRun.query.filter(BlurringRun.id == run_id).one_or_none()
    if existing_run:
        # TODO: find a better way to handle it
        db.session.refresh(existing_run)
        return existing_run
    raise RecordNotFoundException(f"no corresponding run: {run_id}")


def change_total_nb_of_process(run_id: int, nb_of_total_process: int) -> BlurringRun:
    """
        update the nb_of_total_process of the run in the DB
    :param run_id:  id of the run
    :param nb_of_total_process: should correspond to nb of image * nb of filter
    :return: the update entity
    """
    run = read_one(run_id)
    if run:
        run.nb_of_total_process = nb_of_total_process
        return __merge_run(run)
    raise RecordNotFoundException(f"no corresponding run: {run_id}")


def progress(run_id: int) -> BlurringRun:
    """
    increment the nb_of_completed_process of the entity
    :param run_id: the id of the run
    :return: The updated BlurringRun
    """
    run = read_one(run_id)
    if run:
        run.nb_of_completed_process = run.nb_of_completed_process + 1
        return __merge_run(run)
    else:
        raise RecordNotFoundException(f"no corresponding run: {run_id}")


def count_running_process() -> int:
    return BlurringRun.query.filter(BlurringRun.status == Status.RUNNING.name).count()


def failure(run_id: int, error_message: str) -> BlurringRun:
    run = read_one(run_id)
    if run:
        run.error_message = error_message
        run.status = Status.FAILED.name
        return __merge_run(run)
    raise RecordNotFoundException(f"no corresponding run: {run_id}")


def finish(run_id: int, result: str) -> BlurringRun:
    run = read_one(run_id)
    if run:
        run.result = result
        run.status = Status.SUCCESS.name
        return __merge_run(run)
    raise RecordNotFoundException(f"no corresponding run: {run_id}")


def __merge_run(run: BlurringRun) -> BlurringRun:
    run.updated_timestamp = datetime.now()
    db.session.merge(run)
    db.session.commit()
    return run

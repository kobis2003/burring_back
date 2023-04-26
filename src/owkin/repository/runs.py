from datetime import datetime
from enum import Enum, auto

from flask import session

from owkin.models.run import BlurringRun, burning_run_schema
from config import db


class Status(Enum):
    RUNNING = auto()
    FAILED = auto()
    SUCCESS = auto()


class RecordNotFoundException(Exception):
    pass


def create_new_run() -> BlurringRun:
    new_run = burning_run_schema.load(
        BlurringRun(Status.RUNNING.name, 0, 0).to_dict(), session=db.session
    )
    db.session.add(new_run)
    db.session.commit()
    return BlurringRun(**burning_run_schema.dump(new_run))


def read_one(run_id: int) -> BlurringRun:
    existing_run = BlurringRun.query.filter(BlurringRun.id == run_id).one_or_none()
    if existing_run:
        # TODO: find a better way to handle it
        db.session.refresh(existing_run)
        return existing_run
    else:
        raise RecordNotFoundException(f"no corresponding run: {run_id}")


def change_total_nb_of_process(run_id: int, nb_of_total_process: int) -> BlurringRun:
    run = read_one(run_id)
    if run:
        run.nb_of_total_process = nb_of_total_process
        return __merge_run(run)
    else:
        raise RecordNotFoundException(f"no corresponding run: {run_id}")


def progress(run_id: int) -> BlurringRun:
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
    else:
        raise RecordNotFoundException(f"no corresponding run: {run_id}")


def finish(run_id: int, result: str) -> BlurringRun:
    run = read_one(run_id)
    if run:
        run.result = result
        run.status = Status.SUCCESS.name
        return __merge_run(run)
    else:
        raise RecordNotFoundException(f"no corresponding run: {run_id}")


def __merge_run(run: BlurringRun) -> BlurringRun:
    run.updated_timestamp = datetime.now()
    db.session.merge(run)
    db.session.commit()
    return run

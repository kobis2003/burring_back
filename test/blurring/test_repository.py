from config import app
from owkin.repository.runs import (
    read_one,
    Status,
    progress,
    finish,
    failure,
    create_new_run,
    change_total_nb_of_process,
)


def test_run_creation_and_reading():
    with app.app_context():
        new_run = create_new_run()
        change_total_nb_of_process(new_run.id, 15)
        compare_run_start = read_one(new_run.id)
        assert compare_run_start.created_timestamp is not None
        assert compare_run_start.updated_timestamp is not None
        assert compare_run_start.status == Status.RUNNING.name
        assert compare_run_start.nb_of_completed_process == 0
        assert compare_run_start.nb_of_total_process == 15
        old_updated_timestamp = compare_run_start.updated_timestamp
        progress(new_run.id)
        compare_run_after_progress = read_one(new_run.id)
        assert compare_run_after_progress.nb_of_completed_process == 1
        assert (
            compare_run_after_progress.updated_timestamp.timestamp()
            > old_updated_timestamp.timestamp()
        )
        test_result = "the test result"
        finish(new_run.id, test_result)
        compare_run_after_finish = read_one(new_run.id)
        assert compare_run_after_finish.result == test_result
        assert compare_run_after_finish.status == Status.SUCCESS.name


def test_failure_case():
    with app.app_context():
        new_run = create_new_run()
        test_error_message = "something went wrong..."
        failure(new_run.id, test_error_message)
        compare_run_after_failure = read_one(new_run.id)
        assert compare_run_after_failure.error_message == test_error_message
        assert compare_run_after_failure.status == Status.FAILED.name

from datetime import datetime
from typing import Optional

from config import db, ma


class BlurringRun(db.Model):
    __tablename__ = "blurring_run"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    result = db.Column(db.Text)
    error_message = db.Column(db.Text)
    nb_of_completed_process = db.Column(db.Integer, nullable=False)
    nb_of_total_process = db.Column(db.Integer, nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(
        self,
        status: str,
        nb_of_completed_process: int,
        nb_of_total_process: int,
        id: Optional[int] = None,
        result: Optional[str] = None,
        error_message: Optional[str] = None,
        created_timestamp: Optional[datetime] = None,
        updated_timestamp: Optional[datetime] = None,
    ):
        self.status = status
        self.nb_of_completed_process = nb_of_completed_process
        self.nb_of_total_process = nb_of_total_process
        self.created_timestamp = created_timestamp
        self.updated_timestamp = updated_timestamp
        self.result = result
        self.error_message = error_message
        self.id = id

    def to_dict(self) -> dict:
        """
        in order to be able to insert, we need the dict of the object without the id field
        :return:
        """
        return {
            "status": self.status,
            "result": self.result,
            "error_message": self.error_message,
            "nb_of_completed_process": self.nb_of_completed_process,
            "nb_of_total_process": self.nb_of_total_process,
        }


class BlurringRunSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlurringRun
        load_instance = True
        sqla_session = db.session


burning_run_schema = BlurringRunSchema()

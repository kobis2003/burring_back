import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

basedir = pathlib.Path(__file__).parent.parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)


app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'blurring.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class SQLiteAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        options.update(
            {
                "isolation_level": "READ COMMITTED",
            }
        )
        super(SQLiteAlchemy, self).apply_driver_hacks(app, info, options)


db = SQLiteAlchemy(app)
ma = Marshmallow(app)

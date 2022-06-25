from datetime import datetime
import json
from operator import and_, or_
from ..model.register import RegisterModel
from api import db


def get_register_data(dev1, dev2):

    register_records = RegisterModel.query.where(
        or_(
            and_(RegisterModel.dev1 == dev1, RegisterModel.dev2 == dev2),
            and_(RegisterModel.dev1 == dev2, RegisterModel.dev2 == dev1),
        )
    ).all()
    register_records = [row.register_data for row in register_records]
    print(register_records)

    return [json.loads(record) for record in register_records]


def save_register_data(dev1, dev2, register_data):
    register_data = add_register_at(register_data)

    register_data = json.dumps(register_data)
    register_instance = RegisterModel(dev1=dev1, dev2=dev2, register_data=register_data)
    db.session.add(register_instance)
    db.session.commit()

    print(f"Successfully saved data for {dev1} and {dev2}")


def add_register_at(register_data):
    register_data_result = {
        "registered_at": datetime.utcnow().strftime("%Y-%m-%dT:%H:%M:%SZ")
    }

    register_data_result.update(register_data)

    return register_data_result

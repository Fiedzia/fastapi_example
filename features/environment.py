from fastapi.testclient import TestClient

from app import get_db, app

import models


def before_scenario(context, scenario):
    """
    clean up database before each scenario
    """
    context.client = TestClient(app)

    db = [v for v in get_db()][0]
    db.query(models.UserAddressMapping).delete()
    db.query(models.User).delete()
    db.query(models.Address).delete()
    db.query(models.Account).delete()
    db.commit()
    context.db = db

import json

from behave import *

import models


#@given('database state')
#def step_impl(context):
#    get data from context.table
#    pass


@given("existing user '{json_data}'")
def step_impl(context):
    data = json.loads(json_data)
    pass


@given("existing account '{json_data}'")
def step_impl(context):
    pass


@given("existing address '{json_data}'")
def step_impl(context):
    pass


@given("existing user_address_mapping '{json_data}'")
def step_impl(context):
    pass


@when("we create user '{json_data}'")
def step_impl(context, json_data):
    response = context.client.post('/user/', json=json.loads(json_data))
    context.response = response


@when("we create user account '{json_data}' for user_id {user_id}")
def step_impl(context, json_data, user_id):
    response = context.client.post(f'/user/{user_id}/account/', json=json.loads(json_data))
    context.response = response


@when("we create user address '{json_data}' for user_id {user_id}")
def step_impl(context, json_data, user_id):
    response = context.client.post(f'/user/{user_id}/address/', json=json.loads(json_data))
    context.response = response


@when('we assign address {address_id} to user_id {user_id}')
def step_impl(context, address_id, user_id):
    response = context.client.post(f'/user/{user_id}/assign_address/{address_id}/')
    context.response = response


@then("response.content is '{json_data}'")
def step_impl(context, json_data):
    assert json.loads(json_data) == context.response.json()


@then("response.status is {status_code}")
def step_impl(context, status_code):
    assert context.response.status_code == status_code


@then("user exists '{json_data}'")
def step_impl(context, json_data):
    data = json.loads(json_data)
    conditions = [getattr(models.User, k) == v for k, v in data.items()]
    results = context.db.query(models.User).filter(*conditions).all()
    assert len(results) > 0


@then("account exists '{json_data}'")
def step_impl(context, json_data):
    data = json.loads(json_data)
    conditions = [getattr(models.Account, k) == v for k, v in data.items()]
    results = context.db.query(models.Account).filter(*conditions).all()
    assert len(results) > 0


@then("address exists '{json_data}'")
def step_impl(context, json_data):
    data = json.loads(json_data)
    conditions = [getattr(models.Address, k) == v for k, v in data.items()]
    results = context.db.query(models.Address).filter(*conditions).all()
    assert len(results) > 0


@then("address exists '{json_data}' for user_id {user_id}")
def step_impl(context, json_data, user_id):
    data = json.loads(json_data)
    conditions = [getattr(models.Address, k) == v for k, v in data.items()]
    addresses = context.db.query(models.Address).filter(*conditions).all()
    assert len(addresses) > 0
    results = (context.db.query(models.UserAddressMapping)
        .filter(
            models.UserAddressMapping.user_id == user_id,
            models.UserAddressMapping.address_id == addresses[0].id
        ).all())
    assert len(results) > 0

@then("address {address_id} is assigned to user_id {user_id}")
def step_impl(context, address_id, user_id):
    mappings = (context.db.query(models.UserAddressMapping)
        .filter(
            models.UserAddressMapping.user_id == user_id,
            models.UserAddressMapping.address_id == address_id,
        ).all())
    assert len(mappings) > 0


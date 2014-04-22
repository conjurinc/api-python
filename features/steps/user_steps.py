from behave import *
import conjur

@when("I create a user")
def step_impl(context):
    context.user_id = context.random_string('api-python-user')
    context.user = context.api.create_user(context.user_id)

@then("I can login as the user using the api key")
def step_impl(context):
    user_api = context.user_api = conjur.new_from_key(context.user_id, context.user.api_key)
    user_api.authenticate(False)

@when(u'I create a user with a password')
def step_impl(context):
    context.user_id = context.random_string("api-python-user")
    context.password = context.random_string('pass', 30)
    context.user = context.api.create_user(context.user_id, context.password)

@then(u'I can login as the user using the password')
def step_impl(context):
    user_api = conjur.new_from_key(context.user_id, context.password)
    user_api.authenticate(False)
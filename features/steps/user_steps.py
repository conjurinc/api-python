from behave import when, then
import conjur


@when("I create a user")
def step_create_user(context):
    context.user_id = context.random_string('api-python-user')
    context.user = context.api.create_user(context.user_id)


@when('I create a user "{name}"')
def step_creaet_user_named(context, name):
    context.user_id = context.random_string(name)
    context.user = context.api.create_user(context.user_id)


@then("I can login as the user using the api key")
def step_login_as_user(context):
    user_api = context.user_api = conjur.new_from_key(
        context.user_id, context.user.api_key, context.api.config)
    user_api.authenticate(False)


@when(u'I create a user with a password')
def step_create_user_with_password(context):
    context.user_id = context.random_string("api-python-user")
    context.password = context.random_string('pass', 30)
    context.user = context.api.create_user(context.user_id, context.password)


@then(u'I can login as the user using the password')
def step_login_as_user_with_password(context):
    user_api = conjur.new_from_key(context.user_id, context.password,
                                   context.api.config)
    user_api.authenticate(False)

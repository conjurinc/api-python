from behave import *


@when("I create a variable")
def step_impl(context):
    context.variable = context.api.create_variable()


@when('I add a value "{value}"')
def step_impl(context, value):
    context.variable.add_value(value)


@then('the variable should have attribute "{attr}" with value {value}')
def step_impl(context, attr, value):
    actual = getattr(context.variable, attr)
    print(repr(actual))
    assert str(actual) == value


@then('the variable should have value "{value}"')
def step_impl(context, value):
    assert value == context.variable.value()

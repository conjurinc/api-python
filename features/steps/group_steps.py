from behave import *


@when('I create a group "{name}"')
def create_group_impl(context, name):
    name = context.random_string(name)
    context.group = context.api.create_group(name)


@when('I try to create a group "{name}"')
def try_create_group_impl(context, name):
    name = context.random_string(name)
    context.create_group_failed = False
    try:
        context.group = context.api.create_group(name)
    except Exception, e:
        context.create_group_failed = e


@then('it succeeds')
def it_succeeds_impl(context):
    if context.create_group_failed:
        err = context.create_group_failed
        context.create_group_failed = False
        assert not err

@then('I can list the group members')
def list_members_impl(context):
    context.group_members = context.group.members()

@when('I add the member to the group')
def add_member_impl(context):
    context.group.add_member(context.user.role)


from behave import when, then


@when(u'I list members of "{kind}:{name}"')
def list_members_impl(context, kind, name):
    context.group = context.api.role(kind, name)
    context.group_members = context.group.members()

@then(u'"{id}" is a member')
def is_group_member(context, id):
    print(context.group_members)
    assert id in (x['member'] for x in context.group_members)

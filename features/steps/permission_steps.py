from behave import when,then


def check_permission_impl(api, role, privilege, resource, can):
    role = api.role(*role.split(':'))
    resource = api.resource(*resource.split(':'))
    assert resource.permitted(privilege, role) == can


def check_permission_current_impl(api, privilege, resource, can):
    resource = api.resource(*resource.split(':'))
    assert resource.permitted(privilege) == can



@then('"{role}" can "{privilege}" "{resource}"')
def role_can_resource(context, role, privilege, resource):
    check_permission_impl(context.api, role, privilege, resource, True)


@then('"{role}" can not "{privilege}" "{resource}"')
def role_cannot_resource(context, role, privilege, resource):
    check_permission_impl(context.api, role, privilege, resource, False)


@then('the current role can "{privilege}" "{resource}"')
def current_role_can(context, privilege, resource):
    check_permission_current_impl(context.api, privilege, resource, True)


@then('the current role can not "{privilege}" "{resource}"')
def current_role_can(context, privilege, resource):
    check_permission_current_impl(context.api, privilege, resource, False)



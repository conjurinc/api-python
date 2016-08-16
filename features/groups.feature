Feature: Group Management

  Scenario: I can list group memberships
    When I list members of "group:everyone"
    Then "cucumber:user:alice" is a member

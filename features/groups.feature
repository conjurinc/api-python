Feature: Group Management

  Scenario: I can create groups
    When I create a group "foo"
    Then it succeeds

  Scenario: I can list group memberships
    When I create a group "bar"
    Then I can list the members of group "bar" members

  Scenario: I can add members to a group
    When I create a group "developers"
    And I create a user "bob"
    And I add user "bob" to group "developers"
    Then user "bob" is a member of group "developers"

  Scenario: I can remove members from a group
    When I create a group "test"
    And I create a user "bill"
    And I add user "bill" to group "test"
    Then user "bill" is a member of group "test"
    When I remove user "bill" from group "test"
    Then user "bill" is not a member of group "test"
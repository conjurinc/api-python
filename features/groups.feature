Feature: Group Management

  Scenario: I can create groups
    When I try to create a group "foo"
    Then it succeeds

  Scenario: I can list group memberships
    When I create a group "bar"
    Then I can list the group memebers

  Scenario: I can add members to a group
    When I create a group "developers"
    And I create a user "bob"
    And I add the user to the group
    Then the user is a member of the group

  Scenario: I can remove members from a group
    When I create a group "test"
    And I create a user "bill"
    And I add the user to the group
    Then the user is a member of the group
    When I remove the user from the group
    Then the user is not a member of the group
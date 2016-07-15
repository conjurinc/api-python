@wip
Feature: I can check permissions from Python code.

  Background:
    Given a resource "food:bacon"
    And a role "jobs:cook"

  Scenario: The role does not have permission on the resource
    When I deny the role permission to "fry" the resource
    Then the role cannot "fry" the resource

  Scenario: The role can have permission on the resource
    When I grant the role permission to "fry" the resource
    Then the role can "fry" the resource

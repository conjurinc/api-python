Feature: I can check permissions from Python code.
  Scenario: Check some predefined permissions
    Given the preloaded policy
    Then "job:programmer" can not "fry" "food:bacon"
    And "user:alice" can "execute" "webservice:the-service"
    And the current role can "execute" "webservice:the-service"
    And the current role can "update" "webservice:the-service"
    But the current role can not "update" "variable:db-password"

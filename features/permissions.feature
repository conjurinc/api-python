Feature: I can check permissions from Python code.
  Scenario: Check some predefined permissions
    Then "job:programmer" can not "fry" "food:bacon"
    And "job:programmer" can "eat" "food:bacon"
    And "job:cook" can "fry" "food:bacon"
    And "job:cook" can not "eat" "food:bacon"
    And the current role can "eat" "food:bacon"
    And the current role can "fry" "food:bacon"
    But the current role can not "eat" "food:does-not-exist"

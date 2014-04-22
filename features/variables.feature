Feature: Variable manipuation

    Scenario: I can create a variable and add a value to it
        When I create a variable
        And I add a value "foo"
        Then the variable should have attribute "version_count" with value 1
        And the variable should have value "foo"


Feature: User management

  Scenario: I can create a user and authenticate with its credentials
    When I create a user
    Then I can login as the user using the api key

  Scenario: I can create a user with a password
    When I create a user with a password
    Then I can login as the user using the password
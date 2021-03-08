Feature: Manage users, addresses and accounts

  Scenario: create user
    When we create user '{"name": "Alice"}'
    Then response.content is '{"id":"1","name":"Alice"}' 
    Then user exists '{"id":1, "name": "Alice"}'


  Scenario: create user with an account
    When we create user '{"name": "Alice"}'
    When we create user account '{"name": "basic account"}' for user_id 1
    Then user exists '{"id":1, "name": "Alice"}'
    Then account exists '{"id":1, "name": "basic account"}'


  Scenario: create user with an account and an address
    When we create user '{"name": "Alice"}'
    When we create user account '{"name": "basic account"}' for user_id 1
    When we create user address '{"name": "home","content": "home address" }' for user_id 1
    Then user exists '{"id":1, "name": "Alice"}'
    Then account exists '{"id":1, "name": "basic account"}'
    Then address exists '{"id":1, "name": "home", "content": "home address"}'
    Then address exists '{"id":1, "name": "home", "content": "home address"}' for user_id 1
  

  Scenario: create user with an account and two addresses
    When we create user '{"name": "Alice"}'
    When we create user account '{"name": "basic account"}' for user_id 1
    When we create user address '{"name": "home","content": "home address" }' for user_id 1
    When we create user address '{"name": "work","content": "work address" }' for user_id 1
    Then address exists '{"id":1, "name": "home", "content": "home address"}' for user_id 1
    Then address exists '{"id":2, "name": "work", "content": "work address"}' for user_id 1


  Scenario: create two users with same address
    When we create user '{"name": "Alice"}'
    When we create user '{"name": "Bob"}'
    When we create user address '{"name": "home","content": "home address" }' for user_id 1
    When we assign address 1 to user_id 2
    Then address exists '{"id":1, "name": "home", "content": "home address"}' for user_id 1
    Then address exists '{"id":1, "name": "home", "content": "home address"}' for user_id 2


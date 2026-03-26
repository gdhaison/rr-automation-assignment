@pagination
Feature: Pagination and Result Navigation
  As a user
  I want to navigate through multiple pages of movie results
  So that I can browse the entire collection of movies available

  Background:
    Given the user opens the TMDB Discover website
    And the user is on the "Popular" category page

  @positive @smoke
  Scenario: Navigate to the next page of results
    Given the user notes the title of the first movie on the current page
    And the user verifies the movie API for page 1
    When the user scroll to pagination bar
    And the user clicks the "Next" button
    Then the movie list should update with new content

  @positive
  Scenario: Navigate to the Last page of results
    Given the user notes the title of the first movie on the current page
    When the user scroll to pagination bar
    And the user clicks the last page button
    Then the movie list should update with new content

  @positive
  Scenario: Reload page and remain on the current pagination page
    Given the user notes the title of the first movie on the current page
    When the user scroll to pagination bar
    And the user clicks the "Next" button
    Then the movie list should update with new content
    When user reload page
    Then the movie list shouldn't update with new content

  @positive
  Scenario: Navigate to the previous page of results
    Given the user notes the title of the first movie on the current page
    # And the user verifies the movie API for page 1
    When the user scroll to pagination bar
    And the user clicks the "Next" button
    And the user clicks the "Previous" button
    Then the movie list shouldn't update with new content

  @positive
  Scenario: Click button back to previous page
    Given the user notes the title of the first movie on the current page
    When the user scroll to pagination bar
    And the user clicks the "Next" button
    Then the movie list should update with new content
    When the user clicks back button of the browser
    Then the movie list shouldn't update with new content
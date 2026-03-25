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
    When the user scroll to pagination bar
    And the user clicks the "Next" button
    Then the movie list should update with new content

  @positive @smoke
  Scenario: Navigate to the Last page of results
    Given the user notes the title of the first movie on the current page
    When the user scroll to pagination bar
    And the user clicks the last page button
    Then the movie list should update with new content

#   @positive
#   Scenario: Navigate back to the previous page
#     Given the user has navigated to the second page
#     When the user clicks the "Previous" button
#     Then the user should see the first page of results again

#   @negative @known_issue
#   Scenario: Verify pagination failure on the last few pages
#     Given the user navigates to the second to last page of the results
#     When the user clicks the "Next" button to reach the final page
#     Then the system should handle the error gracefully or display a message
#     # Note: Target for the "last few pages may not function properly" bug

#   @positive
#   Scenario: Search reset pagination to page 1
#     Given the user has navigated to the "2nd" page of results
#     When the user searches for a specific movie title "Batman"
#     Then the results should display movies matching "Batman"
#     And the pagination state should reset to the first page
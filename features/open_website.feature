@regression
Feature: Open TMDB Discover Website
  Scenario: User opens the TMDB Discover homepage
    Given the user is on the TMDB Discover homepage
    Then the page title should be "TMDB Discover"

@filter @regression
Feature: Discover Filters (Type, Genre, Year, Ratings)
  As a user
  I want to filter movies/TV shows by different criteria
  So that I can quickly find content matching my preferences

  Background:
    Given the user opens the TMDB Discover website
    And the user is on the "Popular" category page

  @positive @smoke @done
  Scenario: Filter by Genre (select by text, verify API by genre_id)
    Given the user notes the title of the first item on the current list
    When the user selects Genre "Animation" in the Genre filter
    Then the result list should update with new content
    Given the user notes the title of the first item on the current list
    Then the user verifies the discover API matches UI with filters:
      | type     | movie |
      | genre_id | 16    |
      | page     | 1     |
    Then the Genre filter should show "Animation"
    

  @positive @done
  Scenario: Filter by Year range (UI should match API)
    Given the user notes the title of the first item on the current list
    When the user sets Year from "2010" to "2015"
    Then the result list should update with new content
    And the Year filter should display from "2010" to "2015"
    And the user notes the title of the first item on the current list
    And the user verifies the discover API matches UI with filters:
      | type       | movie |
      | year_from  | 2010  |
      | year_to    | 2015  |
      | page       | 1     |

  @positive @done
  Scenario: Filter by Year range input the same year
    Given the user notes the title of the first item on the current list
    When the user sets Year from "2010" to "2010"
    Then the result list should update with new content
    And the Year filter should display from "2010" to "2010"
    And the user notes the title of the first item on the current list
    And the user verifies the discover API matches UI with filters:
      | type       | movie |
      | year_from  | 2010  |
      | year_to    | 2010  |
      | page       | 1     |

  @negative @done
  Scenario: Filter by Year range input with the year from < year to
    Given the user notes the title of the first item on the current list
    When the user sets Year from "2010" to "2005"
    Then there should be "0" input with value "2005"

  @positive @smoke @done
  Scenario: Filter by Ratings (UI should match API)
    Given the user notes the title of the first item on the current list
    When the user selects rating "4.5" stars
    Then the result list should update with new content
    And the Ratings filter should show "4.5" stars
    Then the user verifies the discover API matches UI with filters:
      | type              | movie |
      | vote_average_gte  | 4.5   |
      | page              | 1     |

  @positive
  Scenario: Combine filters: Year range + Ratings (UI should match API)
    Given the user notes the title of the first item on the current list
    When the user selects rating "3.5" stars
    And the user sets Year from "2015" to "2020" 
    Then the result list should update with new content
    And the Year filter should display from "2015" to "2020"
    Then the result list should update with new content
    And the user verifies the discover API matches UI with filters:
      | type             | movie |
      | year_from        | 2015  |
      | year_to          | 2020  |
      | vote_average_gte | 3     |
      | page             | 1     |

  @positive
  Scenario: Filter Newest
  Given the user notes the title of the first item on the current list
  When the user selects "Newest" in navigation bar
  Then the Genre filter should show movies as descending order

  
  @positive
  Scenario: User call api Top rated movies
  Given the user calls API for top rated movies
  Then the API response should contain top rated movies ordered by vote_average descending
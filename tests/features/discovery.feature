Feature: Website Discovery
    As a user
    I want to discover all pages on a website
    So that I can convert them to a single markdown file

    Scenario: Discover pages from a simulated website
        Given a website at "https://treatcfsfm.org"
        And the website is simulated using local data in "tests/data/sample_site"
        When I discover the pages
        Then I should find at least 10 pages
        And the page "https://treatcfsfm.org/index.html" should be in the list

    Scenario: Generate Table of Contents and Structure
        Given a website at "https://treatcfsfm.org"
        And the website is simulated using local data in "tests/data/sample_site"
        When I generate the site structure
        Then the output should contain "Directory Structure"
        And the output should contain "/index.html"
        And the output should contain "File Summary"

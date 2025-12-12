Feature: Website Discovery
    As a user
    I want to discover all pages in a local directory
    So that I can convert them to a single markdown file

    Scenario: Discover pages from a local directory
        Given a local directory "tests/data/sample_site"
        When I discover the files
        Then I should find at least 10 files
        And the file "treatcfsfm.org/index.html" should be in the list

    Scenario: Generate Table of Contents and Structure
        Given a local directory "tests/data/sample_site"
        When I generate the site structure
        Then the output should contain "Directory Structure"
        And the output should contain "treatcfsfm.org/index.html"
        And the output should contain "File Summary"

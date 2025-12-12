Feature: Website Discovery
    As a user
    I want to discover all pages in a local directory
    So that I can convert them to a single markdown file

    Scenario: Discover pages from a local directory
        Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
        And the website contains at least 10 files
        And the website contains an "treatcfsfm.org/index.html" file
        When I discover the files
        Then I should find at least 10 files
        And the file "treatcfsfm.org/index.html" should be in the list

    Scenario: Generate Table of Contents and Structure
        Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
        And the website contains an "treatcfsfm.org/index.html" file
        When I generate the site structure
        Then the output should contain "Directory Structure"
        And the output should contain "treatcfsfm.org/index.html"
        And the output should contain "File Summary"

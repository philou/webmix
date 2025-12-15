Feature: Website Aggregation
    As a user
    I want to aggregate the entire website into a single Markdown file
    So that I can feed it to an LLM as a single context

    Scenario: Aggregate website content
        Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
        When I aggregate the website content
        Then the output should start with "# File Summary"
        And the output should contain "# Directory Structure"
        And the output should contain "# Files"
        And the output should contain "## treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html"
        And the output should contain "How I Improved My Life by Accepting My Limits"

Feature: Batch Processing
    As a user
    I want to download and aggregate a website in one go
    So that I don't have to manually run wget

    Usage: ./webmix.sh <url> [output_file]

    Note: The script creates a temporary directory for the download and cleans it up afterwards.

    @slow @network
    Scenario: Download and aggregate a small website
        Given I am in the same directory as the script "webmix.sh"
        When I run the command "./webmix.sh https://philippe.bourgau.net/complexity-assert/ webmix.md"
        Then the output file "webmix.md" should contain "uses linear regression to determine the time complexity"

Feature: Batch Processing

  The `webmix.sh` script provides a one-shot command to mirror and convert a site.

  Usage:
    ./webmix.sh <url> [output_file]

  - Context: Users want a simple CLI command to handle the full pipeline.
  - Value: Automates the wget + webmix pipeline; handles cleanup.
  - Actors: User, Script.
  - Note: The script creates a temporary directory for the download and cleans it up afterwards.

  Rule: When invoked with a URL, the system shall download and aggregate the website.

    @slow @network
    Scenario: Download and aggregate a small website
      Given I am in the same directory as the script "webmix.sh"
      When I run the command "./webmix.sh https://philippe.bourgau.net/complexity-assert/ webmix.md"
      Then the output file "webmix.md" should contain "uses linear regression to determine the time complexity"
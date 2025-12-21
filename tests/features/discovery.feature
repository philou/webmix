Feature: Website Discovery

  - Context: We need to identify files to process from a local mirror.
  - Value: Ensures we only process relevant content.
  - Actors: User, System.

  Rule: The system shall discover all HTML files in the local mirror.

    Scenario: Discover pages from a local directory
      Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
      And the website contains at least 10 files
      And the website contains an "treatcfsfm.org/index.html" file
      When I discover the files
      Then I should find at least 10 files
      And the file "treatcfsfm.org/index.html" should be in the list

  Rule: The system shall generate a structural summary of the discovered files.

    Scenario: Generate Table of Contents and Structure
      Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
      And the website contains an "treatcfsfm.org/index.html" file
      And the website contains an "treatcfsfm.org/detail-80-Getting-Through-the-Bad-Days.html" file
      And the website contains an "treatcfsfm.org/detail-104-Learning-to-Manage-Fibromyalgia.html" file
      When I generate the site structure
      Then the output should contain "Directory Structure"
      And the output should contain "treatcfsfm.org/"
      And the output should contain "index.html"
      And the output should contain "detail-80-Getting-Through-the-Bad-Days.html"
      And the output should contain "detail-104-Learning-to-Manage-Fibromyalgia.html"
      And the output should contain "File Summary"

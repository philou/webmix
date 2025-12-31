Feature: Website Discovery

  - Context: We need to identify files to process from a local mirror.
  - Value: Ensures we only process relevant content.
  - Actors: User, System.

  Rule: The system shall discover all HTML files in the local mirror.

    Scenario: Discover pages from a local directory
      Given a site with pages:
        | path |
        | index.html |
        | page1.html |
        | sub/page2.html |
      When I aggregate the website content
      Then I should find at least 3 files
      And the file "index.html" should be in the list
      And the file "sub/page2.html" should be in the list

  Rule: The system shall generate a structural summary of the discovered files.

    Scenario: Generate Table of Contents and Structure
      Given a site with pages:
        | path |
        | index.html |
        | about.html |
        | contact.html |
      When I aggregate the website content
      Then the output should contain "Directory Structure"
      And the output should contain "index.html"
      And the output should contain "about.html"
      And the output should contain "contact.html"
      And the output should contain "File Summary"

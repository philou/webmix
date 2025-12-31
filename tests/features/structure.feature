Feature: Site Structure Generation

  The system generates a visual tree structure of the website's files.

  - Context: When aggregating a website into a single file, the flat list of files can be overwhelming.
  - Value: Provides a clear overview of the site's organization, helping both users and LLMs understand the relationship between pages.
  - Actors: User (CLI), LLM (Consumer).

  Rule: The system shall generate a hierarchical Table of Contents reflecting the directory structure.

    Scenario: Generate hierarchical TOC
      Given a local directory "tests/data/hierarchical_site"
      When I aggregate the website content
      Then the output should match the structure:
        """
        - index.html
        - section-a/
          - index.html
          - page1.html
        - section-b/
          - index.html
        """

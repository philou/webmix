Feature: Site Structure Generation

  Rule: The system shall generate a hierarchical Table of Contents reflecting the directory structure.

    Scenario: Generate hierarchical TOC
      Given a local directory "tests/data/hierarchical_site"
      When I generate the site structure
      Then the output should match the structure:
        """
        - index.html
        - section-a/
          - index.html
          - page1.html
        - section-b/
          - index.html
        """

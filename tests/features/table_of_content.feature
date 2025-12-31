Feature: Table of Content Generation

  The system generates a visual Table of Content of the website's files.

  - Context: When aggregating a website into a single file, the flat list of files can be overwhelming.
  - Value: Provides a clear overview of the site's organization, helping both users and LLMs understand the relationship between pages.
  - Actors: User (CLI), LLM (Consumer).

  Rule: The system shall generate a hierarchical Table of Contents reflecting the directory structure.

    Scenario: Generate hierarchical TOC
      Given a site with pages:
        | path | content |
        | index.html | <html><body>Home</body></html> |
        | section-a/index.html | <html><body>Section A</body></html> |
        | section-a/page1.html | <html><body>Page 1</body></html> |
        | section-b/index.html | <html><body>Section B</body></html> |
      When I aggregate the website content
      Then the output should match the table of content:
        """
        - index.html
        - section-a/
          - index.html
          - page1.html
        - section-b/
          - index.html
        """

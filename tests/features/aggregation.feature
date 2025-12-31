Feature: Website Aggregation

  The core value proposition of Webmix is creating a single context file for LLMs.
  - Context: Users need to feed entire documentation sites to LLMs.
  - Value: Enables "chat with your docs" without RAG complexity.
  - Actors: User, LLM.

  Rule: The system shall aggregate all discovered content into a single Markdown file.

    Scenario: Aggregate website content
      Given a site with pages:
        | path | body |
        | index.html | Home |
        | page1.html | Page 1 Content |
      When I aggregate the website content
      Then the output should start with "# File Summary"
      And the output should contain "# Directory Structure"
      And the output should contain "# Files"
      And the output should contain "## page1.html"
      And the output should contain "Page 1 Content"

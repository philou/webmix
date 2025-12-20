Feature: Website Aggregation

  The core value proposition of Webmix is creating a single context file for LLMs.
  - Context: Users need to feed entire documentation sites to LLMs.
  - Value: Enables "chat with your docs" without RAG complexity.
  - Actors: User, LLM.

  Rule: The system shall aggregate all discovered content into a single Markdown file.

    Scenario: Aggregate website content
      Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
      When I aggregate the website content
      Then the output should start with "# File Summary"
      And the output should contain "# Directory Structure"
      And the output should contain "# Files"
      And the output should contain "## treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html"
      And the output should contain "How I Improved My Life by Accepting My Limits"

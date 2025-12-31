Feature: Link Rewriting

  - Context: Original HTML links break when files are merged.
  - Value: Preserves navigability within the single file.
  - Actors: User, System.

  Rule: The system shall rewrite internal links to point to the aggregated sections.

    Scenario: Rewrite internal links to show target page titles

      Links to other pages in the site are rewritten to reference the target page's title, making them useful in a single-file context.

      Given a site with pages:
        | path | title | link |
        | source.html | Source Page | [recovery story](target.html) |
        | target.html | Target Page Title | |
      When I aggregate the website content
      Then the output should contain "recovery story (see: Target Page Title)"

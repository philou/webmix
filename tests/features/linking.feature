Feature: Link Rewriting

  - Context: Original HTML links break when files are merged.
  - Value: Preserves navigability within the single file.
  - Actors: User, System.

  Rule: The system shall rewrite internal links to point to the aggregated sections.

    Scenario: Rewrite internal links to show target page titles
      Given a site with pages:
        | path | body |
        | source.html | <p>In my mind, consistency is both a major challenge and the key to success in pacing. Of the strategies I investigated, I found six especially useful and crucial to my recovery.</p><p>I agree with Dean Anderson, whose <a href="target.html">recovery story</a> is included in the Success Stories on this site. What helped me was to learn to live my life in a new and different way.</p> |
        | target.html | <title>Target Page Title</title><h1>Target Page Title</h1><p>Some content.</p> |
      When I aggregate the website content
      Then the output should contain "recovery story (see: Target Page Title)"

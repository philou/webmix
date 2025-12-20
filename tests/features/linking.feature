Feature: Link Rewriting

  - Context: Original HTML links break when files are merged.
  - Value: Preserves navigability within the single file.
  - Actors: User, System.

  Rule: The system shall rewrite internal links to point to the aggregated sections.

    Scenario: Rewrite internal links to show target page titles
      Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
      And the file "treatcfsfm.org/detail-66-Consistency-A-Key-to-Pacing-Success.html" contains "<a href="detail-35-Acceptance,-Discipline-Hope-A-Story-of-Recovery-from-CFIDS.html">recovery story</a>"
      When I aggregate the website content
      Then the output should contain "recovery story (see: Acceptance, Discipline & Hope: A Story of Recovery from CFIDS)"

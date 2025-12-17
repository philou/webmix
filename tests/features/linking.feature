Feature: Link Rewriting
    As a user
    I want internal links to be rewritten as textual references
    So that I can understand the relationship between pages in the single aggregated file

    Scenario: Rewrite internal links to show target page titles
        Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
        And the file "treatcfsfm.org/detail-66-Consistency-A-Key-to-Pacing-Success.html" contains "<a href="detail-35-Acceptance,-Discipline-Hope-A-Story-of-Recovery-from-CFIDS.html">recovery story</a>"
        When I aggregate the website content
        Then the output should contain "recovery story (see: Acceptance, Discipline & Hope: A Story of Recovery from CFIDS)"

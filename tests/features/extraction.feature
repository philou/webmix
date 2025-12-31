Feature: Content Extraction

  - Context: HTML contains noise (nav, ads) that distracts LLMs.
  - Value: High signal-to-noise ratio in the output.
  - Actors: User, System.

  Rule: The system shall extract the main content from HTML files.

    Scenario: Extract content from HTML to Markdown
      Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
      And the file "treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html" contains "<i>Note: Bianca Veness, a CFS patient from Australia"
      When I extract the content from "treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html"
      Then the output should contain "Note: Bianca Veness, a CFS patient from Australia"

  Rule: The system shall remove navigation and boilerplate elements.

    Scenario: Clean up margin links

      Navigation menus and sidebars are stripped out to leave only the relevant article content.

      Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
      And the file "treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html" contains "<li><a href="index.html" >Home</a></li>"
      When I extract the content from "treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html"
      Then the output should not contain "Home"
      And the output should not contain "Contact Us"
      And the output should not contain "Self-Appraisal"

  Rule: Where images are present in the content, the system shall preserve their alt text.

    Scenario: Extract alt text from images
      Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
      And the file "treatcfsfm.org/menubar-Pacing-vs.-Push-and-Crash-148.html" contains "alt="The Push/Crash Cycle""
      When I extract the content from "treatcfsfm.org/menubar-Pacing-vs.-Push-and-Crash-148.html"
      Then the output should contain "![The Push/Crash Cycle The Push/Crash Cycle]"

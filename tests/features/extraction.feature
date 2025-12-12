Feature: Content Extraction
    As a user
    I want to extract the main content from an HTML page
    So that I can have a clean markdown version without navigation or ads

    Scenario: Extract content from HTML to Markdown
        Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
        And the file "treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html" contains "<i>Note: Bianca Veness, a CFS patient from Australia"
        When I extract the content from "treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html"
        Then the output should contain "Note: Bianca Veness, a CFS patient from Australia"

    Scenario: Clean up margin links
        Given the website "treatcfsfm.org" downloaded in local directory "tests/data/sample_site"
        And the file "treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html" contains "<li><a href="index.html" >Home</a></li>"
        When I extract the content from "treatcfsfm.org/detail-100-How-I-Improved-My-Life-by-Accepting-My-Limits.html"
        Then the output should not contain "Home"
        And the output should not contain "Contact Us"
        And the output should not contain "Self-Appraisal"

Feature: Sitemap Support

  - Context: Websites often have a logical structure (Sitemap) that differs from their physical file structure.
  - Value: Provides a more meaningful Table of Contents and reading order for the LLM.
  - Actors: User, System.
  - References: TODO.md

  Rule: Where a sitemap is available, the system shall use it to generate the Table of Contents.

    Scenario: Parse standard XML sitemap

      The site has a sitemap that does not contain the contact page, so it should not appear in the ToC.

      Given a site with pages:
        | path | body |
        | index.html | Home |
        | about/index.html | About |
        | contact/index.html | Contact |
      And the site contains a "sitemap.xml" with:
        """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
           <url><loc>http://example.com/index.html</loc></url>
           <url><loc>http://example.com/about/index.html</loc></url>
        </urlset>
        """
      When I aggregate the website content
      Then the output should match the table of content:
        """
        - about/
          - index.html
        - index.html
        """

  Rule: Where a sitemap is explicitly provided, the system shall use it instead of auto-discovery.

    Scenario: Override with CLI argument

      The user provides a custom sitemap that lists contact and about pages, but not the home page.

      Given a site with pages:
        | path | body |
        | index.html | Home |
        | about/index.html | About |
        | contact/index.html | Contact |
      And a standard sitemap
      And the site contains a "custom-sitemap.xml" with:
        """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
           <url><loc>http://example.com/contact/index.html</loc></url>
           <url><loc>http://example.com/about/index.html</loc></url>
        </urlset>
        """
      When I aggregate the website content with argument "--sitemap custom-sitemap.xml"
      Then the output should match the table of content:
        """
        ## contact/index.html
        ## about/index.html
        """

  Rule: If no sitemap is available, then the system shall fallback to directory structure.

    Scenario: Fallback to directory walking
      Given a site with pages:
        | path | body |
        | index.html | Home |
        | page1.html | Page 1 |
      When I aggregate the website content
      Then the output should match the table of content:
        """
        - index.html
        - page1.html
        """

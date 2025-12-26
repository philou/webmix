Feature: Sitemap Support

  - Context: Websites often have a logical structure (Sitemap) that differs from their physical file structure.
  - Value: Provides a more meaningful Table of Contents and reading order for the LLM.
  - Actors: User, System.
  - References: TODO.md

  Rule: Where a sitemap is available, the system shall use it to generate the Table of Contents.

    Scenario: Parse standard XML sitemap
      Given a local mirror of "simple-site"
      And the site contains a "sitemap.xml" with:
        """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
           <url><loc>http://example.com/</loc></url>
           <url><loc>http://example.com/about</loc></url>
           <url><loc>http://example.com/contact</loc></url>
        </urlset>
        """
      When I generate the webmix
      Then the Table of Contents should follow the order:
        | / |
        | /about |
        | /contact |

  Rule: Where a sitemap is explicitly provided, the system shall use it instead of auto-discovery.

    Scenario: Override with CLI argument
      Given a local mirror of "simple-site"
      And the site contains a "sitemap.xml" with:
        """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
           <url><loc>http://example.com/</loc></url>
           <url><loc>http://example.com/about</loc></url>
           <url><loc>http://example.com/contact</loc></url>
        </urlset>
        """
      And the site contains a "custom-sitemap.xml" with:
        """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
           <url><loc>http://example.com/contact</loc></url>
           <url><loc>http://example.com/about</loc></url>
        </urlset>
        """
      When I generate the webmix with argument "--sitemap custom-sitemap.xml"
      Then the Table of Contents should follow the order:
        | /contact |
        | /about |

  Rule: If no sitemap is available, then the system shall fallback to directory structure.

    Scenario: Fallback to directory walking
      Given a local mirror of "no-sitemap-site"
      And the site does not contain "sitemap.xml"
      When I generate the webmix
      Then the Table of Contents should reflect the directory structure

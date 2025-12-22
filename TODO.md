## Plan: Webmix (Agentic BDD Experiment)

We will build a Python CLI tool to crawl, extract (Reader Mode), and aggregate a website into a single Markdown file. We will use **pytest-bdd** for specs and **Trafilatura** for extraction. We will implement a **Fetcher Abstraction** to switch between a real HTTP client and a **Local Website Simulator** for fast, deterministic testing.

Note on Sanitization: `trafilatura` handles the heavy lifting of cleaning HTML (Reader Mode), so we don't need to implement complex sanitization logic ourselves.

### Steps
- [x] Project Scaffolding & Test Data
    - [x] Initialize Poetry project with `pytest`, `pytest-bdd`, `trafilatura`, `requests`, `typer`.
    - [x] Create `README.md` and other meta info files.
    - [x] Action: Download a small subset of the target site (or a dummy site) into `tests/data/sample_site` to serve as our "Simulator" data source.

- [x] Feat: Discovery & TOC (Initial Implementation)
    - [x] Spec: `features/discovery.feature`. Scenario: "Given a website root, discover pages and generate a Table of Contents."
    - [x] Sub-step: Core Abstraction (The Fetcher)
        - [x] Goal: Define a `WebFetcher` protocol (interface) with methods like `get_html(url)` and `get_sitemap(url)`.
        - [x] Implementations:
            - [x] `HttpFetcher`: The real implementation using `requests`/`trafilatura`.
            - [x] `LocalFetcher`: The simulator that maps URLs to files in `tests/data/sample_site`.
    - [x] Test: Inject `LocalFetcher`. Verify it finds pages and returns a Markdown list of links to be used as the TOC.
    - [x] Refinement: The output format should mimic `repomix` structure:
        1.  File Summary (Purpose, Format, Usage)
        2.  Directory Structure (Tree view of the site)
        3.  Files (The actual content sections)

- [x] Refactor: Switch to Filesystem-First Approach (Option B)
    - [x] Goal: Simplify the architecture by assuming `wget` has already mirrored the site to a local directory. Remove the `Fetcher` abstraction.
    - [x] Refactor `discovery.py`: Instead of crawling links via `WebFetcher`, implement `discover_files(directory_path)` using `os.walk` to find all HTML files.
    - [x] Refactor Tests: Update `discovery.feature` and `test_discovery.py` to use "Given a local directory..." instead of "Given a website URL...".
    - [x] Cleanup: Remove `webmix/fetcher.py` and `HttpFetcher`.

- [x] Manual Test Entrypoint
    - [x] Goal: Create a `main.py` or CLI entrypoint using `typer` to run the tool manually against a local folder.
    - [x] Implementation: `webmix/main.py` should accept a directory path and print the generated structure/TOC to stdout.

- [x] Feat: Content Extraction (Reader Mode)
    - [x] Spec: `features/extraction.feature`. Scenario: "Given a local HTML file, return clean Markdown."
    - [x] Test: Read a specific HTML file from the `tests/data/sample_site` and assert the Markdown output is clean (no nav/ads).

- [x] Feat: Aggregation
    - [x] Spec: `features/aggregation.feature`.
    - [x] Test: Verify the final output starts with a TOC and contains all sections concatenated.

- [x] Feat: Link Rewriting
    - [x] Spec: `features/linking.feature`. Scenario: "Links between pages are converted to explicit textual references."
    - [x] Test: Verify `[Link](page2.html)` becomes `Link (see: Page 2 Title)` or similar clear text in the final output.
    - Note: Since `wget --convert-links` makes links relative, we just need to resolve them to the target file's title/anchor.
    - [x] There is hard coded reference to the sample website 'treatcfsfm.org/' in rewrite_link. There should not.

- [x] Batch Script
    - [x] Create a shell script `webmix.sh` (or similar) that:
        1.  Takes a URL as input.
        2.  Runs `wget` to mirror the site to a temporary folder. If given an url with a subfolder, it should download what it under this subfolder, not the whole domain (ex: with https://philippe.bourgau.net/storexplore/, dont' download the whole https://philippe.bourgau.net/). I think this is the --no-parent option of wget
        3.  Runs `webmix` on that folder.
        4.  Cleans up the temporary folder (optional).
    - [x] Add a feature test for this too
        - make it disabled by default so that it does not slow down other tests, and does not fail when we don't have an internet connection.
        - use the website https://philippe.bourgau.net/complexity-assert/ as an example: it's small and fast
    - [x] disable the batch.feature tests by default.
        - [x] also fix the warnings when running the tests (unknown @slow @network tags...)

- Doc: Agentic BDD experimenting
    - [x] Instructions for this style of TODO.md
    - [x] Instruction for mixed "risk-aware + conventional" commit messages
    - [x] Instructions for BDD/Gherkin style (EARS + Rules)
    - [x] Create or customize an agent to write the specs, maybe asking me questions (Example Mapping style?)
    - [x] Add instructions for a glossary file. Maybe try with contextize
    - [x] Create an agent to follow a flow:
        - Walking Skeleton
        - Pause after specs for reviews
        - Do implementation
        - Review Living Documentation:
            - Vocab missing
            - Docs still up to date
            - ADRs to write
            - duplication in tests and steps
        - Pause for review and commit

- [x] Review specs to have more domain context
- [x] Review and improve README

- [x] Refactor: remove duplicated feature step definition

- [x] Feat: alt text for images

- [x] Ask BDD developer agent to
    - not pause so often (eats up premium requests)
    - pause before the commit! Actually, I will be doing the commit

- [x] Feat: Breadcrumbs, hierarchical extraction

- [x] Refactor: Migrate to uv

- [x] Feat: Sitemaps. Rely on the sitemap hierarchy rather than folder structure to build the Table of Content
    - [x] If the website has a ./sitemap.xml: Automatically use the hierarchy found in the sitemap.xml to buidl the table of content. (You might need to look at the specifications of sitemap xml to know how to rebuild the hierarchy)
    - [x] If the website has no sitemap.xml, use subdirectory structure as we are already doing

- [x] Feat: sitemap option. It should be possible to override the sitemap (or the absence of sitemap) by passing in an optional local sitemap file through the command line.

- [x] Feat: Create a small standalone app that builds a sitemap.xml from the the sample website treatcfsfm.org which has a sitemap.php.html file that is not xml. You'll need to do some form of scrapping or parsing, It uses html nesting depth and custom classes to represent the hierarchy of topics.


### Parking
- [ ] Improve sitemap.feature:
    - there is a hard coded translation of paths to titles in the step def
    - the second scenario, where we expect to use the overriden sitemap hides stuff in the step definition
- [ ] refactor the Discovery and ToC tests to use builders instead of a full website
    *   For Structural Logic (Discovery, Linking, Aggregation): Use Builders.
        *   *Why:* We care about the graph/links, not the messy HTML content.
        *   *How:* `Given a site with pages: | url | title | content |` (Generates simple HTML on the fly).
    *   For Parsing Logic (Extraction): Use Hybrid (Fixtures + Assertions).
        *   *Why:* We need realistic, messy HTML (ads, scripts) to test `trafilatura`, but we also need readable tests.
        *   *How:* `Given the fixture "article_with_ads.html"` AND `And the page contains a sidebar with "Subscribe Now"` (Loads real file but asserts its content in the step to prevent drift).
- [ ] strip out files from the sample data to have faster tests, or migrate to a smaller website, like https://philippe.bourgau.net/storexplore/
- [ ] Feat: filter out remaining noise (there are some "|" remaining here and there)

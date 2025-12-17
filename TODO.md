## Plan: Webmix (Agentic BDD Experiment)

We will build a Python CLI tool to crawl, extract (Reader Mode), and aggregate a website into a single Markdown file. We will use **pytest-bdd** for specs and **Trafilatura** for extraction. We will implement a **Fetcher Abstraction** to switch between a real HTTP client and a **Local Website Simulator** for fast, deterministic testing.

Note on Sanitization: `trafilatura` handles the heavy lifting of cleaning HTML (Reader Mode), so we don't need to implement complex sanitization logic ourselves.

### Testing Strategy (Split Approach)
*   For Structural Logic (Discovery, Linking, Aggregation): Use Builders.
    *   *Why:* We care about the graph/links, not the messy HTML content.
    *   *How:* `Given a site with pages: | url | title | content |` (Generates simple HTML on the fly).
*   For Parsing Logic (Extraction): Use Hybrid (Fixtures + Assertions).
    *   *Why:* We need realistic, messy HTML (ads, scripts) to test `trafilatura`, but we also need readable tests.
    *   *How:* `Given the fixture "article_with_ads.html"` AND `And the page contains a sidebar with "Subscribe Now"` (Loads real file but asserts its content in the step to prevent drift).

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

- [ ] Feat: Link Rewriting
    - [x] Spec: `features/linking.feature`. Scenario: "Links between pages are converted to explicit textual references."
    - [x] Test: Verify `[Link](page2.html)` becomes `Link (see: Page 2 Title)` or similar clear text in the final output.
    - Note: Since `wget --convert-links` makes links relative, we just need to resolve them to the target file's title/anchor.
    - [ ] There is hard coded reference to the sample website 'treatcfsfm.org/' in rewrite_link. There should not.

- [ ] Batch Script
    - [ ] Create a shell script `webmix.sh` (or similar) that:
        1.  Takes a URL as input.
        2.  Runs `wget` to mirror the site to a temporary folder.
        3.  Runs `webmix` on that folder.
        4.  Cleans up the temporary folder (optional).

- [ ] Refactor: remove duplicated feature step definition

- [ ] Feat: alt text for images

- [ ] Feat: Breadcrumbs, hierarchical extraction (follow sitemap in ToC)


### Parking
- [ ] Review specs to have more domain context, and create a glossary
- [ ] refactor the Discovery and ToC tests to use builders instead of a full website
- [ ] strip out files from the sample data to have faster tests
- Agentic BDD experimenting
    - [ ] Create or customize an agent to write the specs, maybe asking me questions (Example Mapping style?)
    - [ ] Create an agent to follow a flow:
        - Walking Skeleton
        - Pause after specs for reviews
        - Do implementation
        - Review BDD/DDD:
            - Vocab missing
            - Docs still up to date
            - ADRs to write
        - Pause for review and commit
    - [ ] Instructions for this style of TODO.md
    - [ ] Instructions for testing strategy (builders vs website)
    - [ ] Instruction for mixed "risk-aware + conventional" commit messages
- [ ] Feat: filter out remaining noise (there are some "|" remaining here and there)

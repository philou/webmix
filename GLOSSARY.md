# Domain Glossary

This document defines the **Ubiquitous Language** for the Webmix project. Use these terms consistently in code, tests, feature files, and documentation.

## Core Concepts

### Aggregation
The process of combining multiple extracted pages into a single, cohesive Markdown document.
*   **Synonyms:** Compilation, Merging.
*   **Output:** The "Webmix" file.

### Batch Mode
The mode of operation where the tool processes a complete website mirror (downloaded via `wget`) in one go.
*   **Context:** `webmix.sh` script.

### Discovery
The phase where the system identifies which files or pages belong to the target website.
*   **Mechanism:** Currently filesystem walking (`os.walk`) on a local mirror.
*   **Artifact:** A list of file paths or a tree structure.

### Extraction
The process of parsing a single HTML file and converting its main content into clean Markdown.
*   **Mechanism:** Uses `trafilatura` (Reader Mode).
*   **Goal:** Remove navigation, ads, footers, and boilerplate.

### Link Rewriting
The transformation of internal hyperlinks (pointing to other HTML files) into internal Markdown anchors (pointing to sections within the aggregated file).
*   **Goal:** Offline navigability.
*   **Format:** `[Link Text](#target-anchor) (see: Target Title)`.

### Local Mirror
A directory containing a copy of a website's HTML files, preserving the original directory structure.
*   **Source:** Usually created by `wget --mirror`.

### Reader Mode
The specific heuristic used during **Extraction** to identify the "meat" of an article and discard the "shell" (nav, sidebar).

### Structure Generation
The process of creating the **Table of Contents** and **Directory Structure** visualization from the discovered files.
*   **Output:** A tree view and a list of links at the start of the aggregated file.

### Table of Contents (TOC)
The hierarchical list of links generated at the beginning of the aggregated file, reflecting the structure of the **Local Mirror**.

### Webmix File
The final single Markdown file produced by the **Aggregation** process.
*   **Structure:** File Summary -> Directory Structure -> Files (Content).

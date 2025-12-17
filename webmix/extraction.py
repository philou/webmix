import trafilatura
import os
import re
from typing import Optional, Dict

def extract_content(file_path: str, link_map: Optional[Dict[str, str]] = None) -> Optional[str]:
    """
    Extract the main content from an HTML file using trafilatura.
    Returns the content as Markdown, including the title.
    
    Args:
        file_path: Path to the HTML file.
        link_map: A dictionary mapping relative URLs to page titles for link rewriting.
    """
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
        
    # Use bare_extraction to get metadata
    doc = trafilatura.bare_extraction(html_content)
    
    if not doc:
        return None
        
    title = doc.title
    
    # Fallback for title if trafilatura missed it
    if not title:
        match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if match:
            title = match.group(1).strip()
            
    # Get Markdown content using extract()
    # We need to ensure links are preserved.
    text = trafilatura.extract(html_content, output_format='markdown', include_links=True)
    
    # Construct Markdown
    output = []
    if title:
        output.append(f"# {title}")
        output.append("")
        
    if text:
        # Rewrite links if link_map is provided
        if link_map:
            text = rewrite_links(text, link_map)
        output.append(text)
        
    return "\n".join(output)

def rewrite_links(text: str, link_map: Dict[str, str]) -> str:
    """
    Rewrite markdown links [Text](url) to [Text (see: Title)](url) or similar.
    Actually, the requirement is "Home (see: Treating CFS & FM)".
    So we want to replace `[Link Text](url)` with `Link Text (see: Target Title)`.
    """
    def replace_link(match):
        link_text = match.group(1)
        url = match.group(2)
        
        # Normalize URL (remove anchor, etc if needed, but for now simple lookup)
        # The link_map keys should match the URLs found in the markdown.
        # Trafilatura might convert relative links.
        
        # Check if we have a title for this URL
        if url in link_map:
            target_title = link_map[url]
            return f"{link_text} (see: {target_title})"
            
        # Try matching just the filename if the path doesn't match exactly
        filename = os.path.basename(url)
        if filename in link_map:
            target_title = link_map[filename]
            return f"{link_text} (see: {target_title})"
            
        # Try matching with 'treatcfsfm.org/' prefix if it's missing (hack for sample site structure)
        # The sample site has files in a subdir but links might be relative
        if not url.startswith('treatcfsfm.org/') and f"treatcfsfm.org/{url}" in link_map:
             target_title = link_map[f"treatcfsfm.org/{url}"]
             return f"{link_text} (see: {target_title})"
             
        # Try matching without 'treatcfsfm.org/' prefix if it's present in link_map keys
        # This handles cases where link_map keys are relative to the root of the crawl
        # but the link in the file is relative to the file itself.
        
        return match.group(0)

    # Regex for Markdown links: [text](url)
    # Trafilatura might not be outputting markdown links for some reason in this specific file?
    # Let's check if we can force it.
    # Or maybe the link text "recovery story" is not being detected as a link by Trafilatura?
    # Wait, in the debug output: "I agree with Dean Anderson, whose recovery story is included..."
    # There are NO brackets around "recovery story".
    # This means Trafilatura is stripping the link but keeping the text!
    # This happens if Trafilatura thinks the link is not important or if we need to configure it.
    # We need to tell Trafilatura to keep links.
    # trafilatura.extract(..., with_metadata=True, include_links=True) ?
    # No, include_links is not a standard option for extract() but maybe in settings?
    # Actually, trafilatura usually keeps links in markdown output.
    # Let's try adding `include_links=True` to extract().
    
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, text)

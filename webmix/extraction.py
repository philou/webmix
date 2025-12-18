import trafilatura
import os
import re
from typing import Optional, Dict

def extract_content(file_path: str, link_map: Optional[Dict[str, str]] = None, current_path: Optional[str] = None) -> Optional[str]:
    """
    Extract the main content from an HTML file using trafilatura.
    Returns the content as Markdown, including the title.
    
    Args:
        file_path: Path to the HTML file.
        link_map: A dictionary mapping relative URLs to page titles for link rewriting.
        current_path: The relative path of the current file, used for resolving relative links.
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
            text = rewrite_links(text, link_map, current_path)
        output.append(text)
        
    return "\n".join(output)

def rewrite_links(text: str, link_map: Dict[str, str], current_path: Optional[str] = None) -> str:
    """
    Rewrite markdown links [Text](url) to [Text (see: Title)](url) or similar.
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
            
        # Resolve relative path if current_path is known
        if current_path and not url.startswith(('http:', 'https:', 'ftp:', 'mailto:', '#')):
             # url is likely relative
             current_dir = os.path.dirname(current_path)
             resolved_path = os.path.normpath(os.path.join(current_dir, url))
             
             if resolved_path in link_map:
                 target_title = link_map[resolved_path]
                 return f"{link_text} (see: {target_title})"
        
        return match.group(0)

    # Regex for Markdown links: [text](url)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, text)

import trafilatura
import os
import re
from typing import Optional

def extract_content(file_path: str) -> Optional[str]:
    """
    Extract the main content from an HTML file using trafilatura.
    Returns the content as Markdown, including the title.
    """
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
        
    # Use bare_extraction to get metadata and text separately
    doc = trafilatura.bare_extraction(html_content)
    
    if not doc:
        return None
        
    title = doc.title
    text = doc.text
    
    # Fallback for title if trafilatura missed it
    if not title:
        match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if match:
            title = match.group(1).strip()
            
    # Construct Markdown
    output = []
    if title:
        output.append(f"# {title}")
        output.append("")
        
    if text:
        output.append(text)
        
    return "\n".join(output)

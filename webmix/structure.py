from typing import List, Optional, Dict
import os
import re
from webmix.extraction import extract_content

def generate_file_summary(files: List[str]) -> str:
    return f"""# File Summary

This file contains the content of {len(files)} pages from the website.
"""

def generate_directory_structure(files: List[str]) -> str:
    structure = "# Directory Structure\n\n"
    
    # Files are already relative paths
    sorted_files = sorted(files)
    
    for path in sorted_files:
        structure += f"- {path}\n"
        
    return structure

def build_link_map(base_dir: str, files: List[str]) -> Dict[str, str]:
    """
    Build a map of filename -> title for all files.
    This will be used to rewrite links.
    """
    link_map = {}
    for relative_path in files:
        full_path = os.path.join(base_dir, relative_path)
        # We need to extract just the title efficiently.
        # For now, let's reuse extract_content but maybe optimize later?
        # Or just peek at the title.
        # Let's do a quick title extraction.
        if not os.path.exists(full_path):
            continue
            
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if match:
                title = match.group(1).strip()
                # Clean up title (e.g. remove " | Site Name")
                if "|" in title:
                    title = title.split("|")[0].strip()
                link_map[relative_path] = title
                # Also map just the filename if it's unique? 
                # Trafilatura might output links as just filenames.
                link_map[os.path.basename(relative_path)] = title
                
    return link_map

def generate_files_content(base_dir: str, files: List[str]) -> str:
    content_section = "# Files\n\n"
    sorted_files = sorted(files)
    
    # Build the link map first
    link_map = build_link_map(base_dir, files)
    
    for relative_path in sorted_files:
        full_path = os.path.join(base_dir, relative_path)
        content = extract_content(full_path, link_map=link_map, current_path=relative_path)
        
        if content:
            content_section += f"## {relative_path}\n\n"
            content_section += f"{content}\n\n"
        else:
            # Handle cases where extraction fails or file is empty
            content_section += f"## {relative_path}\n\n"
            content_section += "(Content could not be extracted)\n\n"
            
    return content_section

def generate_webmix_output(files: List[str], base_dir: Optional[str] = None) -> str:
    summary = generate_file_summary(files)
    structure = generate_directory_structure(files)
    
    output = f"{summary}\n{structure}\n"
    
    if base_dir:
        files_content = generate_files_content(base_dir, files)
        output += f"{files_content}"
        
    return output

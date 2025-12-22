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
    
    # Build tree
    tree = {}
    for path in sorted(files):
        parts = path.split('/')
        current = tree
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # File
                current[part] = None
            else:
                # Directory
                if part not in current:
                    current[part] = {}
                current = current[part]
                
    # Format tree
    def format_tree(node, indent=0):
        output = ""
        # Sort keys: directories first or files first? 
        # Usually mixed, alphabetical.
        for key in sorted(node.keys()):
            value = node[key]
            prefix = "  " * indent
            if value is None:
                # File
                output += f"{prefix}- {key}\n"
            else:
                # Directory
                output += f"{prefix}- {key}/\n"
                output += format_tree(value, indent + 1)
        return output

    structure += format_tree(tree)
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
    # Do not sort files here, respect the order provided (e.g. from sitemap)
    
    # Build the link map first
    link_map = build_link_map(base_dir, files)
    
    for relative_path in files:
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

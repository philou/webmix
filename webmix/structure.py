from typing import List, Optional
import os
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

def generate_files_content(base_dir: str, files: List[str]) -> str:
    content_section = "# Files\n\n"
    sorted_files = sorted(files)
    
    for relative_path in sorted_files:
        full_path = os.path.join(base_dir, relative_path)
        content = extract_content(full_path)
        
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

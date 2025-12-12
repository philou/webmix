from typing import List

def generate_file_summary(files: List[str]) -> str:
    return f"""# File Summary

This file contains the content of {len(files)} pages from the website.
"""

def generate_directory_structure(files: List[str]) -> str:
    structure = "# Directory Structure\n\n"
    
    # Files are already relative paths
    sorted_files = sorted(files)
    
    for path in sorted_files:
        # Add leading slash to mimic previous output format if desired, 
        # or keep as relative path. Let's keep it simple: relative path.
        structure += f"- {path}\n"
        
    return structure

def generate_repomix_output(files: List[str]) -> str:
    summary = generate_file_summary(files)
    structure = generate_directory_structure(files)
    
    return f"{summary}\n{structure}\n"

import os
from typing import List

def discover_files(base_dir: str, extensions: List[str] = ['.html', '.htm']) -> List[str]:
    """
    Recursively find all files with specific extensions in a directory.
    Returns a list of paths relative to the base_dir.
    """
    found_files = []
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                full_path = os.path.join(root, file)
                # Get path relative to base_dir
                rel_path = os.path.relpath(full_path, base_dir)
                # Ensure forward slashes for consistency
                rel_path = rel_path.replace(os.sep, '/')
                found_files.append(rel_path)
                
    return sorted(found_files)

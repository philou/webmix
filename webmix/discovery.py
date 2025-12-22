import os
import xml.etree.ElementTree as ET
from typing import List
from urllib.parse import urlparse

def discover_files(base_dir: str, extensions: List[str] = ['.html', '.htm']) -> List[str]:
    """
    Recursively find all files with specific extensions in a directory.
    Returns a list of paths relative to the base_dir.
    If sitemap.xml exists, uses it to determine the file order.
    """
    # Check for sitemap.xml
    sitemap_path = os.path.join(base_dir, "sitemap.xml")
    if os.path.exists(sitemap_path):
        try:
            return discover_files_from_sitemap(base_dir, sitemap_path)
        except Exception as e:
            print(f"Warning: Failed to parse sitemap.xml: {e}. Falling back to directory walk.")
    
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

def discover_files_from_sitemap(base_dir: str, sitemap_path: str) -> List[str]:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # Handle namespaces
    # The default namespace is usually http://www.sitemaps.org/schemas/sitemap/0.9
    namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    urls = []
    # Try with namespace
    for url in root.findall('ns:url', namespaces):
        loc = url.find('ns:loc', namespaces)
        if loc is not None and loc.text:
            urls.append(loc.text)
            
    # If no URLs found, try without namespace (fallback)
    if not urls:
        for url in root.findall('url'):
            loc = url.find('loc')
            if loc is not None and loc.text:
                urls.append(loc.text)
                
    files = []
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path
        
        # Remove leading slash
        if path.startswith('/'):
            path = path[1:]
            
        # Map to local file
        candidates = []
        if not path:
            candidates.append("index.html")
        elif path.endswith('/'):
            candidates.append(os.path.join(path, "index.html"))
        else:
            # Try exact match, then .html, then /index.html
            candidates.append(path)
            candidates.append(path + ".html")
            candidates.append(os.path.join(path, "index.html"))
            
        found = False
        for candidate in candidates:
            full_path = os.path.join(base_dir, candidate)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                files.append(candidate.replace(os.sep, '/'))
                found = True
                break
        
        # If not found, we skip it. The sitemap might contain URLs that were not downloaded.
            
    return files

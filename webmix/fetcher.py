from typing import Protocol, Optional
import os
import requests
from urllib.parse import urlparse

class WebFetcher(Protocol):
    def get_content(self, url: str) -> Optional[str]:
        """Retrieve the content of a URL."""
        ...

class HttpFetcher:
    def get_content(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None

class LocalFetcher:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def get_content(self, url: str) -> Optional[str]:
        parsed = urlparse(url)
        # Remove leading slash from path
        path = parsed.path.lstrip('/')
        if not path:
            path = "index.html"
        elif path.endswith('/'):
            path += "index.html"
            
        # Construct local path: base_dir / domain / path
        # The wget download created a directory with the domain name
        domain = parsed.netloc
        local_path = os.path.join(self.base_dir, domain, path)
        
        if os.path.exists(local_path):
            with open(local_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        return None

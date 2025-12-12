from typing import List, Set
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from webmix.fetcher import WebFetcher

def discover_pages(start_url: str, fetcher: WebFetcher, max_pages: int = 100) -> List[str]:
    visited: Set[str] = set()
    queue: List[str] = [start_url]
    found_pages: List[str] = []
    
    start_domain = urlparse(start_url).netloc

    while queue and len(found_pages) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        
        visited.add(url)
        content = fetcher.get_content(url)
        
        if content:
            found_pages.append(url)
            soup = BeautifulSoup(content, 'html.parser')
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    full_url = urljoin(url, href)
                    # Normalize URL (remove fragment)
                    full_url = full_url.split('#')[0]
                    
                    # Only follow links to same domain
                    if urlparse(full_url).netloc == start_domain:
                        if full_url not in visited and full_url not in queue:
                            queue.append(full_url)
                            
    return found_pages

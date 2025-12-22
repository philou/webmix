import os
from bs4 import BeautifulSoup
import sys

def convert_html_sitemap_to_xml(html_path: str, output_path: str, base_url: str = "http://treatcfsfm.org/"):
    """
    Converts the specific sitemap.php.html from treatcfsfm.org to a standard sitemap.xml.
    Preserves the order of links as they appear in the HTML (which represents the hierarchy).
    """
    if not os.path.exists(html_path):
        print(f"Error: Input file not found: {html_path}")
        return

    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # The sitemap links are inside divs with classes sitemap_link1, sitemap_link2, sitemap_link3
    # We want to extract them in order.
    # Since they are nested in the DOM, a simple find_all on the container or just traversing 
    # the 'sitemap_menu' class cell should work.
    
    # Find the main container
    container = soup.find(class_="sitemap_menu")
    if not container:
        print("Error: Could not find element with class 'sitemap_menu'")
        return

    urls = []
    
    # We can just find all 'a' tags within the container. 
    # BeautifulSoup's find_all returns elements in document order.
    # We need to filter out links that might not be part of the sitemap structure if any,
    # but looking at the HTML, the container seems to only have the sitemap links.
    
    for a_tag in container.find_all('a'):
        href = a_tag.get('href')
        if href:
            # Clean up href
            href = href.strip()
            if not href.startswith('http'):
                # Handle relative links
                # Ensure we don't double slash
                if base_url.endswith('/') and href.startswith('/'):
                    full_url = base_url + href[1:]
                elif not base_url.endswith('/') and not href.startswith('/'):
                    full_url = base_url + '/' + href
                else:
                    full_url = base_url + href
            else:
                full_url = href
            
            # Avoid duplicates if any (though sitemap usually lists unique pages, 
            # sometimes the same page is linked twice? In a tree structure, usually not).
            # But let's keep them as is to preserve structure/order.
            urls.append(full_url)

    # Generate XML
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for url in urls:
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{url}</loc>')
        xml_content.append('  </url>')
    
    xml_content.append('</urlset>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_content))
    
    print(f"Successfully generated sitemap.xml with {len(urls)} URLs at {output_path}")

if __name__ == "__main__":
    # Default paths based on the project structure
    # Assuming script is run from project root or scripts/ folder
    
    # Try to locate the file relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    input_file = os.path.join(project_root, "tests/data/sample_site/treatcfsfm.org/sitemap.php.html")
    output_file = os.path.join(project_root, "tests/data/sample_site/treatcfsfm.org/sitemap.xml")
    
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
        
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    
    convert_html_sitemap_to_xml(input_file, output_file)

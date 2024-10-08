import json
import re

def load_ecommerce_urls():
    with open('ecommerce_urls.json', 'r') as f:
        return json.load(f)

def load_picture_names():
    with open('picture_name.json', 'r') as f:
        return json.load(f)

def normalize_name(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

def match_screenshots(ecommerce_data, picture_data):
    for site in ecommerce_data:
        site_name = normalize_name(site['title'])
        site['screenshots'] = []
        
        for entry in picture_data:
            for name in entry['filenames']:
                normalized_name = normalize_name(name)
                if site_name in normalized_name and 'screenshot' in normalized_name:
                    site['screenshots'].append(name)
        
        print(f"Matched {len(site['screenshots'])} screenshots for {site['title']}")
    return ecommerce_data

def save_updated_ecommerce_urls(data):
    with open('ecommerce_urls.json', 'w') as f:
        json.dump(data, f, indent=4)

def main():
    ecommerce_data = load_ecommerce_urls()
    picture_data = load_picture_names()
    updated_data = match_screenshots(ecommerce_data, picture_data)
    save_updated_ecommerce_urls(updated_data)
    print("ecommerce_urls.json has been updated with matched screenshots.")

if __name__ == "__main__":
    main()

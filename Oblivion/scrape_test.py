from playwright.sync_api import sync_playwright
import json
import time


BASE = "https://www.elderstats.com"


# Parse attributes from text

def parse_class(text): 
    classes = {}
    key = ["class"]
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for i in range(len(lines) - 1):
        if lines[i].lower() == "class": 
             classes["className"] = lines[i + 1] 

    return classes


def parse_attributes(text):
    stats = {}
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    keys = ["Strength", "Intelligence", "Willpower",
            "Agility", "Speed", "Endurance",
            "Personality", "Luck"]

    for i in range(len(lines)):
        if lines[i] in keys:
            try:
                stats[lines[i]] = int(lines[i + 1])
            except:
                pass

    return stats


# Scrape one character
def scrape_character(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("#profile_body")

    # click overview then attributes
    overview_text = page.inner_text("#profile_body")
    page.click(".obnav_attributes")
    page.wait_for_timeout(500)
    
    attributes_text = page.inner_text("#profile_body")

    return {
        "url": url,
        "class": parse_class(overview_text),
        "attributes": parse_attributes(attributes_text)
    }

# Get character links
def get_character_urls(page, limit=100):
    urls = []

    for page_num in range(1, 4):  
        url = f"https://www.elderstats.com/stats/db/oblivion?page={page_num}"
        print("Visiting", url)

        page.goto(url, wait_until="domcontentloaded")


        links = page.query_selector_all("a[href*='/character/']")

        for a in links:
            href = a.get_attribute("href")
            if href and "/character/" in href:
                full = BASE + href
                if full not in urls:
                    urls.append(full)

    return urls[:limit]

def main():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Collecting character URLs...")
        urls = get_character_urls(page, limit=100)
        print(f"Found {len(urls)} characters")

        for i, url in enumerate(urls):
            try:
                print(f"[{i+1}/{len(urls)}] Scraping {url}")

                data = scrape_character(page, url)
                results.append(data)

                time.sleep(2)  

            except Exception as e:
                print("FAILED:", url, e)

        browser.close()

    # save output
    with open("oblivion_characters.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Done → saved to oblivion_characters.json")


if __name__ == "__main__":
    main()
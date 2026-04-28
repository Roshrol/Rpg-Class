from playwright.sync_api import sync_playwright
import json
import csv
import time


BASE = "https://www.elderstats.com"


# Parse attributes from text

def parse_class(text): 
    allowed_Classes = {"Acrobat", "Agent", "Archer", "Assassin", 
    "Barbarian", "Bard", "Battlemage", "Crusader", "Healer", "Knight", "Mage", "Monk", 
    "Nightblade", "Pilgrim", "Rogue", "Scout", "Sorcerer", "Spellsword", "Thief", "Warrior", "Witchhunter"}

    classes = {}
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for i in range(len(lines) - 1):
        if lines[i].lower() == "class":
            next_val = lines[i + 1]
            if next_val in allowed_Classes:
                classes["className"] = next_val

    return classes

def parse_skills(text):
    allowed_Skills = ["Armorer",  "Athletics", "Blade", "Block", "Blunt", "Hand to Hand", "Heavy Armor",
    "Alchemy", "Alteration", "Conjuration", "Destruction", "Illusion", "Mysticism", 
    "Restoration", "Acrobatics", "Light Armor", "Marksman", "Mercantile", "Security", "Sneak", "Speechcraft"]
    skills = {}
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for i in range(len(lines) - 1):
        if lines[i] in allowed_Skills:
            try:
                value = int(lines[i + 1])
                skills[lines[i]] = value
            except:
                continue

    return skills


def parse_attributes(text):
    stats = {}
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    keys = ["Strength", "Intelligence", "Willpower",
            "Agility", "Speed", "Endurance",
            "Personality", "Luck"]

    for i in range(len(lines) - 1):
        if lines[i] in keys:
            try:
                value = int(lines[i + 1])
                if value != 0 and value != 255:
                    stats[lines[i]] = value
            except:
                continue

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
    
    page.click(".obnav_skills")
    page.wait_for_timeout(500)
    skills_text = page.inner_text("#profile_body")
    

    required_Keys = {
    "Strength", "Intelligence", "Willpower",
    "Agility", "Speed", "Endurance",
    "Personality", "Luck"
}

    character = {
    "url": url,
    "class": parse_class(overview_text),
    "attributes": parse_attributes(attributes_text),
    "skills": parse_skills(skills_text)
}

    if not character["class"]:
        return None

    attributes = character["attributes"]

    if not attributes:
        return None

    if not required_Keys.issubset(attributes.keys()):
        return None

    return character

# Get character links
def get_character_urls(page, limit=1000):
    urls = []

    for page_num in range(1, 73):  
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

    return urls

def main():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Collecting character URLs...")
        urls = get_character_urls(page)
        print(f"Found {len(urls)} characters")

        for url in urls:
            try:
                print(f"Scraping {url}")

                data = scrape_character(page, url)
                if data == None:
                    continue

                results.append(data)
                if len(results) >= 1000:
                    break

                time.sleep(2)  

            except Exception as e:
                print("FAILED:", url, e)

        browser.close()

    # save output
        with open("oblivion_characters.csv", "w", newline="") as f:
            writer = csv.writer(f)

            skill_columns = [
                "Armorer", "Athletics", "Blade", "Block", "Blunt",
                "Hand to Hand", "Heavy Armor", "Alchemy", "Alteration",
                "Conjuration", "Destruction", "Illusion", "Mysticism",
                "Restoration", "Acrobatics", "Light Armor", "Marksman",
                "Mercantile", "Security", "Sneak", "Speechcraft"
            ]

            attribute_columns = [            
                "Strength", "Intelligence", "Willpower",
                "Agility", "Speed", "Endurance",
                "Personality", "Luck"
            ]

            writer.writerow(["url", "class"] + skill_columns + attribute_columns)

            for r in results:
                if not r:
                    continue

                attrs = r["attributes"]
                skills = r["skills"]

                writer.writerow([r["url"], r["class"].get("className", "")] + 
                [skills.get(skill, "") for skill in skill_columns] + 
                [attrs.get("Strength", "") for attr in  attribute_columns])

if __name__ == "__main__":
    main()
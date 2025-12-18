"""
SEO Smart Form Filler
---------------------------------
A Selenium-based smart form autofill engine
for SEO directory and backlink submissions.

⚠️ This version uses FAKE / SAMPLE data.
Do NOT store real credentials in public repositories.
"""

from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# ======================================================
# SAMPLE DATA (SAFE FOR PUBLIC REPOSITORIES)
# ======================================================

DATA = {
    # Account
    "username": "sample_user_123",
    "first_name": "John",
    "last_name": "Doe",
    "login_email": "john.doe@example.com",
    "password": "SamplePassword@123",

    # Business identity
    "business_name": "Sample Appliance Store",
    "category": "Appliance Store",

    # Location
    "country": "Canada",
    "province": "Ontario",
    "city": "Toronto",
    "address": "123 Sample Street",
    "postal_code": "A1A1A1",
    "phone": "123-456-7890",

    # Online
    "website": "https://www.example.com",
    "business_email": "contact@example.com",

    # SEO description
    "description": (
        "Sample Appliance Store offers home appliances and parts "
        "with professional installation and customer support."
    ),

    # Social profiles
    "facebook": "https://www.facebook.com/example",
    "instagram": "https://www.instagram.com/example",
    "youtube": "https://www.youtube.com/@example"
}

# ======================================================
# FIELD MAP (SMART ALIAS MATCHING)
# ======================================================

FIELD_MAP = {
    # Personal
    "first_name": ["first name", "fname", "given name"],
    "last_name": ["last name", "lname", "surname"],

    # Account
    "username": ["username", "user name"],
    "login_email": ["email", "e-mail"],
    "password": ["password"],
    "confirm_password": ["confirm password", "re-enter", "verify password"],

    # Business
    "business_name": [
        "business name", "company", "company name",
        "organization", "listing title", "listing name"
    ],

    # Category
    "category": ["category", "categories", "business type"],

    # Address
    "address": ["address", "street"],
    "city": ["city", "locality"],
    "province": ["province", "state", "region"],
    "country": ["country"],
    "postal_code": ["postal", "zip", "postcode"],

    # Contact
    "phone": ["phone", "telephone", "tel"],
    "business_email": ["business email", "contact email"],

    # Web
    "website": ["website", "url"],

    # Description
    "description": ["description", "about", "details"],

    # Social
    "facebook": ["facebook"],
    "instagram": ["instagram"],
    "youtube": ["youtube"]
}

# ======================================================
# HELPER FUNCTIONS
# ======================================================

def similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def match_key(meta: str):
    """
    Match input metadata (name, id, placeholder, aria-label)
    to a DATA key using FIELD_MAP.
    """
    meta = meta.lower()

    # Priority rule: email fields map to login_email
    if "email" in meta:
        return "login_email"

    for key, keywords in FIELD_MAP.items():
        for kw in keywords:
            if kw in meta:
                return key

    return None

# ======================================================
# SMART FILL ENGINE
# ======================================================

def smart_fill(driver):
    print("\n[INFO] Smart Fill Started")

    elements = driver.find_elements(By.XPATH, "//input | //textarea | //select")

    for element in elements:
        try:
            tag = element.tag_name.lower()

            meta = " ".join([
                element.get_attribute("name") or "",
                element.get_attribute("id") or "",
                element.get_attribute("placeholder") or "",
                element.get_attribute("aria-label") or ""
            ])

            key = match_key(meta)
            if not key:
                continue

            value = DATA["password"] if key == "confirm_password" else DATA.get(key)
            if not value:
                continue

            # Handle dropdowns
            if tag == "select":
                select = Select(element)
                for option in select.options:
                    if similarity(option.text, value) > 0.6:
                        select.select_by_visible_text(option.text)
                        print(f"[FILLED] Dropdown → {key}")
                        break

            # Handle input / textarea
            else:
                input_type = element.get_attribute("type") or ""

                if input_type == "password":
                    driver.execute_script(
                        "arguments[0].value = arguments[1];",
                        element,
                        value
                    )
                    print(f"[FILLED] {key} (password)")
                else:
                    element.clear()
                    element.send_keys(value)
                    print(f"[FILLED] {key}")

        except Exception:
            # Ignore fields that cannot be interacted with
            pass

    print("[INFO] Smart Fill Completed\n")

# ======================================================
# MAIN — MANUAL NAVIGATION MODE
# ======================================================

def main():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    print("""
=================================================
MANUAL MODE ENABLED
-------------------------------------------------
1. Browser is open
2. Navigate to any form page
3. Login / solve CAPTCHA manually
4. When the form is ready, type:
   → fill
5. Type 'exit' to close
=================================================
""")

    while True:
        command = input("Command (fill / exit): ").strip().lower()

        if command == "fill":
            smart_fill(driver)
        elif command == "exit":
            break

    driver.quit()


if __name__ == "__main__":
    main()

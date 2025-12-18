# SEO Smart Form Filler 🤖

A Selenium-based smart form autofill engine designed to automate SEO directory
and backlink submission workflows.

---

## 🚀 Why This Project Exists

SEO professionals often spend hours filling repetitive forms across
business directories, citation websites, and backlink platforms.

This project reduces that manual effort by intelligently detecting
and filling form fields using a flexible matching system.

---

## ✨ Key Features

- Smart field detection using:
  - `name`
  - `id`
  - `placeholder`
  - `aria-label`
- Supports:
  - Input fields
  - Textareas
  - Dropdowns (select elements)
- Similarity-based matching using `difflib`
- Manual CAPTCHA-safe workflow
- Centralized and configurable data structure

---

## 🛠️ Tech Stack

- Python
- Selenium WebDriver
- difflib (SequenceMatcher)

---

## ⚙️ How It Works

1. Launches a Chrome browser session
2. User manually navigates to any form page
3. Login and CAPTCHA are handled manually
4. User types `fill` in the terminal
5. Script automatically fills detected form fields

---

## 📂 Project Structure

```text
seo-smart-form-filler/
│
├── smart_form_filler.py   # Main automation script
├── README.md              # Project documentation
├── LICENSE                # MIT License
└── .gitignore             # Python ignore rules


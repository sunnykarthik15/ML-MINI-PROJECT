import os
import time
from playwright.sync_api import sync_playwright

os.makedirs("reports/screenshots", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1366, "height": 950})
    page.goto("http://localhost:8501", wait_until="networkidle")
    page.wait_for_selector(".main-header", timeout=15000)
    time.sleep(2)

    # Click Tab 0: Model Explanations
    tabs = page.locator('[data-testid="stTab"]')
    print("Found tabs count:", tabs.count())
    if tabs.count() >= 3:
        tabs.nth(0).click()
        time.sleep(2)
        page.screenshot(path="reports/screenshots/04_model_explanations.png")
        print("Saved 04_model_explanations.png")

        tabs.nth(1).click()
        time.sleep(2)
        page.screenshot(path="reports/screenshots/05_model_comparison_and_cm.png")
        print("Saved 05_model_comparison_and_cm.png")

        tabs.nth(2).click()
        time.sleep(2)
        page.screenshot(path="reports/screenshots/06_eda_visualizations.png")
        print("Saved 06_eda_visualizations.png")

    # Also capture token preview expander from real prediction
    page.get_by_role("button", name="📄 Load Real News Example").click()
    time.sleep(1)
    page.get_by_role("button", name="🔍 Classify Article").click()
    time.sleep(2)
    # Click expander
    expander = page.locator("summary:has-text('View Preprocessed NLP Tokens')")
    if expander.count() > 0:
        expander.click()
        time.sleep(1)
    page.screenshot(path="reports/screenshots/07_nlp_tokens_inspection.png")
    print("Saved 07_nlp_tokens_inspection.png")

    browser.close()

print("All screenshots successfully captured!")

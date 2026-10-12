import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    url = 'http://localhost:3000/view?path=C%3A%5CUsers%5Cbilal%5COneDrive+-+BTH+Student%5CCanvas+Kurser%5CSoftware+architecture%5CAssigment+nr+2%5CAssigment+2%5Cclick-repo'
    print('Navigating to Git Truck...')
    page.goto(url, wait_until='networkidle')
    # wait for visualization to render
    time.sleep(6)
    page.screenshot(path='analysis/gittruck_overview.png', full_page=False)
    print('Saved analysis/gittruck_overview.png')
    
    # Let's see if we can find author breakdown or options
    page.screenshot(path='analysis/gittruck_authors.png')
    print('Saved analysis/gittruck_authors.png')
    browser.close()

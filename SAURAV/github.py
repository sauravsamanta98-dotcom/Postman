print("*********Welcome TO MACK ********")

A = input("enter User ID:")
B = input("enter Password:")

from multiprocessing import context

import playwright
from playwright.sync_api import Page

url = "https://macktesting.solverminds.net/"
def run(page: Page):
    page.goto(url)
    page.locator("#username").fill(A)
    page.locator("#password").fill(B)
    page.locator("#kc-login").click()
    context.close()
    browser.close()

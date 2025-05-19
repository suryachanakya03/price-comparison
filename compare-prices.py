from flask import Flask, send_file, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


app = Flask(__name__)

CHROME_DRIVER_PATH = r"C:\Users\surya\Documents\price comparison\chromedriver.exe"

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

def get_price_amazon(product):
    driver = setup_driver()
    driver.get(f"https://www.amazon.in/s?k={product.replace(' ', '+')}")
    
    price = "N/A"
    try:
        # Wait for the price element to be present
        price_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-price-whole"))
        )
        price = price_elem.text.replace(",", "").strip()
    except Exception:
        pass

    driver.quit()
    return price

def get_price_flipkart(product):
    driver = setup_driver()
    driver.get(f"https://www.flipkart.com/search?q={product.replace(' ', '+')}")
    
    # Close login popup if it appears
    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
        )
        close_btn.click()
    except Exception:
        pass

    price = "N/A"
    try:
        # Wait for the price element with your provided class
        price_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Nx9bqj._4b5DiR"))
        )
        price = price_elem.text.replace("₹", "").replace(",", "").strip()
    except Exception:
        pass

    driver.quit()
    return price

def get_price_croma(product):
    driver = setup_driver()
    driver.get(f"https://www.croma.com/search/?text={product.replace(' ', '%20')}")

    price = "N/A"
    try:
        # Wait for the price element to be present
        price_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.amount"))
        )
        price = price_elem.text.replace("₹", "").replace(",", "").strip()
    except Exception:
        pass

    driver.quit()
    return price

@app.route("/")
def index():
    return send_file("index.html")

@app.route('/compare.css')
def css():
    return send_file('compare.css')

@app.route('/compare.js')
def js():
    return send_file('compare.js')

@app.route("/get-prices")
def get_prices():
    product = request.args.get("product", "")
    amazon = get_price_amazon(product)
    flipkart = get_price_flipkart(product)
    croma = get_price_croma(product)
    return jsonify({
        "amazon": amazon,
        "flipkart": flipkart,
        "croma": croma
    })

if __name__ == "__main__":
    app.run(debug=True)

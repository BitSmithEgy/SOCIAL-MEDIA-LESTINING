from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyperclip 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cred import FACEBOOK_EMAIL, FACEBOOK_PASSWORD
import csv

MESSAGE = """
 _____ _    ____ _____ ____   ___   ___  _  __
|  ___/ \  / ___| ____| __ ) / _ \ / _ \| |/ /
| |_ / _ \| |   |  _| |  _ \| | | | | | | ' / 
|  _/ ___ \ |___| |___| |_) | |_| | |_| | . \ 
|_|/_/   \_\____|_____|____/ \___/ \___/|_|\_\\
                                              
 ____   ____ ____      _    ____  _____ ____  
/ ___| / ___|  _ \    / \  |  _ \| ____|  _ \ 
\___ \| |   | |_) |  / _ \ | |_) |  _| | |_) |
 ___) | |___|  _ <  / ___ \|  __/| |___|  _ < 
|____/ \____|_| \_\/_/   \_\_|   |_____|_| \_\\
"""




def main(FACEBOOK_EMAIL, FACEBOOK_PASSWORD, KEYWORD, MAXPOSTS):
    csv_file = f"{KEYWORD}_posts.csv"
    driver = webdriver.Firefox()
    try:
        driver.get("https://www.facebook.com")
        time.sleep(3)

        driver.find_element(By.ID, "email").send_keys(FACEBOOK_EMAIL)
        time.sleep(3)
        driver.find_element(By.ID, "pass").send_keys(FACEBOOK_PASSWORD)
        time.sleep(3)
        driver.find_element(By.ID, "pass").send_keys(Keys.RETURN)
        time.sleep(10)

        search_url = f"https://www.facebook.com/search/posts/?q={KEYWORD}"
        driver.get(search_url)
        time.sleep(5)

        for _ in range(MAXPOSTS):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        posts = driver.find_elements(By.XPATH, "//div[@aria-posinset]")[:MAXPOSTS]

        data = []
        for post in posts:
            try:
                post_text_element = post.find_element(By.XPATH, ".//div[contains(@dir, 'auto')]")
                post_text = post_text_element.text if post_text_element else "Text not found"
            except:
                post_text = "Text not found"

            try:
                see_more = post.find_element(By.XPATH, ".//div[contains(text(), 'See more')]")
                if see_more:
                    driver.execute_script("arguments[0].click();", see_more)
                    time.sleep(4)
                    post_text_element = post.find_element(By.XPATH, ".//div[contains(@dir, 'auto')]")
                    post_text = post_text_element.text if post_text_element else "Text not found"
            except:
                pass
            
            try:
                share = post.find_element(By.XPATH, ".//div[@class='xabvvm4 xeyy32k x1ia1hqs x1a2w583 x6ikm8r x10wlt62']")
                share = share.find_element(By.XPATH, ".//div[@class='xq8finb x16n37ib']")
                share = share.find_element(By.XPATH, ".//div[@class='x9f619 x1ja2u2z x78zum5 x2lah0s x1n2onr6 x1qughib x1qjc9v5 xozqiw3 x1q0g3np xjkvuk6 x1iorvi4 xwrv7xz x8182xy x4cne27 xifccgj']")
                share = share.find_elements(By.XPATH, ".//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xg83lxy x1h0ha7o x10b6aqq x1yrsyyn']")[-1]

                share.click()

                copy_link = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Copy link')]"))
                )
                copy_link.click()
                time.sleep(4)
                share_link = pyperclip.paste()
            except:
                share_link = "Share link not found"

            post_Data = {
                "post_text": post_text,
                "share_link": share_link
            }
            data.append(post_Data)

        

        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["post_text", "share_link"])
            
            writer.writeheader()
            
            writer.writerows(data)

        print(f"Data saved to {csv_file}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()


if __name__:
    print(MESSAGE)
    print('--------------------------------------------------------------------')
    KEYWORD = input('Enter The keyword: ')
    print('--------------------------------------------------------------------')
    try:
        MAXPOSTS = int(input('Enter The max posts number: '))
        main(FACEBOOK_EMAIL, FACEBOOK_PASSWORD, KEYWORD, MAXPOSTS)
    except ValueError:
        print('Please enter a valid number for max posts number (int only)')
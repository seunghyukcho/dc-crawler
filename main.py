import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome("/Users/user/chromedriver/chromedriver", options=options)
    # driver.implicitly_wait(3)

    for page in range(1, 10):
        driver.get(f"https://gall.dcinside.com/board/view/?id=leagueoflegends3&no={page}")
        try:
            driver.find_element_by_class_name("delet")
        except NoSuchElementException:
            pass
        else:
            print(f"page #{page} not found")
            continue

        try:
            n_comments = driver.find_element_by_class_name("cmt_paging")
            n_comments = n_comments.find_elements_by_tag_name('a')
            last_comment_page = len(n_comments) + 1

            title = driver.find_element_by_class_name("title_subject")
            content = driver.find_element_by_class_name("writing_view_box")

            for i in range(last_comment_page + 1, 0, -1):
                driver.execute_script(f"viewComments({i}, 'D')")
                comments = driver.find_elements_by_class_name("usertxt")
        except NoSuchElementException:
            page -= 1

    driver.quit()

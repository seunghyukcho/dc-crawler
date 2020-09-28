from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from .exception import *


class Crawler:
    def __init__(self, driver, timeout=60, retry=True):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")

        self.retry = retry
        self.driver = webdriver.Chrome(driver, options=options)
        self.driver.set_page_load_timeout(timeout)

    def crawl(self, gallery, idx):
        while True:
            try:
                self.driver.get(f"https://gall.dcinside.com/board/view/?id={gallery}&no={idx}")

                try:
                    self.driver.find_element_by_class_name("delet")
                except NoSuchElementException:
                    pass
                else:
                    raise DeletedPostException

                comments = []
                try:
                    n_comments = self.driver.find_element_by_class_name("cmt_paging")
                    n_comments = n_comments.find_elements_by_tag_name("a")
                    last_comment_page = len(n_comments) + 1
                except NoSuchElementException:
                    last_comment_page = 0

                title = self.driver.find_element_by_class_name("title_subject")
                content = self.driver.find_element_by_class_name("writing_view_box")
                content = content.find_elements_by_tag_name("div")
                content = content[-1]

                for i in range(last_comment_page, 0, -1):
                    self.driver.execute_script(f"viewComments({i}, 'D')")
                    page_comments = self.driver.find_elements_by_class_name("usertxt")
                    for comment in page_comments:
                        comments.append(comment.text)

                return {
                    "title": title.text,
                    "content": content.text,
                    "comments": comments
                }

            except DeletedPostException:
                raise DeletedPostException

            except (NoSuchElementException, TimeoutException):
                if not self.retry:
                    raise ServerException

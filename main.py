import logging
from tap import Tap
from tqdm import tqdm
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class ArgumentParser(Tap):
    save_to: str  # Path to output file
    log_to: str = "log.txt"  # Path to log file
    gallery: str  # Name of gallery (etc. leagueoflegends3)
    start_idx: int = 1  # Start index of gallery page
    end_idx: int  # End index of gallery page
    chrome_driver: str  # Path to chrome driver

    
if __name__ == "__main__":
    args = ArgumentParser().parse_args()

    logging.basicConfig(filename=args.log_to, format="%(asctime)s %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
    save_file = open(args.save_to, 'a')

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(args.chrome_driver, options=options)
    driver.implicitly_wait(5)

    for page_idx in tqdm(range(args.start_idx, args.end_idx + 1)):
        while True:
            try:
                driver.get(f"https://gall.dcinside.com/board/view/?id={args.gallery}&no={page_idx}")

                try:
                    driver.find_element_by_class_name("delet")
                except NoSuchElementException:
                    pass
                else:
                    break

                comments = []
                n_comments = driver.find_element_by_class_name("cmt_paging")
                n_comments = n_comments.find_elements_by_tag_name("a")
                last_comment_page = len(n_comments) + 1

                title = driver.find_element_by_class_name("title_subject")
                content = driver.find_element_by_class_name("writing_view_box")
                content = content.find_elements_by_tag_name("div")
                content = content[-1]

                for i in range(last_comment_page, 0, -1):
                    driver.execute_script(f"viewComments({i}, 'D')")
                    page_comments = driver.find_elements_by_class_name("usertxt")
                    for comment in page_comments:
                        comments.append(comment.text)

                save_file.write(title.text + '\n')
                save_file.write(content.text.replace('\n', ' ') + '\n')
                for comment in comments:
                    save_file.write(comment + '\n')
                save_file.write("\n\n\n")
            except (NoSuchElementException, TimeoutException):
                logging.warning(f"Page #{page_idx} reloading...")
            else:
                break

    save_file.close()
    driver.quit()

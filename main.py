from tap import Tap
from tqdm import tqdm
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ArgumentParser(Tap):
    save_to: str  # Path to output file
    gallery: str  # Name of gallery (etc. leagueoflegends3)
    start_idx: int = 1  # Start index of gallery page
    end_idx: int  # End index of gallery page
    chrome_driver: str  # Path to chrome driver


if __name__ == "__main__":
    args = ArgumentParser().parse_args()

    log_file = open(args.save_to, 'w')

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(args.chrome_driver, options=options)

    for page_idx in tqdm(range(args.start_idx, args.end_idx + 1)):
        driver.get(f"https://gall.dcinside.com/board/view/?id={args.gallery}&no={page_idx}")
        try:
            driver.find_element_by_class_name("delet")
        except NoSuchElementException:
            pass
        else:
            continue

        try:
            n_comments = driver.find_element_by_class_name("cmt_paging")
            n_comments = n_comments.find_elements_by_tag_name('a')
            last_comment_page = len(n_comments) + 1

            title = driver.find_element_by_class_name("title_subject")
            content = driver.find_element_by_class_name("writing_view_box")
            content = content.find_elements_by_tag_name('div')
            content = content[-1]

            log_file.write(title.text + '\n')
            log_file.write(content.text.replace('\n', ' ') + '\n')

            for i in range(last_comment_page + 1, 0, -1):
                driver.execute_script(f"viewComments({i}, 'D')")
                comments = driver.find_elements_by_class_name("usertxt")
                for comment in comments:
                    log_file.write(comment.text + '\n')
            log_file.write("\n\n\n")
        except NoSuchElementException:
            page_idx -= 1

    log_file.close()
    driver.quit()

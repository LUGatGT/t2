#!/usr/bin/env python
from selenium import webdriver
import selenium
import os,sys
import json

def create_driver():
    dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87"
    try:
        phantom = webdriver.PhantomJS(desired_capabilities=dcap, service_log_path=config().phantomjs_logfile)
    except selenium.common.exceptions.WebDriverException as e:
        print("Please install phantomjs for this script to work.")
        sys.exit(1)
    return phantom


class config():
    # TODO Eliminate the need for this global state
    # Currently used determining --no-cache is set
    # http://code.activestate.com/recipes/66531/
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        t2_dir = os.path.join(os.path.expanduser('~'), '.t2')
        self.cache_dir = t2_dir
        self.config_dir = t2_dir
        self.crash_dir = os.path.join(t2_dir, 'crashes')
        self.phantomjs_logfile = os.path.join(t2_dir, 'ghostdriver.log')

        self.username_file = os.path.join(self.config_dir, 'username')
        self.password_file = os.path.join(self.config_dir, 'password')

        self.course_cache = os.path.join(self.cache_dir, 'courses')
        self.cookie_file = os.path.join(self.cache_dir, 'cookies')

class T2():
    def __init__(self):
        self.config = config()
        self.driver = create_driver()
        self.driver.implicitly_wait(30)
        self.base_url = "https://t-square.gatech.edu/"
        self.logged_in = False


    def close(self):
        self.driver.quit()
    

    def login(self, user=None, password=None):
        driver = self.driver
        if self.logged_in:
            return

        if self.config.cache and os.path.exists(self.config.cookie_file):
            f = open(self.config.cookie_file)
            cookies = json.load(f)
            f.close()
            driver.get(self.base_url) # Try this if it doesn't work
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            return

        if not user:
            user = open(self.config.username_file).read().strip()
        if not password:
            password = open(self.config.password_file).read().strip()
        driver.get(self.base_url + "/portal")
        driver.find_element_by_id("loginLink1").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(user)
        driver.find_element_by_name("submit").click()
        self.logged_in = True
        if self.config.cache:
            f = open(self.config.cookie_file, "w")
            json.dump(driver.get_cookies(), f)
            f.close()


    def list_courses(self):
        driver = self.driver
        driver.get(self.base_url + "/portal")
        courses = [link.get_attribute('title') for link in driver.find_element_by_id("siteLinkList").find_elements_by_css_selector('li > a')]
        return courses


    def list_assignments(self, course_name):
        driver = self.driver
        driver.get(self.base_url + "/portal")
        driver.find_element_by_css_selector('a[title="' + course_name + '"] > span').click()
        driver.find_element_by_link_text("Assignments").click()
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe").get_attribute('id'))
        return [a.text for a in driver.find_element_by_tag_name('table').find_elements_by_css_selector('td[headers="title"] > h4 > a')]


    def upload_files_to_assignment(self, course_name, assignment_name, files, remove_old=True):
        driver = self.driver
        driver.get(self.base_url + "/portal")
        driver.find_element_by_css_selector('a[title="' + course_name + '"] > span').click()
        driver.find_element_by_link_text("Assignments").click()
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe").get_attribute('id'))
        driver.find_element_by_link_text(assignment_name).click()

        if remove_old:
            pass

        for f in files:
            driver.find_element_by_name("upload").send_keys(os.path.abspath(f))

        #driver.find_element_by_id("Assignment.view_submission_honor_pledge_yes").click()
        driver.find_element_by_name("post").click()
        driver.save_screenshot('proof.png')

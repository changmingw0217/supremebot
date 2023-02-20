from selenium import webdriver
from imagetyperzapi3 import imagetyperzapi
from twocaptcha import TwoCaptcha
import time
import json


class SupremeBot(object):

    def __init__(self):
        self.driver = webdriver.Chrome("/Users/changmingwang/Downloads/chromedriver")
        # url = 'https://www.google.com/accounts/Login'
        # self.driver.get(url)
        # time.sleep(30)
        self.driver.get("https://www.supremenewyork.com/shop/all/sweatshirts")
        self.twoCaptcha = TwoCaptcha("3a4df793276e4651aa44ad4a9de61907")
        self.url = "https://www.supremenewyork.com/checkout"
        self.site_key = "6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz"
        self.token = self.solve_captcha()

    def __key_word_compare(self, name, key_words_list):
        for key in key_words_list:
            if key not in name:
                return False
        return True

    def __find_product(self, key_words_list):
        product_list = self.driver.find_elements_by_class_name("product-name")
        link_list = []
        for item in product_list:
            element = item.find_element_by_class_name("name-link")
            name = element.text.lower()
            if self.__key_word_compare(name, key_words_list):
                link_list.append(element.get_attribute("href"))

        return link_list

    def __find_color_link(self, link_list, color):
        product_style = self.driver.find_elements_by_class_name("product-style")
        # result = []
        for item in product_style:
            element = item.find_element_by_class_name("name-link")
            element_color = element.text.lower()

            link = element.get_attribute("href")

            if (color in element_color) and (link in link_list):
                # result.append(link)
                return link

    # return result

    def __select_size(self, size):
        # select = self.driver.find_element_by_id("s")
        select = self.driver.find_element_by_css_selector("[aria-labelledby=size-select]")
        for option in select.find_elements_by_tag_name("option"):
            if option.text == size:
                option.click()
                break

    def __add_to_cart(self):
        x_path = '//input[@type="submit" and @name="commit"]'
        self.driver.find_element_by_xpath(x_path).click()
        time.sleep(1)

    def __fill_infos(self):
        action = webdriver.ActionChains(self.driver)
        name_x_path = '//input[@placeholder="name"]'
        name = self.driver.find_element_by_xpath(name_x_path)
        action.move_to_element(name)
        action.click(name)
        name.send_keys("mike li")
        email_x_path = '//input[@placeholder="email"]'
        email = self.driver.find_element_by_xpath(email_x_path)
        action.move_to_element(email)
        action.click(email)
        email.send_keys("hahamikeli@gmail.com")
        tel_x_path = '//input[@placeholder="tel"]'
        tel = self.driver.find_element_by_xpath(tel_x_path)
        action.move_to_element(tel)
        action.click(tel)
        tel.send_keys("9174567890")
        address_x_path = '//input[@placeholder="address"]'
        address = self.driver.find_element_by_xpath(address_x_path)
        action.move_to_element(address)
        action.click(address)
        address.send_keys("123 abc st")
        add2_x_path = '//input[@placeholder="apt, unit, etc"]'
        # add2 = self.driver.find_element_by_xpath(add2_x_path)
        # add2.send_keys("")
        zip_x_path = '//input[@placeholder="zip"]'
        zip_code = self.driver.find_element_by_xpath(zip_x_path)
        action.move_to_element(zip_code)
        action.click(zip_code)
        zip_code.send_keys("10001")
        # city_x_path = '//input[@placeholder="city"]'
        # city = self.driver.find_element_by_xpath(city_x_path)
        # city.send_keys("New York")
        # time.sleep(0.1)
        states = self.driver.find_element_by_id("order_billing_state")
        for option in states.find_elements_by_tag_name("option"):
            if option.text == "NY":
                option.click()
        cc_x_path = '//input[@placeholder="number"]'
        cc = self.driver.find_element_by_xpath(cc_x_path)
        action.move_to_element(cc)
        action.click(cc)
        cc.send_keys("4117735013089365")
        mouth = self.driver.find_element_by_id("credit_card_month")
        for option in mouth.find_elements_by_tag_name("option"):
            if option.text == "12":
                option.click()
        year = self.driver.find_element_by_id("credit_card_year")
        for option in year.find_elements_by_tag_name("option"):
            if option.text == "2024":
                option.click()
        cvv_x_path = '//input[@placeholder="CVV"]'
        cvv = self.driver.find_element_by_xpath(cvv_x_path)
        cvv.send_keys("123")
        term_x_path = '//label[@class="has-checkbox terms"]'
        term = self.driver.find_element_by_xpath(term_x_path)
        action.move_to_element(term)
        term.click()

        data_callback = self.driver.find_element_by_class_name('g-recaptcha').get_attribute('data-callback')
        js = '{}("{}");'.format(data_callback, self.token)
        # cookies = self.driver.get_cookies()
        # json_Cookies = json.dumps(cookies)
        # print(json_Cookies)
        time.sleep(3.5)
        self.driver.execute_script(js)

    def cop(self):
        links = self.__find_product(["cutout", "letters"])

        res_link = self.__find_color_link(links, "blue")
        self.driver.get(res_link)
        self.__select_size("Large")
        self.__add_to_cart()
        self.driver.get("https://www.supremenewyork.com/checkout")
        self.__fill_infos()

    def solve_captcha(self):
        start = time.clock()
        captcha_token = self.twoCaptcha.solve_captcha(site_key=self.site_key, page_url=self.url)
        end = time.clock()
        print(end - start)
        print(captcha_token)
        return captcha_token


if __name__ == "__main__":
    SupremeBot = SupremeBot()
    SupremeBot.cop()
    # SupremeBot.solve_captcha()

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import json
import requests
import logging

class maps_chrome_driver:
    def __init__(self):
        self.d = DesiredCapabilities.CHROME
        self.d['loggingPrefs'] = { 'performance':'ALL' }
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.maps_url = 'http://www.google.com/maps'
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s    %(levelname)-5.5s   %(message)s",
            handlers=[
                logging.FileHandler("qa_google_maps.log"),
                logging.StreamHandler()
        ])


    def is_google_maps_up(self):
    
        """ Description
        Method checks if Google maps site is up by checking status code.
        It is checking http status code by calling the one of the methods: get_http_status_selenium and get_http_status_requests.
        This two functions are doing the same - but using different Python libraries.
        In my example, I am using get_http_status_requests, but it can be changed with get_http_status_selenium, which will give the same result.
        """

        self.driver.get(self.maps_url)
        if self.get_http_status_requests() == 200:
            logging.info("Google maps site is up and running.")
            is_up = True
        else:
            logging.error("Google maps returned a status code other than 200, something is wrong! Aborting.")
            is_up = False
            self.driver.quit()
        return is_up

    def get_http_status_selenium(self):
    
        """ Description
        Method checks the status code from response using requests Python Selenium 
        """    
        try:
            response_content = self.driver.get_log('performance')
        except Exception as e:
            logging.error("There was an error connecting to the website ")
            logging.error(e)
            return None
        for response in response_content:
                response_msg = json.loads(response['message'])['message']
                if response_msg.get('params') != None:
                    response_msg_params =  response_msg['params']
                    if response_msg_params.get('response') != None:
                        response_msg_response = response_msg_params['response']
                        if response_msg_response.get('url') != None:
                            if response_msg_response['url'] == self.driver.current_url:
                                return (response_msg_response['status'])
                else: 
                    continue
        return None

    def get_http_status_requests(self):

        """ Description
        Method checks the status code from response using requests library from Python
        """
        try:
            response = requests.get(self.maps_url)
            return response.status_code
        except Exception as e:
            logging.error("There was an error connecting to the website ")
            logging.error(e)

    def check_path(self, path_from, path_to, check_details_page = True):
    
        """ Description
        :type path_from: string
        :param path_from: input path from which you want to travel
    
        :type path_to: string
        :param path_to: input path to which you want to travel
    
        :type check_details_page: boolean
        :param check_details_page: enables __are_time_and_distance_present function

        Method for finding the longest route from Budapest to Belgrade by car, and skipping the highways.
        """
        try:
            self.driver.find_element_by_class_name('searchbox-directions').click()
            logging.info("Going to page for choosing directions")
            wait = WebDriverWait(self.driver, 1000)
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "widget-pane-visible")))
            element_from = self.driver.find_element_by_xpath('//div[@id="sb_ifc51"]/input[@class="tactile-searchbox-input"]')
            element_from.send_keys(path_from)
            ActionChains(self.driver).move_to_element(element_from).click().perform()
            logging.info("Starting point is %s" %path_from)
        except NoSuchElementException as e:
            logging.error("There was an error finding element")
            logging.error(e)

        try:
            element_to = self.driver.find_element_by_xpath('//div[@id="sb_ifc52"]/input[@class="tactile-searchbox-input"]')
            element_to.send_keys(path_to)
            ActionChains(self.driver).move_to_element(element_to).click().perform()
            element_to.send_keys(Keys.ENTER)
            logging.info("Destination is %s" %path_to)
        except NoSuchElementException as e:
            logging.error("There was an error finding element")
            logging.error(e)
        
        try:
            self.driver.find_element_by_xpath('//*[@id="omnibox-directions"]/div/div[2]/div/div/div[1]/div[2]/button').click()
            wait = WebDriverWait(self.driver, 100)
            logging.info("Choosing directions for a car")
        except NoSuchElementException as e:
            logging.error("There was an error finding element")
            logging.error(e)
        except WebDriverException as e:
            logging.error("There was an error")
            logging.error(e)

        try:
            self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/button[2]').click()
            logging.info("Clicking options")
            element_highway_checkbox = self.driver.find_element_by_xpath('//*[@id="pane.directions-options-avoid-highways"]')
            ActionChains(self.driver).move_to_element(element_highway_checkbox).click().perform()
            logging.info("Checking option for avoiding highways")

            element_km = self.driver.find_element_by_xpath('//*[@id="pane.directions-options-units-km"]')
            ActionChains(self.driver).move_to_element(element_km).click().perform()
            logging.info("Checking option for displaying distance in kilometers")
        except NoSuchElementException as e:
            logging.error("There was an error finding element")
            logging.error(e)
        except WebDriverException as e:
            logging.error("There was an error")
            logging.error(e)

        wait = WebDriverWait(self.driver, 1000)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "section-directions-trip-distance")))

        try:
            direction_elements = self.driver.find_elements_by_class_name('section-directions-trip-distance')

            directions_dictionary = {}
            for direction_element in direction_elements:
                path_len_in_km = direction_element.find_element_by_tag_name("div").text.split(" ")[0] 
                directions_dictionary[direction_element] = path_len_in_km

            longest_direction = max(directions_dictionary, key = directions_dictionary.get)
            longest_direction.find_element_by_tag_name("div").click()
            logging.info("First click is showing warnings")
            longest_direction.find_element_by_tag_name("div").click()
            logging.info("Second click is showing details page")
            logging.info('Longest route: %s' %longest_direction.text)
        except NoSuchElementException as e:
            logging.error("There was an error finding element")
            logging.error(e)

        if check_details_page == True:
            if self.__are_time_and_distance_present():
                logging.info("Time and distance are present on the details page")
            else:
                logging.error("Time and distance are not present on the details page")
    

    def __are_time_and_distance_present(self):
    
        """ Description
        This is a private method that checks if time and distance parameters are present on details page.
        This method can be called with passing True/False argument.
        """    
        wait = WebDriverWait(self.driver, 1000)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[3]')))
        try:
            if self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[3]'):
                return True
            else:
                return False
        except NoSuchElementException as e:
            logging.error("There was an error finding element")
            logging.error(e)

if __name__ == '__main__':
    gmaps_test = maps_chrome_driver()
    gmaps_test.is_google_maps_up()
    gmaps_test.check_path("Budapest", "Belgrade", check_details_page = True)

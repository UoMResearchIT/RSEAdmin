from datetime import date, datetime
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.firefox.options import Options

import time
from rse.models import *
from rse.tests.test_random_data import random_project_and_allocation_data
from django.conf import settings

from django.contrib.auth import (
    SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY,
)

from django.contrib.sessions.backends.db import SessionStore

class TemplateTests(LiveServerTestCase):
    """
    Tests using Selenium to check for HTML and Log errors
    These are not proper view tests as they do not check the view logic but could be extended to do so!
    They do however test for the correct title response and as such will catch any view or permission errors
    """

    PAGE_TITLE_LOGIN = "RSE Group Administration Tool: Login Required"
    
    def setUp(self):
        """
        Setup the chrome driver for tests
        """
        super(TemplateTests, self).setUp()
        

        #generic options
        driver_options = Options()  
        driver_options.add_argument("--headless")

        # Setup chrome driver (currently replaced with gecko firefox driver)
        # driver_options.add_argument("--disable-gpu")
        # driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])   # suppress loggin message
        # d = DesiredCapabilities.CHROME
        # d['goog:loggingPrefs'] = { 'browser':'ALL' }
        # # start the chrome driver
        # self.selenium = webdriver.Chrome(chrome_options=driver_options, desired_capabilities=d)


        # setup firefox driver
        d = DesiredCapabilities.FIREFOX
        d['loggingPrefs'] = { 'browser':'ALL' }
        self.selenium = webdriver.Firefox(firefox_options=driver_options, desired_capabilities=d)

        # create test data
        random_project_and_allocation_data()

        # create an admin user
        user = User.objects.create_superuser(username='paul', email='admin@rseadmin.com', password='test', first_name="Paul", last_name="Richmond")

        # store some usefull user ids
        self.admin_user_id = user.id
        self.first_rse_id = RSE.objects.all()[0].id
        self.first_rse_user_id = RSE.objects.all()[0].user.id


        
    def tearDown(self):
        """
        Quit the chrome driver.
        There is a windows bug which gives a timeout!
        """

        # Bug with ConnectionResetError on Windows 10 non of the following Stack Overflow suggestions help!
        #self.selenium.implicitly_wait(10)
        #self.selenium.refresh()
        #time.sleep(30)
        self.selenium.quit()
        # Errors from the above call seem to only occur on Windows but do not prevent the tests from running!
        super(TemplateTests, self).tearDown()
        
       

    def check_for_log_errors(self):
        """ 
        Check the browser driver logs for any js errors 
        The method commented out below is only available in chrome but chrome has a whole bunch of other issues....
        See: https://github.com/mozilla/geckodriver/issues/284
        Possible solution is https://github.com/hurracom/WebConsoleTap
        For now no log errors are checked
        """
        #for entry in self.selenium.get_log('browser'):
            # Any severe js errors should cause test to fail
            # self.assertNotEqual(entry['level'], 'SEVERE')
            # if entry['level'] == 'SEVERE':
            #    logger.warning(f"SEVERE LOG ERROR: {entry['message']}")

    def get_url_as_admin(self, url: str, username: str = "paul", password: str = "test"):
        """
        Calls the selenium get method and sets the state of the driver but by using an authenticated admin user (from test database)
        """
        # set authentication cookie (for admin user)
        self.client.login(username=username, password=password)
        cookie = self.client.cookies['sessionid']
        self.selenium.get(url)
        self.selenium.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.selenium.refresh()
        self.selenium.get(url)

    def get_url_as_rse(self, url: str, username: str = "user2", password: str = "12345"):
        """
        Calls the selenium get method and sets the state of the driver but by using an authenticated rse user (from test database)
        """
        # set authentication cookie (for rse user)
        self.client.login(username=username, password=password)
        cookie = self.client.cookies['sessionid']
        self.selenium.get(url)
        self.selenium.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.selenium.refresh()
        self.selenium.get(url)

    ########################
    ### Index (homepage) ###
    ########################

    def test_homepage_login(self):
        """
        Tests the homepage to check for login redirect
        """
        self.selenium.get(f"{self.live_server_url}{reverse_lazy('index')}")
        expected = TemplateTests.PAGE_TITLE_LOGIN
        self.assertEqual(self.selenium.title, expected)

        # check for javascript errors in log
        self.check_for_log_errors()

    def test_homepage(self):
        """ Tests the homepage to check for admin homepage (with login) """
        
        # test url
        url = f"{self.live_server_url}{reverse_lazy('index')}"

        # test admin view
        self.get_url_as_admin(url)
        expected = "RSE Group Administration Tool: Admin Homepage"
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()
        
        # test rse view
        self.get_url_as_rse(url)
        expected = "RSE Group Administration Tool: RSE User Homepage"
        self.assertEqual(self.selenium.title, expected)   
        self.check_for_log_errors()         


    #######################
    ### Authentication ####
    #######################

    def test_login(self):
        """ Tests the login page """

        # test url
        url = f"{self.live_server_url}{reverse_lazy('login')}"
        # test page (no authentication)
        self.selenium.get(url)
        expected = TemplateTests.PAGE_TITLE_LOGIN
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()

    # logout has no template

    def test_change_password(self):
        """ Tests the change_password page """

        # test url
        url = f"{self.live_server_url}{reverse_lazy('change_password')}"

        # test admin view
        self.get_url_as_admin(url)
        expected = "RSE Group Administration Tool: Change Password"
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()
        
        # test rse view
        self.get_url_as_rse(url)
        expected = "RSE Group Administration Tool: Change Password"
        self.assertEqual(self.selenium.title, expected)  
        self.check_for_log_errors()

    def test_user_new(self):
        """ Tests the user_new page """

        # test url
        url = f"{self.live_server_url}{reverse_lazy('user_new')}"

        # test admin view
        self.get_url_as_admin(url)
        expected = "RSE Group Administration Tool: New User"
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()
        
        # test rse view
        self.get_url_as_rse(url)
        expected = TemplateTests.PAGE_TITLE_LOGIN
        self.assertEqual(self.selenium.title, expected)  
        self.check_for_log_errors()


    def test_user_new_rse(self):
        """ Tests the user_new_rse page """

        # test url
        url = f"{self.live_server_url}{reverse_lazy('user_new_rse')}"

        # test admin view
        self.get_url_as_admin(url)
        expected = "RSE Group Administration Tool: New RSE User"
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()
        
        # test rse view (login should be required)
        self.get_url_as_rse(url)
        expected = TemplateTests.PAGE_TITLE_LOGIN
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()

    def test_user_edit_rse(self):
        """ Tests the user_edit_rse page """

        # test url
        url = f"{self.live_server_url}{reverse_lazy('user_edit_rse', kwargs={'rse_id': self.first_rse_id})}"

        # test admin view
        self.get_url_as_admin(url)
        expected = "RSE Group Administration Tool: Edit RSE User"
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()
        
        # test rse view (login should be required)
        self.get_url_as_rse(url)
        expected = TemplateTests.PAGE_TITLE_LOGIN
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()

    def test_user_new_admin(self):
        """ Tests the user_new_admin page """

        # test url
        url = f"{self.live_server_url}{reverse_lazy('user_new_admin')}"

        # test admin view
        self.get_url_as_admin(url)
        expected = "RSE Group Administration Tool: New Admin User"
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()
        
        # test rse view (login should be required)
        self.get_url_as_rse(url)
        expected = TemplateTests.PAGE_TITLE_LOGIN
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()

    def test_user_edit_admin(self):
        """ Tests the user_edit_admin page """

        # test url
        url = f"{self.live_server_url}{reverse_lazy('user_edit_admin', kwargs={'user_id': self.admin_user_id})}"

        # test admin view
        self.get_url_as_admin(url)
        expected = "RSE Group Administration Tool: Edit Admin User"
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()
        
        # test rse view (login should be required)
        self.get_url_as_rse(url)
        expected = TemplateTests.PAGE_TITLE_LOGIN
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()

    def test_user_change_password(self):
        """ Tests the user_change_password page """

        # test url
        url = f"{self.live_server_url}{reverse_lazy('user_change_password', kwargs={'user_id': self.first_rse_user_id})}"

        # test admin view
        self.get_url_as_admin(url)
        expected = "RSE Group Administration Tool: Change A Users Password"
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()
        
        # test rse view (login should be required)
        self.get_url_as_rse(url)
        expected = TemplateTests.PAGE_TITLE_LOGIN
        self.assertEqual(self.selenium.title, expected)   
        self.check_for_log_errors()  

    def test_users(self):
        """ Tests the users page """

        # test url
        url = f"{self.live_server_url}{reverse_lazy('users')}"

        # test admin view
        self.get_url_as_admin(url)
        expected = "RSE Group Administration Tool: View all Users"
        self.assertEqual(self.selenium.title, expected)
        self.check_for_log_errors()
        
        # test rse view (login should be required)
        self.get_url_as_rse(url)
        expected = TemplateTests.PAGE_TITLE_LOGIN
        self.assertEqual(self.selenium.title, expected)  
        self.check_for_log_errors()   
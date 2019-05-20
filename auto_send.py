from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search.settings")
django.setup()

from log.models import Log
from search.views import MainList, TOKEN


if __name__ == '__main__':
    logs = Log.objects.filter(auto_search='Y')

    for log in logs:
        main = MainList(keywords=log.keywords, company_name=log.company_name)
        main.get_links()
        main.send_message()

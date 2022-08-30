# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# import os 

# SLEEP_SHORT = 5

# def get_driver(headless=False, no_sandbox=True, disable_dev_shm_usage=True):
#     # Make browser open in background
#     options = webdriver.ChromeOptions()
#     options.add_argument('--no-sandbox') if no_sandbox else None
#     options.add_argument('--headless') if headless else None
#     options.add_argument('--disable-dev-shm-usage') if disable_dev_shm_usage else None

#     # check possible locations for chromedriver
#     possible_locations = [
#         'chromedriver',
#         'chromedriver.exe',
#         '../chromedriver',
#         '../chromedriver.exe',
#         './spiders/chromedriver',
#         './spiders/chromedriver.exe',
#         '/media/ggarrett/SpaceJunk/codee/horses/horses/spiders/chromedriver',
#     ]
#     driver_path = None
#     for location in possible_locations:
#         # check if chromedriver exists
#         if os.path.exists(location):
#             # add to path 
#             os.environ['PATH'] += os.pathsep + os.path.dirname(location)
#             driver_path = location
#     if driver_path is None:
#         raise Exception('chromedriver not found')
#         # raise exception if not found
#     return webdriver.Chrome(chrome_options=options,
#                             executable_path=driver_path)



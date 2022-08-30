from facebook_scraper import get_posts
import requests
import json 

# get cookies from exported-cookies.json
# with open('/media/ggarrett/SpaceJunk/codee/horses/horses/exported-cookies.json', 'r') as f:
#     cookies = json.load(f)

# print(cookies)

# cookiejar = requests.utils.cookiejar_from_dict(*cookies)
# cookiejars = [requests.utils.cookiejar_from_dict(c) for c in cookies]
# print(cookiejars)
# print(cookiejar)


for post in get_posts(group=1492885717598959,
# credentials=('geoffrey_garrett@hotmail.com', '@rtful_Crypt0M!n3r2207'),
 pages=1,
 cookies="/media/ggarrett/SpaceJunk/codee/horses/horses/facebook.com_cookies.txt"):
     print(post['text'][:50])

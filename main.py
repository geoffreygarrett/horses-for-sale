import pymongo
from horses.settings import MONGO_DATABASE, MONGO_URI
import re 
import datetime 
import os 

# get pymongo
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]

# get collection
collection = db['horses']

# get all items
items = list(collection.find())

import pandas as pd


def make_clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)

def make_image(url, alt=''):
    # add https://www.junkmail.co.za/images/jm-logo-red.jpg?v=HElAEZdbB6iRmsT1_qvPDx1mpkA7OuzOCCCfThquvPQ image in the bottom right corner
    # return

    return '<img src="{}" alt="{}" style="width:100px;height:100px;">'.format(url, alt)

def get_age(date):
    # re_age = r"(\d+\s?[yY]ears)|(20\d{2})"
    re_age_1 = r"(\d+)\s?[yY]ears"
    re_age_2 = r"(20\d{2})"
    
    # if match group 1 
    match_1 = re.findall(re_age_1, date)
    match_2 = re.findall(re_age_2, date)

    if match_1:
        return match_1[0]
        # if group 1
    elif match_2:
        # get current year
        current_year = datetime.datetime.now().year
        return current_year - int(match_2[0])
    else:
        raise ValueError("No age found, {}: {}, {}".format(date, match_1, match_2))

df = pd.DataFrame(items)

df['sold'] = df['ref'].apply(lambda x: True if type(x)==str and "(Sold)" in x else False)
df['gender'] = df['details'].apply(lambda x: x['Gender'] if 'Gender' in x else None)

# remove unwanted values
df = df[df['sold'] == False]
# df = df[df['gender'] != 'Filly']
# df = df[df['gender'] != 'Colt']

df['name'] = df.apply(lambda x: make_clickable(x['link'], x['name']), axis=1)
# df['ref'] = df['ref'].replace('\n', '', regex=True)
#
df['image'] = df['images'].apply(lambda x: make_image(x[0], 'image') if x and type(x) is list else None)

temp = df['details'].apply(lambda x: x['DOB / Age'] if 'DOB / Age' in x else None)
df['age'] = temp.apply(lambda x: get_age(x) if x else None)

df['height'] = df['details'].apply(lambda x: x['Height'] if 'Height' in x else None)
df['breed'] = df['details'].apply(lambda x: x['Breed'] if 'Breed' in x else None)

# set print optiosn
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)
# print(df)





# convert to teimdelta from hours if not float NaN
def convert_to_timedelta(hours):
    try:
        return datetime.timedelta(hours=hours)
    except:
        return None

df['driving_time'] = df['driving_time'].apply(lambda x: convert_to_timedelta(x))

#
# # filter driving time more than 8 hours
df = df[df['driving_time'] < datetime.timedelta(hours=12)]

# # where price is string, set as infinity
# df['price'] = df['price'].apply(lambda x: int(10e9) if type(x)==str else x)

# sort price ascending
# df = df.sort_values(by='price', ascending=True)

# # format price as <thousands> k
# def format_price(price):
#     # if price is 10e9, set as 'Not mentioned'
#     if price == 10e9:
#         return 'Not mentioned'
#     elif price:
#         return "{} k".format(int(price/1000))
#     else:
#         return None

# df['price'] = df['price'].apply(lambda x: format_price(x) if type(x)==float else None)

# format date to day name month name year
# def format_date(date):
#     return datetime.datetime.strftime(date, '%B %d %Y')


# def format_timedelta(td):
#     minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
#     hours, minutes = divmod(minutes, 60)
#     return '{:d} h {:02d} m'.format(hours, minutes, seconds)
    # return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

# def largest_unit(td):
#     if td.days > 0:
#         return td.days
#     elif td.hours > 0:
#         return td.hours
#     elif td.minutes > 0:
#         return td.minutes
#     elif td.seconds > 0:
#         return td.seconds
#     else:
#         return None

# def format_added_timedelta(td):
#     unit = largest_unit(td)
#     if unit == td.days:
#         # check for months
#         if td.days > 30:
#             ret = "{} month".format(int(td.days/30))
#             unit = int(td.days/30)
#         else:
#             ret = '{} day'.format(td.days)
#     elif unit == td.hours:
#         ret = '{} hour'.format(td.hours)
#     elif unit == td.minutes:
#         ret = '{} minute'.format(td.minutes)
#     elif unit == td.seconds:
#         ret = '{} second'.format(td.seconds)
#     else:
#         ret = None
    
#     # check for plural
#     if ret and unit > 1:
#         ret += 's'
#     return ret

def format_added_timedelta(td):
    # unit = largest_unit(td)
    return int(td.days)

# add column for time delta "added" in days hours ago
df['listing_age'] = df['listing_date'].apply(lambda x: format_added_timedelta(datetime.datetime.now() - x))
# df['listing_date'] = df['listing_date'].apply(lambda x: format_date(x) if x else None)

# where values are None, set to "N/A"
msg = "N/A"
df['breed'] = df['breed'].apply(lambda x: x if x  is not None else msg)
df['gender'] = df['gender'].apply(lambda x: x if x  is not None else msg)
df['age'] = df['age'].apply(lambda x: x if x  is not None else msg)
df['height'] = df['height'].apply(lambda x: x if x  is not None else msg)


#     print(v)
# sort by driving time and reindex
# df.sort_values(by=['driving_time'], inplace=True, ascending=True)

df.reset_index(drop=True, inplace=True)

# format driving time to 1 decimal place
# convert df['driving_time'] to timedelta


df['driving_time'] = df['driving_time'].apply(lambda x: x.seconds)

# change all NoneType values to N/A
# reorder columns
df = df[['name', 
# 'ref',
# 'sold',
'image',
'gender', 
'age', 
'height', 
'breed', 
'price', 
'driving_time', 
'location',
'listing_age', 
# 'link'
]]
df = df.replace("None", 'N/A')

# save as html and open
html_string = '''
<!DOCTYPE html>
<html>
  <head><title>Horses for sale in proximinity of the Overberg District, WC</title>
  <script defer src="script.js"></script>
  </head>
  <link rel="stylesheet" type="text/css" href="style.css"/>
  <body>
    <h2><b>Horses for sale in proximinity of the Overberg District, WC</b></h2>
    <p><b>Time updated:</b> {last_updated}</p>
    <p><b>Horses found:</b> {horses_found}</p>
    <!-- add a field for filtering a column value from a drop down -->
    <div id="filter">
      <button id="add_filter", onclick="add_filter()">Add filter</button>
    </div>
    <p><b>Click on a column header to sort.</b> </p>
    <p>Feel free to leave feedback through one of the icons below.</p>
    <p><a href="https://github.com/geoffreygarrett/horses-for-sale" target="_blank"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" style="width:40px;height:40px;"></a></p>
    {table}
  </body>
</html>
'''

# rename 'listing age' colum to 'Listing age (days)'
# df.rename(columns={'listing_age': 'Listing age (days)'}, inplace=True)

# remove underscores from column names
df.columns = [x.replace('_', ' ') for x in df.columns]
html_table = df.to_html(render_links=True, classes='mystyle', escape=False, index=False)
import shutil



print(df.columns)

# if out doesnt exist, create it
if not os.path.exists("out"):
    os.makedirs("out")

# for v in df['price'].values:
#     print(v)
# OUTPUT AN HTML FILE
# format date to day name month name year hour minute second timezone
last_updated = datetime.datetime.now().strftime('%B %d %Y %H:%M:%S SAST')
horses_found = len(df)
with open('out/index.html', 'w') as f:
    f.write(html_string.format(table=html_table, last_updated=last_updated,
    horses_found=horses_found))

# copy style.css from styles/ to out/
shutil.copyfile('styles/style.css', 'out/style.css')
shutil.copyfile('js/script.js', 'out/script.js')

# # write last updated to file
# with open('out/last_updated.txt', 'w') as f:
#     f.write(last_updated)


# copy template/deploy-pages.yaml to out/.github/workflows/deploy-pages.yaml creating if necessary
if not os.path.exists("out/.github/workflows"):
    os.makedirs("out/.github/workflows")
shutil.copyfile('template/deploy-pages.yaml', 'out/.github/workflows/deploy-pages.yaml',)

# "output.html", 
os.system("xdg-open out/index.html")
        


import datetime
from random import randint, shuffle
from time import sleep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #hdr)
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except: 
        pass
        
    return html_content

def get_details(url):
    
    stamp = {}
    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price = html.select('.VariationProductPrice')[0].get_text()
        price = price.replace('$', '').replace(',', '').strip()
        stamp['price'] = price
    except: 
        stamp['price'] = None

    try:
        title = html.select('#ProductBreadcrumb li')[-1].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None
        
    try:
        sku = html.select('.VariationProductSKU')[0].get_text().strip()
        stamp['sku'] = sku
    except:
        stamp['sku'] = None    
        
    try:
        stock_num = html.select('.VariationProductInventory')[0].get_text().strip()
        stamp['stock_num'] = stock_num
    except:
        stamp['stock_num'] = None
        
    try:
        raw_text = html.select('.DetailRow')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None

    stamp['currency'] = "USD"

    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('.ProductThumbImage a')
        for image_item in image_items:
            img = image_item.get('href')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    #sleep(randint(25, 65))
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.ProductDetails a.pname'):
            item_link = item.get('href').strip()
            items.append(item_link)
    except:
        pass

    try:
        next_item = html.select('a.nav-next')
        if next_item:
            next_url = next_item[0].get('href')
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items, next_url

selection = input('Please insert url: ')
            
page_url = selection
while(page_url): 
    page_items, page_url = get_page_items(page_url)
    for page_item in page_items:
        stamp = get_details(page_item)
import re
def get_url_input( mode):
        while True:
            fmode = mode.replace('_',' ')
            url = input(f'Enter {fmode} URL : ')
            if mode == 'single_product':
                if ('product' not in url and not re.search(r'https://www\.digikala\.com/product/dkp-\d+/$', url) ):
                    print('URL is not belong to any product check it and Please try again.')
                    continue
            elif mode == 'single_seller':
                pattern = re.compile(r'https://www\.digikala\.com/seller/[A-Za-z0-9]+$')
                if  (not pattern.match(url)):
                     print("URL is not belong to any seller check it and Please try again.")
                     continue
            elif mode == 'category':
                pattern = re.compile(r'search/\?q=|/category-|/search/')
                if not ('search/?q=' in url or '/category-' in url or '/search/' in url):
                    print('Wrong category URL, try one more time')
                    continue
            break
        return url
get_url_input( 'single_product')
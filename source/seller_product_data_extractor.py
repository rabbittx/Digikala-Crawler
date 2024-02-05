from time import gmtime, strftime ,sleep
class SellerProductDataExtractor:
    """
     This class is used to extract the required data for a seller product listing.
    
    """
    def __init__(self, driver ,db_handler,log):
        self.log = log
        self.driver = driver
        self.db_handler = db_handler

    def has_desired_text(self,tags,find_text):
        """
         Check if any of the tags in 'tags' contains 'find_text'. 
         
        :param tags: A list of WebElement objects representing the HTML elements being checked.
        :type tags: List[WebElement]
        :param find_text: The text that we want to search for within the elements.
        :type find_text: String
        :return: element or False depending on whether 'find_text' was found in one of the elements.
        
        """
        for element in tags:
            if find_text in element.text :
                return element

    def seller_details(self,soup):
        """
         Extracts and returns the details about the seller from the given BeautifulSoup object.
         
        :param soup: A BeautifulSoup object containing the page source code.
        :type soup: BeautifulSoup
        :return: Dictionary with keys as "name" & "rating". Value corresponding to each key is string.
        
        """
        self.log.info('start to ectrext seller details')
        return { 'crawl_date' : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                'seller_name':soup.find('h1',{'class':'text-h5 text-neutral-900 whitespace-nowrap'}).text,
                'membership_period':soup.find('div',{'class':'w-full flex flex-col mr-5'}).find('p',{'class':'text-body-2'}).text,
                'satisfaction_with_goods':soup.find('p',string='رضایت از کالاها').find_parent('div').find('p').text,
                'seller_performance':soup.find('p',string='عملکرد فروشنده').find_parent('div').find('p').text,
                'people_have_given_points':self.has_desired_text(soup.find_all('p',),'نفر امتیاز داده‌اند').string.replace('نفر امتیاز داده‌اند','') if self.has_desired_text(soup.find_all('p',),'نفر امتیاز داده‌اند') else ' Uncertain number of votes',
                'timely_supply':soup.find('p', string='تامین به موقع').find_previous_sibling('p').string,
                'obligation_to_send':soup.find('p', string='تعهد ارسال').find_previous_sibling('p').string,
                'no_return':soup.find('p', string='بدون مرجوعی').find_previous_sibling('p').string,
                'introduction_of_the_seller':soup.find('span',string='معرفی فروشنده').find_parent('div').find_parent('div').find_next_sibling('div').text if soup.find('span',string='معرفی فروشنده') else ' info unavailable ',
            }
    
    def extract_product_details(self,product):
        """
         Extracts product information (price, discount price, description) from a single product element.
         
        :param product: A WebElement object representing the product's HTML element.
        :type product: WebElement
        :return: Dictionary with keys as "price","discounted_price","description". Values are strings.
        
        """
   
        try :
            img_element = product.find('picture').find('img', {'class': 'w-full rounded-medium inline-block'})
        except Exception as e :
            self.log.error(f'Error during find product picture {e}')
        try :
            rate_element = product.find('div',{'class':'mb-1 flex items-center justify-between'}).find('p',{'class':'text-body2-strong text-neutral-700'})
        except Exception as e : 
            self.log.error(f'Error during find product rate {e}')
        try : 
            price_element = product.find('span',{'data-testid':'price-final'})
        except Exception as e : 
            self.log.error(f'Error during find product price {e}')
        try :
            price_discount_percent_element = product.find('span',{'data-testid':'price-discount-percent'})
        except Exception as e : 
            self.log.error(f'Error during find product price discount percent {e}')
        try :    
            element_price_discount = product.find('div',{'data-testid':'price-no-discount'})
        except Exception as e :
            self.log.error(f'Error during find product price discount {e}')
        try:
            product_special_sale = 'special sale' if 'SpecialSell.svg' in (product.find('div', {'class': 'flex items-center justify-start mb-1'}).find('img').get('src', '')) else 'unavailable special sale'
        except AttributeError:
            product_special_sale = 'unavailable special sale'

   
        return {
            'crawl_date' : strftime("%Y-%m-%d %H:%M:%S", gmtime())  ,
            'product_id':product.find('a')['href'].split('/')[2],
            'product_link': "https://www.digikala.com"+product.find('a')['href'],
            'product_image':img_element['src'] if img_element else 'image not found' ,
            'product_rate':rate_element.text if rate_element else 'rate not found',
            'product_name':product.find('h3').text,
            'product_price':price_element.text.replace(',','') if price_element else "product unavailable",
            'product_price_discount_percent':price_discount_percent_element.text if price_discount_percent_element else "unavailable discount percent",
            'product_price_discount':element_price_discount.text if element_price_discount else "unavailable discount price" ,
            'product_special_sale':product_special_sale,
            'stock':self.has_desired_text(product.find('p'),'باقی مانده').replace('تنها ','').replace(' عدد در انبار باقی مانده','') if self.has_desired_text(product.find('p'),'باقی مانده') else 'Quantity unspecified',
        }

    def check_category(self,url,scroll_count):
        """
         This method use to extrect  data from category page of digikala.
         
         :param url: Link of the category page that we want to crawle.
         :type url: Str
         :param scroll_count: How many time we will scroll down on this page for load all products.
         :type scroll_count: Int
         :return: List of dict contain information about each product in this category.
         :rtype: List[Dict]
        
        """
        self.driver.open_page(url)
        self.driver.scroll_page(scroll_count)
        page_source = self.driver.get_page_source()
        prodcut_links = self.driver.get_prdoucts_on_page(page_source,return_value='products_link')
        sellers_id = []
        self.log.info(f"{len(prodcut_links)} - product links found on this category page with scroll count of {scroll_count}")
        for link in prodcut_links:
            self.driver.open_page(link)
            seller_id = self.driver.get_seller_id()
            # digikala id = 5a52n - pass this one to extrect 
            if seller_id not in sellers_id and seller_id != None and seller_id != 'No_seller':
                sellers_id.append(seller_id)
        
        self.log.info(f"{len(sellers_id)} - unique seller found on this category")
        for index , seller in  enumerate(sellers_id):
            
            seller_link = f'https://www.digikala.com/seller/{seller}'
            self.log.info(f'[!] try to open seller page with id=[{seller}] - {index+1}/{len(sellers_id)}')
            self.driver.open_page(seller_link)
            self.driver.scroll_page(scroll_count=True)
            self.driver.click_on_element_by_xpath("//p[text()='جزئیات بیشتر']/..")
            seller_page_source_code = self.driver.get_page_source()
            seller_info = self.seller_details(seller_page_source_code)
            seller_info['seller_id'] = seller
            self.db_handler.update_database(data=seller_info,column_name='seller_id',table_name='sellers')
            self.driver.click_on_element_by_xpath("//div[@role='dialog']//div[@class='flex cursor-pointer']")
            product_elements = self.driver.get_prdoucts_on_page(seller_page_source_code,return_value='products_element')
            for product in product_elements:
                product_info = self.extract_product_details(product)
                product_info['seller_name'] = seller_info['seller_name']
                product_info['seller_id'] = seller_info['seller_id']
                product_info['product_id'] = product_info['product_id']
                self.db_handler.update_database(data=product_info,column_name='product_id',table_name='products')
            self.log.info(f'[!] seller page with id=[{seller}] - extrection successfully ')
        
    def check_seller(self,url):
        """
         This method is used to get the details of a specific seller by url.

         Args :
            url : seller page url 

         Return :
                dict : contains all information about the seller .
        
        """
        self.log.info(f'[!] try to open seller page')
        self.driver.open_page(url)
        self.driver.scroll_page(scroll_count=True)
        self.driver.click_on_element_by_xpath("//p[text()='جزئیات بیشتر']/..")
        seller_page_source_code = self.driver.get_page_source()
        seller_info = self.seller_details(seller_page_source_code)
        seller_info['seller_id'] = url.split('/')[-2]
        self.db_handler.update_database(data=seller_info,column_name='seller_id',table_name='sellers')
        self.driver.click_on_element_by_xpath("//div[@role='dialog']//div[@class='flex cursor-pointer']")
        product_elements = self.driver.get_prdoucts_on_page(seller_page_source_code,return_value='products_element')
        for product in product_elements:
            if product.find(lambda tag: tag.name == "title" and tag.text.strip() == "Loading..."):
                continue
            else :
                product_info = self.extract_product_details(product)
                product_info['seller_name'] = seller_info['seller_name']
                product_info['seller_id'] = seller_info['seller_id']
                product_info['product_id'] = product_info['product_id']
                self.db_handler.update_database(data=product_info,column_name='product_id',table_name='products')
        self.log.info(f'[!] seller page with id=[{seller_info["seller_id"]}] - extrection successfully ')
        
      

from bs4 import BeautifulSoup, Tag, ResultSet
from time import gmtime, strftime
import re

class ProductDetailsExtractor:
    """
     Class to extract product details from a given HTML page.
    
    """
    def __init__(self, driver,db_handler,log):
            self.log = log
            self.driver = driver
            self.db_handler = db_handler

    def clean_text(self, text):
        """
         Method to remove unwanted characters and return the cleaned text.
         
        Args:  
            text (str,list,dict,url): The input string that needs to be cleaned.
        
        Return :
            clean text
        """
        pattern = '[^ا-یآ-ی۰-۹a-zA-Z0-9\s:/\.\-،%(),\n _]'
        def is_url(s):
            return re.match(r'https?://\S+\.\S+', s)
        if isinstance(text, str):
            if is_url(text):
                return text
            return re.sub(pattern, '', text.replace('\n','').replace('\n\n','').replace('\r','').replace('\xa0',' '))
        elif isinstance(text, list):
            return [self.clean_text(i) for i in text]
        elif isinstance(text, dict):
            return {k: self.clean_text(v) for k, v in text.items()}
    
    def check_with_multi_class_name(self,element,field_name,tag_name,attrs_name,attrs_list):
        """
         this method use to find element if they have multi class name .

         Args :
            element : tags of element object of Bs4 
            field_name : field name which we want to search on it .
            tag_name :  tag name of element .
            attrs_name : attribute name of element .
            attrs_list : list of value of attribute .
            
         Returns :
              result of search .
        
        """
        for class_combo in attrs_list:
            price_span = element.find(tag_name, {attrs_name: class_combo})
            if price_span:
                field = price_span.get_text(strip=True)
                break
            else:
                field = f"{field_name} Not available"
        return field
    
    def safe_find(self,soup,finds, tag, attrs):
        """
         This method help to  find elements with try and catch block ,  
         so if there is an error in finding process it will not raise any exception  
         
         Args :
             soup : page content that we want to search on it .
             finds : string that contain the values what you want to find (find,find_all) .
             tag : tag name of element to find.
             attrs : dictionary of attributes of element .
             
         Returns :
               Element object or None .
        
        """
        try:
            if finds == 'find':
                return soup.find(tag, attrs)
            elif finds == 'find_all':
                return soup.find_all(tag, attrs)
        except AttributeError:
            return 'element not found'
    
    def safe_extraction(self,element_name ,element, extraction_function):
        """
         This method call extraction function by passing required arguments   
         Args : 
             element_name : this argument used for making good log message  
                            when there is a problem in extracting data from html .
             element       : HtmlElementObject that we want to extract its value .
             extraction_function : Function that defined how we want to extract data from HtmlElementObject .
             
         Returns :
                 The result of extraction_function .
        """
        try:
            return extraction_function(element)
        except Exception as e:
            # self.log.error(f'NOT FOUND - {element_name} - {e}')
            return f'{element_name} not found '
        
    def product_elements_extraction(self,soup):
        """
         This method will extraction  all needed products elements from html page using BeautifulSoup library .
         
         Args :
            soup : HtmlElementObject.

         Return :
              dictionary of  all products information that extracted from the page .
        
        """
        specific_text = 'پیشنهاد فروشندگان'
        element = soup.select_one("span:-soup-contains('{}')".format(specific_text)).find_parent('div',{'class':'flex flex-col relative overflow-hidden w-full pt-2 lg:border-complete-200 lg:rounded-medium lg:mt-4 pb-3 styles_PdpProductContent__sectionBorder__39zAX'}) if  soup.select_one("span:-soup-contains('{}')".format(specific_text)) else 'element not found'
        
        if isinstance(element, BeautifulSoup):
            seller_offer = element.find_all("a",{'class':'block cursor-pointer relative bg-neutral-000 overflow-hidden grow py-3 px-4 lg:px-2 h-full border-complete-l'})
        else:
            seller_offer = 'offer not found'   
        product_elements = {}
        product_elements['categories'] = self.safe_find(soup,'find','div',{'class':'swiper-container swiper-container-initialized swiper-container-horizontal swiper-container-pointer-events swiper-container-free-mode swiper-container-rtl'}).text.replace('\u200c',' ') if self.safe_find(soup,'find','div',{'class':'swiper-container swiper-container-initialized swiper-container-horizontal swiper-container-pointer-events swiper-container-free-mode swiper-container-rtl'}) else 'categories element not found'
        product_elements["main_product_details"] = self.safe_find(soup,'find','div',{'class':'styles_InfoSection__leftSection__0vNpX'}).parent if self.safe_find(soup,'find','div',{'class':'styles_InfoSection__leftSection__0vNpX'}) else 'element not found'       
        product_elements["buy_box"] = self.safe_find(soup,'find','div',{'data-testid':'buy-box'})
        product_elements["image_box"] = self.safe_find(soup,'find','div',{'class':'flex flex-col items-center lg:max-w-92 xl:max-w-145 lg:block mb-2'}).find_all('picture') if self.safe_find(soup,'find','div',{'class':'flex flex-col items-center lg:max-w-92 xl:max-w-145 lg:block mb-2'}) else 'images element not found'
        product_elements["other_seller_box"] =self.safe_find(soup,'find','div',{'id':'sellerSection'}).find_all('div',{'class':'rounded-medium styles_SellerListItemDesktop__sellerListItem__u9p3q p-4'}) if self.safe_find(soup,'find','div',{'id':'sellerSection'}) else "no found other seller for this product"
        product_elements["similar_products"] = self.safe_find(soup,'find_all','a',{'data-cro-id':'related-products'}) 
        product_elements["related_videos"] = self.safe_find(soup,'find_all','div',{"data-cro-id":"magnet_click_on_video"})                  
        product_elements["introduction_box"] = self.safe_find(soup,'find','div',{'id':'PdpShortReview'}).parent.find('div',{'class':'text-body-1 text-neutral-800'}).text if self.safe_find(soup,'find','div',{'id':'PdpShortReview'}) else 'Introduction element not found'
        product_elements["expert_check_box"] = self.safe_find(soup,'find','div',{'id':'expertReview'}).parent if self.safe_find(soup,'find','div',{'id':'expertReview'}) else 'expert check box element not found'
        product_elements["specifications_box"] = self.safe_find(soup,'find_all','div',{'class':'flex flex-col lg:flex-row pb-6 lg:py-4 styles_SpecificationBox__main__JKiKI'})
        product_elements["reviews_box"] = self.safe_find(soup,'find_all','article',{'class':'py-3 lg:mt-0 flex items-start br-list-vertical-no-padding-200'})
        product_elements["question_box"] = self.safe_find(soup,'find_all','article',{'class':'br-list-vertical-no-padding-200 py-3'})
        product_elements["also_bought_items"] = self.safe_find(soup,'find_all','a',{'data-cro-id':"also_bought_products"})                            
        product_elements["seller_offer"] = seller_offer      
        return product_elements
    
    def main_product_details_extraction(self,element):
        """
         Extracting data from a div element which contains main details about the product .

         Args :
             element : HtmlElementObject.

         Returns :
                 Dictionary contain title , price and other main features of the product .
        
        """
        if isinstance(element ,(Tag, ResultSet)):
            details={}
            details["product_title"] = self.safe_extraction('product title',element, lambda e: e.find('h1',{'data-testid':'pdp-title'}).text)
            details["product_main_title"] = self.safe_extraction('product main title',element, lambda e: e.find('span',{'class':'text-neutral-300 ml-2 text-body-2'}).text)
            details["user_review"] = self.safe_extraction('user review',element, lambda e: e.find('p',{'class':'ml-2 text-neutral-600 text-body-2'}).text)
            details["colors"] = self.safe_extraction('colors',element, lambda e: [element_color.text for element_color in e.find('div',{"class":"border-complete-t lg:border-none mt-3 lg:mt-0"}).find_all('div',{'data-popper-placement':"bottom"})])
            details["insurer"] = self.safe_extraction('Insurer',element, lambda e: e.find('div',{'class':'bg-neutral-000 flex border-complete-200 rounded-medium'}).find('p',{'class':'text-body2-strong text-neutral-700'}).text)
            details["Insurance_discount_percent"] = self.safe_extraction('Insurance discount percent',element, lambda e: e.find('div',{'class':'bg-neutral-000 flex border-complete-200 rounded-medium'}).find('span',{'data-testid':'price-discount-percent'}).text)
            details["Insurance_price_before_discount"] = self.safe_extraction('Insurance Price before discount',element, lambda e: e.find('div',{'class':'bg-neutral-000 flex border-complete-200 rounded-medium'}).find('div',{'class':'text-body-2 text-neutral-300 line-through'}).text)
            details["Insurance_final_price"] = self.safe_extraction('Insurance final price',element, lambda e: e.find('div',{'class':'bg-neutral-000 flex border-complete-200 rounded-medium'}).find('span',{'data-testid':'price-final'}).text)
            self.log.info('[+] main details extraction successfully')
            return details
        else :
            return {}
        
    def product_buy_box_extraction(self,element):
        """
         Extracting data from a div element which contains buy box details about the product 
        
         Args :
             element : HtmlElementObject.

         Returns :
                 Dictionary contain other_sellers,warranty,discount info and etc ... .
        """
        if isinstance(element ,(Tag, ResultSet)):
            details={}
            details["other_sellers"]= self.safe_extraction('other sellers',element, lambda e: e.find('span',{'data-cro-id':'pdp-other-seller'}).text)
            details["satisfaction_with_the_product"]= self.safe_extraction('satisfaction with the product',element, lambda e: e.find('div',{"data-cro-id":"pdp-seller-info-cta"}).find('p',{'class':'ml-1 text-body2-strong'}).text)
            details["warranty"]= self.safe_extraction('warranty',element, lambda e: e.find('div',{'data-cro-id':'pdp-shipment-info'}).find_previous('p',{'class':'text-button-2 text-neutral-700'}).text)
            details["digiclub_points"]= self.safe_extraction('digiclub points',element, lambda e: e.find('div',{'data-cro-id':'pdp-shipment-info'}).find_next('p',{'class':'text-button-2 text-neutral-700'}).text)
            details["discount_percent"] = self.safe_extraction('discount percent',element, lambda e: e.find('span',{'data-testid':'price-discount-percent'}).text)
            details["price_before_discount"] = self.safe_extraction('Price before discount',element, lambda e: e.find('span',{'data-testid':'price-no-discount'}).text)
            details["final_price"] = self.safe_extraction('final price',element, lambda e: e.find('span',{'data-testid':'price-final'}).text)
            details["product_stock"] = self.safe_extraction('prdouct stock', element, lambda e: e.find('p',{"class":"text-primary-500 text-body2-strong mb-3"}).text)
            self.log.info('[+] buy box extraction successfully')
            return details
        else :
            return {}
        
    def product_image_extraction(self,element):
        """
         Get image url from img tag in html page.
         
         Args:
             element : HtmlElementObject.
             
         Return:
                Image Url as String.
        
        """
        if isinstance(element ,(Tag, ResultSet)):
            return {'product_images' :self.safe_extraction('images',element, lambda e: [image.find('img')["src"] for image in e])}
        else :
            return {}
        
    def other_seller_box_extraction(self,element):
        """
         Extracting information of other sellers who have this product.
         
         Args :
             element : HtmlElementObject that contain all other seller's box.
             
         Returns :
                 List of Dictionaries each dictionary represent one seller with his name and price.
        
        """
        class_combinations = [
                                'text-h4 ml-1 text-neutral-800', 
                                'text-neutral-800 ml-1 text-h4',  
                            
                            ]
    
        if isinstance(element ,(Tag, ResultSet)):
            other_sellers = []
            for seller in element:
                seller_info = {}
                seller_info["other_seller_seller_name"] = self.safe_extraction('seller name', seller, lambda e: e.find('p',{'class':'text-neutral-700 ml-2 text-subtitle'}).text)
                seller_info["other_seller_page_link"] = self.safe_extraction('seller page link', seller, lambda e: e.find('a',{'class':'styles_Link__RMyqc'})["href"])
                seller_info["warranty"] = self.safe_extraction('seller warranty', seller, lambda e: e.find('p',{'class':'text-subtitle text-neutral-700'}).text)
                seller_info["discount_percent"] = self.safe_extraction('discount percent', seller, lambda e: e.find('span',{"data-testid":"price-discount-percent"}).text)
                seller_info["price_before_discount"] = self.safe_extraction('Price before discount', seller, lambda e: e.find('span',{'class':'line-through text-body-2 ml-1 text-neutral-300'}).text)
                seller_info["final_price"] = self.check_with_multi_class_name(seller,'final price','span','class',class_combinations)
                other_sellers.append(seller_info)
            self.log.info('[+] other seller extraction successfully')
            return other_sellers
        else : return []

    def similar_products_extraction(self,element):
        """
         Extracting information of similar products .
         
         Args :
             element : HtmlElementObject that contain all similar products.
             
         Returns :
                 List of Dictionaries each dictionary represent one similar products name, price etc ...
        
        """
        if isinstance(element ,(Tag, ResultSet)):
            similar_products = []
            for product in element:
                similar_products_info={}
                similar_products_info["product_link"] = 'https://www.digikala.com' + self.safe_extraction('product link', product, lambda e: e["href"])
                similar_products_info["product_name"] = self.safe_extraction('product name', product, lambda e: e.find('h3').text)
                similar_products_info["final_price"] = self.safe_extraction('final price', product, lambda e: e.find('span',{"data-testid":"price-final"}).text)
                similar_products_info["product_stockproduct"] = self.safe_extraction('prdouct stock', product, lambda e: e.find('p',{"class":"text-caption text-primary-700"}).text)
                similar_products_info["discount_percent"] = self.safe_extraction('discount percent', product, lambda e: e.find('span',{'data-testid':"price-discount-percent"}).text)
                similar_products_info["price_before_discount"] = self.safe_extraction('price before discount', product, lambda e: e.find('span',{'data-testid':"price-no-discount"}).text)
                similar_products.append(similar_products_info)
            self.log.info('[+] similar products extraction successfully')
            return similar_products
        else :
            return []  
          
    def related_videos_extraction(self,element):
        """
         Extracting information of related videos review.
         
         Args :
             element : HtmlElementObject that contain all related videos review.
             
         Returns :
                 List of Dictionaries each dictionary represent one related videos review name, etc ...
        
        """
        if isinstance(element ,(Tag, ResultSet)):
            related_videos = []
            for video in element:
                related_videos_info = {}
                related_videos_info["video_title"] = self.safe_extraction('video title', video.parent, lambda e: e.find('div',{'class','mt-2 text-body-1 inline-block ellipsis overflow-hidden whitespace-nowrap styles_MagnetPostCard__title__8g7dy'}).text)
                related_videos_info["producer"] = self.safe_extraction('producer', video.parent, lambda e: e.find('span',{'class','mr-2 text-neutral-400 text-body-2'}).text)
                related_videos_info["producer_link"] = 'https://www.digikala.com' +  self.safe_extraction('producer link', video.parent, lambda e: e.find('a',{'class','styles_Link__RMyqc'})["href"]) 
                related_videos_info["thumbnail"] = self.safe_extraction('thumbnail', video, lambda e: e.find('img',{'class','w-full inline-block'})["src"])
                related_videos.append(related_videos_info)
            self.log.info('[+] related videos extraction successfully')
            return related_videos
        else : return []

    def expert_check_box_extraction(self,element):
        """
         Extracting information about the experts check box from the page.
         
         Args : 
             element : HtmlElementObject that contain all experts checkboxes.
             
         Returns :
                 A list contains names of checked experts .
        
        """
        if isinstance(element ,(Tag, ResultSet)):
            expert_check = []
            for expert in element.find_all('section'):
                expert_check_info = {}
                expert_check_info["titles"] = self.safe_extraction('titles', expert, lambda e: e.find('p',{'class':'grow text-h5 text-neutral-900'}).text)
                expert_check_info["expert_text"] = self.safe_extraction('expert text', expert, lambda e: e.find('p',{'class':'text-body-1 text-neutral-800'}).text)
                if expert_check_info["expert_text"] == '' :
                    expert_check_info["expert_text"] = self.safe_extraction('expert text', expert, lambda e: e.find('img',{'class':'w-full lg:block sm:block xs:block inline-block'})['src'])
                expert_check.append(expert_check_info)
            self.log.info('[+] expert check extraction successfully')
            return expert_check
        else :
            return []
        
    def specifications_box_extraction(self,element):
        """
         Extracting information about the product specification from the page.
         
         Args :  
             element : HtmlElementObject that contain all specs.
             
         Returns :
                 A dictionary contains key and value pairs of each specs.
        
        """
        if isinstance(element ,(Tag, ResultSet)):
            specifications= {}
            for ele in element:
                spec_list = []
                main_title = ele.find('p',{'class':'w-full lg:ml-12 text-h5 text-neutral-700 shrink-0 mb-3 lg:mb-0 styles_SpecificationBox__title__ql60s'}).text
                box = ele.find_all('div',{'class':'w-full flex last styles_SpecificationAttribute__valuesBox__gvZeQ'})
                for i in box : 
                    title = i.find('p',{'class':'ml-4 text-body-1 text-neutral-500 py-2 lg:py-3 lg:p-2 shrink-0 styles_SpecificationAttribute__value__CQ4Rz'}).text
                    speci = i.find_all('p',{'class':'flex items-center w-full text-body-1 text-neutral-900 break-words'})
                    sep = []
                    for item in speci : 
                        sep.append(item.text.replace('\n\n','').replace('\r',''))
                    spec_list.append({self.clean_text(title).replace('\n\n',''):self.clean_text(sep)})
                specifications[main_title] = spec_list
            return specifications
        else : return {}

    def reviews_box_extraction(self,element):
        """
         Extracting review data from the page.

         Args:
            element : HtmlElementObject  that contain all reviews.

         Return:
               List of dictionaries with keys as 'username', 'date' and 'review'.
        
        """
        class_combinations_review_title = [
                                            'inline-block  text-caption-strong', 
                                            'text-neutral-900 text-h5 pb-3',
                                          ]
        class_combinations_review_dislike = [
                                            'dp-question-dislike',
                                            'pdp-comment-dislike',
                                          ]
        class_combinations_review_like = [
                                            'dp-question-like',
                                            'pdp-comment-like',
                                          ]
        if isinstance(element ,(Tag, ResultSet)):
            review_data = []
            for reivew in element:
                review_info = {}
                review_info["user_rating"] = self.safe_extraction('user rating', reivew, lambda e: e.find('div',{'class':'p-1 rounded-small text-caption-strong text-neutral-000 flex justify-center items-center px-2 bg-rating-4-5 styles_commentRate__main__YKGC5'}).text)            
                review_info["review_date"] = self.safe_extraction('review date', reivew, lambda e: e.find('p',{'class':'text-caption text-neutral-400 inline'}).text)   
                review_info["user_role"]  = self.safe_extraction('review date', reivew, lambda e: e.find('div',{'class':'inline-flex items-center mr-2 Badge_Badge__QIekq Badge_Badge--small__ElV6O px-2 text-caption-strong'}).text) 
                review_info["review_offer"] = self.safe_extraction('review offer', reivew, lambda e: e.find('p',{'class':'text-body-2'}).text)            
                review_info["review_comment"] = self.safe_extraction('review comment', reivew, lambda e: e.find('p',{'class':'text-body-1 text-neutral-900 mb-1 pt-3 break-words'}).text)  
                review_info["review_seller"] = self.safe_extraction('review seller', reivew, lambda e: e.find('p',{'class':'text-caption text-neutral-700 inline'}).text)
                review_info["review_color"] = self.safe_extraction('review color', reivew, lambda e: e.find('div',{'class':'ml-2 inline-block rounded-circle styles_PdpCommentContentFooter__purchasedItem--color__GOLKc'}).parent.text.replace(review_info["review_seller"],''))
                review_feedback = self.safe_extraction('review feedback', reivew, lambda e: e.find_all('div',{"class":"flex items-center pt-2px"}))
                review_info["review_feedback"] = [
                f"{'+' if 'var(--color-icon-rating-4-5)' in feedback.find('svg')['style'] else '-'} {feedback.text.replace('n','')}".replace('\n','')
                for feedback in review_feedback]
                review_info['review_title'] = self.check_with_multi_class_name(reivew,'review title','p','class',class_combinations_review_title)
                review_info['review_like'] = self.check_with_multi_class_name(reivew,'review like','button','data-cro-id',class_combinations_review_like)
                review_info['review_dislike'] = self.check_with_multi_class_name(reivew,'review dislike','button','data-cro-id',class_combinations_review_dislike)
                review_data.append(review_info)
            self.log.info('[+] review info extraction successfully')
            return review_data
        else : return []

    def  question_box_extraction(self,element):
        """
         Extracting question data from the page.

         Args:
             element : HtmlElementObject  that contain questions.
             
         Returns:
                 Dictionay containing key value pairs of question number and its corresponding answer.
        
        """
        class_combinations_question_dislike = [
                                            'dp-question-dislike',
                                            'pdp-comment-dislike',
                                          ]
        class_combinations_question_like = [
                                            'dp-question-like',
                                            
                                            'pdp-comment-like',
                                          ]
        if isinstance(element ,(Tag, ResultSet)):

            questions = []
            for quest in element:
                question_info = {}
                question_info["question_title"] = self.safe_extraction('question title', quest, lambda e: e.find('p',{'class':'text-subtitle w-full'}).text)     
                question_info["question_answer"] = self.safe_extraction('question answer', quest, lambda e: e.find('p',{'class':'text-body-1'}).text)
                question_info["answer_user_name"] = self.safe_extraction('answer user name', quest, lambda e: e.find('p',{'class':'text-caption text-neutral-400'}).text)
                question_info["answer_user_role"] = self.safe_extraction('answer user role', quest, lambda e: e.find('p',{'class':'inline-block  text-caption-strong'}).text)         
                question_info["question_like"] = self.check_with_multi_class_name(quest,'question like','button','data-cro-id',class_combinations_question_like)
                question_info["question_dislike"] = self.check_with_multi_class_name(quest,'question dislike','button','data-cro-id',class_combinations_question_dislike)
                questions.append(question_info)
            self.log.info('[+] question info extraction successfully')
            return questions
        else : return []

    def also_bought_items_extraction(self,element):
        """
         Extracting "also bought" items from the product description page.

         Args:
             element : HtmlElementObject  that contains "also bought" items.

         Returns:
                 List of item names which are also bought with the main item.

        
        """
        if isinstance(element ,(Tag, ResultSet)):
            also_bought_items = []
            for item in element :
                also_bought_item_info = {}
                also_bought_item_info["also_bought_item_title"] = self.safe_extraction('also bought item title', item, lambda e: e.find('h3').text)
                also_bought_item_info["also_bought_item_image"] = self.safe_extraction('also bought item link', item, lambda e: e.find('img')["src"])
                also_bought_item_info["also_bought_item_link"] = 'https://www.digikala.com'+ self.safe_extraction('also bought item image', item, lambda e: e["href"])
                also_bought_item_info["also_bought_item_final_price"] = self.safe_extraction('also bought item final price', item, lambda e: e.find('span',{"data-testid":"price-final"}).text)
                also_bought_item_info["also_bought_item_discount_percent"] = self.safe_extraction('also bought item discount percent', item, lambda e: e.find('span',{"data-testid":"price-no-discount"}).text)    
                also_bought_item_info["also_bought_item_price_before_discount"] = self.safe_extraction('also bought item price before discount', item, lambda e: e.find('span',{"data-testid":"price-no-discount"}).text)
                also_bought_items.append(also_bought_item_info)
            self.log.info('[+] also bought items extraction successfully')
            return also_bought_items
        else : return []

    def seller_offer_extraction(self,element):
        """
         Extracting "seller offer" items from the product description page.

         Args:
             element : HtmlElementObject  that contains "seller offer" items.

         Returns:
                Dictionary  containing information about the seller offers on the products.
        
        """
        if isinstance(element ,(Tag, ResultSet)):
            seller_offers_items = []
            for offer in element:
                seller_offers_info = {}
                seller_offers_info["seller_offers_title"] = self.safe_extraction('seller offers title', offer, lambda e: e.find('h3').text)
                seller_offers_info["seller_offers_image"] = self.safe_extraction('seller offers link', offer, lambda e: e.find('img',{'class':'w-full rounded-medium inline-block'})["src"])
                seller_offers_info["seller_offers_link"] = 'https://www.digikala.com'+ self.safe_extraction('seller offers image', offer, lambda e: e["href"])
                seller_offers_info["seller_offers_final_price"] = self.safe_extraction('seller offers final price', offer, lambda e: e.find('span',{"data-testid":"price-final"}).text)
                seller_offers_info["seller_offers_discount_percent"] = self.safe_extraction('seller offers discount percent', offer, lambda e: e.find('span',{"data-testid":"price-discount-percent"}).text)
                seller_offers_info["seller_offers_price_before_discount"] = self.safe_extraction('seller offers price before discount', offer, lambda e: e.find('span',{"data-testid":"price-no-discount"}).text)
                seller_offers_items.append(seller_offers_info)
            return seller_offers_items
        else : return []

    def page_extraction(self,prdouct_id,prdouct_url):
        """
         This method extracts all relevant data from a single webpage.

         Args:
             prdouct_id   : String representing the unique id of the product .
                           It's used to store the extracted data into the database.
             prdouct_url  : String representing the url of the product page.

         Returns:
                     A dictionary containing all the extracted data from the web page.
        
        """
        soup = self.driver.get_page_source()
        elements = self.product_elements_extraction(soup)
        seller_id = self.driver.get_seller_id()
        main_product_details = self.clean_text(self.main_product_details_extraction(elements["main_product_details"]))
        buy_box = self.clean_text(self.product_buy_box_extraction(elements["buy_box"]))
        product_images = self.clean_text(self.product_image_extraction(elements["image_box"]))
        other_seller = self.clean_text(self.other_seller_box_extraction(elements["other_seller_box"]))
        similar_products = self.clean_text(self.similar_products_extraction(elements["similar_products"]))
        related_videos = self.clean_text(self.related_videos_extraction(elements["related_videos"]))
        introduction_box = self.clean_text(elements["introduction_box"])
        expert_check = self.clean_text(self.expert_check_box_extraction(elements["expert_check_box"]))
        specifications_box = self.clean_text(self.specifications_box_extraction(elements["specifications_box"]))
        reviews = self.clean_text(self.reviews_box_extraction(elements["reviews_box"]))
        question_box = self.clean_text(self.question_box_extraction(elements["question_box"]))
        also_bought_items = self.clean_text(self.also_bought_items_extraction(elements["also_bought_items"]))
        seller_offer = self.clean_text(self.seller_offer_extraction(elements["seller_offer"]))

        prodcut_info= {
                    'id' : self.db_handler.get_next_id(table_name='products_extraction',fields_id=prdouct_id,id_name='product_id'),
                    'crawl_date' : strftime("%Y-%m-%d %H:%M:%S", gmtime()),     
                    'product_id' : prdouct_id,
                    'seller_id' : seller_id,
                    'seller_name': self.safe_extraction('seller name',elements["buy_box"] ,lambda e: e.find('p',{'class':'text-neutral-700 ml-2 text-subtitle'}).text),
                    'categories' : elements['categories'],
                    'product_link' : prdouct_url,
                    'product_title' : main_product_details["product_title"] ,
                    'product_main_title' : self.check_not_empity(main_product_details["product_main_title"]) ,
                    'user_review' : main_product_details["user_review"] ,
                    'insurer' : main_product_details["insurer"] ,
                    'Insurance_discount_percent' : main_product_details["Insurance_discount_percent"] ,
                    'Insurance_price_before_discount' : main_product_details["Insurance_price_before_discount"] ,
                    'Insurance_final_price' : main_product_details["Insurance_final_price"] ,
                    'Other_sellers_for_this_product' : self.check_not_empity(buy_box["other_sellers"]) , 
                    'satisfaction_with_the_product' : buy_box["satisfaction_with_the_product"] , 
                    'warranty' : buy_box["warranty"] , 
                    'digiclub_points' : buy_box["digiclub_points"] , 
                    'discount_percent' : buy_box["discount_percent"] , 
                    'price_before_discount' : buy_box["price_before_discount"] , 
                    'final_price' : buy_box["final_price"] , 
                    'product_stock' : buy_box["product_stock"] , 
                    "product_image" : product_images,
                    "other_seller" : self.check_not_empity(other_seller),
                    "similar_products" : self.check_not_empity(similar_products),
                    "related_videos" : self.check_not_empity(related_videos),
                    "introduction_box" : self.check_not_empity([introduction_box]),
                    "expert_check" : self.check_not_empity(expert_check),
                    "specifications_box" : self.check_not_empity(specifications_box),
                    "reviews" : self.check_not_empity(reviews),
                    "question_box" : self.check_not_empity(question_box),
                    "also_bought_items" : self.check_not_empity(also_bought_items),
                    "seller_offer" : self.check_not_empity(seller_offer),
            }
        
        self.db_handler.update_database(data=prodcut_info,column_name='product_id',table_name='products_extraction')

    def check_not_empity(self,data):
        """
         This method help to find if any field are empity 

         Args :
             data :  It is the value of a particular key in dictionary .
         
         Returns :
              If the value of the key is not empty then it will return the value otherwise it will return 0.
        
        """
        if isinstance(data,str) and len(data)== 0:
            return '0'
        elif isinstance(data,list) and len(data)== 0:
            return['0']
        else:
            return data 
    def run(self,url):          
        self.driver.load_page(url)
        ids = url.split('/')[4]
        self.page_extraction(ids,url)
        
    # TODO :
    # Currently, 20 items are received in reviews and questions. To get more items, if available, 
            # get first page items click on the next page button get source and add it to temp in loop  
                # source_code = driver.source_code ->
                  # get_next_review/question_button ->
                    # click on button -> 
                      # source_code += driver.source_code ->
                        # send for extraction

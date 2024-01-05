from bs4 import BeautifulSoup

# use this file to find seller info (to do not make spam request)

with open('soucre.html','r',encoding='utf-8') as file :
    page= file.read()

def has_desired_text(tags,find_text):
    for element in tags:
        if find_text in element.text :
            return element

soup = BeautifulSoup(page,'html.parser')

seller_details = {
    'seller_name':soup.find('h1',{'class':'text-h5 text-neutral-900 whitespace-nowrap'}).text,
    'seller_Membership_period':soup.find('div',{'class':'w-full flex flex-col mr-5'}).find('p',{'class':'text-body-2'}).text,
    'seller_Satisfaction_with_the_goods':soup.find('p',string='رضایت از کالاها').find_parent('div').find('p').text,
    'Seller_performance':soup.find('p',string='عملکرد فروشنده').find_parent('div').find('p').text,
    
}

seller_more_details = {'People have given points':has_desired_text(soup.find_all('p',),'نفر امتیاز داده‌اند').string.replace('نفر امتیاز داده‌اند',''),
                      'timely supply':soup.find('p', string='تامین به موقع').find_previous_sibling('p').string,
                      'Obligation to send':soup.find('p', string='تعهد ارسال').find_previous_sibling('p').string,
                      'No return':soup.find('p', string='بدون مرجوعی').find_previous_sibling('p').string,
                      'Introduction of the seller':soup.find('span',string='معرفی فروشنده').find_parent('div').find_parent('div').find_next_sibling('div').text,
                      }



products = soup.find_all('div',{'class':'product-list_ProductList__item__LiiNI'})
for product in products:
    img_element = product.find('picture').find('img', {'class': 'w-full rounded-medium inline-block'})
    rate_element = product.find('div',{'class':'mb-1 flex items-center justify-between'}).find('p',{'class':'text-body2-strong text-neutral-700'})
    price_element = product.find('span',{'data-testid':'price-final'})
    price_discount_percent_element = product.find('span',{'data-testid':'price-discount-percent'})
    element_price_discount = product.find('div',{'data-testid':'price-no-discount'})
    try:
        product_special_sale = 'special sale' if 'SpecialSell.svg' in (product.find('div', {'class': 'flex items-center justify-start mb-1'}).find('img').get('src', '')) else 'unavailable special sale'
    except AttributeError:
        product_special_sale = 'unavailable special sale'

    product_details = {
        'product_link': "https://www.digikala.com"+product.find('a')['href'],
        'product_image':img_element['src'] if img_element else 'image not found' ,
        'product_rate':rate_element.text if rate_element else 'rate not found',
        'product_name':product.find('h3').text,
        'product_price':price_element.text.replace(',','') if price_element else "unavailable",
        'product_price_discount_percent':price_discount_percent_element.text if price_discount_percent_element else "unavailable discount percent",
        'product_price_discount':element_price_discount.text if element_price_discount else "unavailable discount price" ,
        'product_special_sale':product_special_sale,
        'stock':has_desired_text(product.find('p'),'باقی مانده').replace('تنها ','').replace(' عدد در انبار باقی مانده','') if has_desired_text(product.find('p'),'باقی مانده') else 'Quantity unspecified',
    }
    

   


    
    

    




   

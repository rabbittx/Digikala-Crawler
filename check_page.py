from bs4 import BeautifulSoup

# use this file to find seller info (to do not make spam request)

with open('soucre.html','r',encoding='utf-8') as file :
    page= file.read()



suop = BeautifulSoup(page,'html.parser')

products = suop.find_all('div',{'class':'product-list_ProductList__item__LiiNI'})

seller_name = suop.find('div',{'class':'w-full flex justify-between'}).find('h1',{'class':'text-h5 text-neutral-900 whitespace-nowrap'}).text
seller_Membership_period = suop.find('div',{'class':'w-full flex flex-col mr-5'}).find('p',{'class':'text-body-2'}).text

seller_Satisfaction_with_the_goods = suop.find('div',{'class':'styles_SellerOption__optionItem__M141z'}).find('div').find('p',{'class':'text-h3'}).text
Seller_performance = suop.find('div',{'class':'styles_SellerOption__optionItem__M141z'}).find('div').find('p',{'class':'text-h3'}).text

seller_more_details = {'People have given points':'',
                      'timely supply':'',
                      'Obligation to send':'',
                      'No return':'',
                      'Introduction of the seller':'',
                      }

for product in products:
    product_link = "https://www.digikala.com"+product.find('a')['href']
    img_element = product.find('picture').find('img', {'class': 'w-full rounded-medium inline-block'})
    product_image = img_element['src'] if img_element else 'image not found'  
    rate_element = product.find('div',{'class':'mb-1 flex items-center justify-between'}).find('p',{'class':'text-body2-strong text-neutral-700'})
    product_rate = rate_element.text if rate_element else 'rate not found'
    product_name = product.find('h3').text
    price_element = product.find('span',{'data-testid':'price-final'})
    product_price = price_element.text.replace(',','') if price_element else "unavailable"
    price_discount_percent_element = product.find('span',{'data-testid':'price-discount-percent'})
    product_price_discount_percent = price_discount_percent_element.text if price_discount_percent_element else "unavailable discount percent"
    element_price_discount = product.find('div',{'data-testid':'price-no-discount'})
    product_price_discount = element_price_discount.text if element_price_discount else "unavailable discount price" 
    try:
        element_special_sale = product.find('div', {'class': 'flex items-center justify-start mb-1'}).find('img')
        if element_special_sale and 'SpecialSell.svg' in element_special_sale.get('src', ''):
            product_special_sale = 'special sale'
        else:
            product_special_sale = 'unavailable special sale'
    except AttributeError:
        product_special_sale = 'unavailable special sale'

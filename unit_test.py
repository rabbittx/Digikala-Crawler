from bs4 import BeautifulSoup, ResultSet, Tag
import re

with open('page_source.html','r',encoding='utf-8')as file:
     page_source = file.read()

soup = BeautifulSoup(page_source,'html.parser')


def clean_text( text):
        # تعریف پترن با اضافه کردن \n و \n\n به پترن اصلی
    pattern = '[^ا-یآ-ی۰-۹a-zA-Z0-9\s:/\.\-،%(),\n _]'
        # تابع برای بررسی اینکه آیا یک رشته شبیه به URL است یا نه
    def is_url(s):
        return re.match(r'https?://\S+\.\S+', s)

    if isinstance(text, str):
            # اگر رشته شبیه به URL باشد، بدون تغییر باقی می‌ماند
        if is_url(text):
            return text
            # در غیر این صورت، حذف کاراکترهای ناخواسته
        return re.sub(pattern, '', text.replace('\n','').replace('\n\n','').replace('\r',''))
    elif isinstance(text, list):
            # اعمال تابع بر روی هر عنصر از لیست
        return [clean_text(i) for i in text]
    elif isinstance(text, dict):
            # اعمال تابع بر روی هر مقدار از دیکشنری
        return {k: clean_text(v) for k, v in text.items()}

def safe_find(soup,finds, tag, attrs):
        try:
            if finds == 'find':
                return soup.find(tag, attrs)
            elif finds == 'find_all':
                return soup.find_all(tag, attrs)
        except AttributeError:
            return 'element not found'
    
def safe_extraction(element_name ,element, extraction_function):
        try:
            return extraction_function(element)
        except Exception as e:
            return f'{element_name} not found'


elements ={
'specifications_box': safe_find(soup,'find_all','div',{'class':'flex flex-col lg:flex-row pb-6 lg:py-4 styles_SpecificationBox__main__JKiKI'}),
}

def specifications_box_extrection(element):
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
                
                spec_list.append({clean_text(title).replace('\n\n',''):clean_text(sep)})
            specifications[main_title] = spec_list
        return specifications
    else : return {}

specification = specifications_box_extrection(elements['specifications_box'])

for (k,v) in specification.items() :
    print(k , " : ")
    for j in v:
        for (i,g) in j.items():
            print(i,' : ',g)
    print('-----------')

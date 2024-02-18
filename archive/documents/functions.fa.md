[raed in english](functions.md)

### کلاس ها و توابع 

## `webScriper.py` : 
# مستندات کلاس DigiKalaScraper

کلاس `DigiKalaScraper` برای تسهیل عملیات وب اسکرپینگ در وب‌سایت دیجی‌کالا طراحی شده است. این کلاس با استفاده از اجزای مختلف، اطلاعات مربوط به فروشندگان، محصولات و جزئیات محصولات را استخراج کرده و این داده‌ها را در یک پایگاه داده ذخیره می‌کند. این کلاس همچنین امکاناتی برای صدور داده‌ها به فایل‌های CSV و مدیریت فرآیند وب اسکرپینگ از طریق حالت‌های مختلف را فراهم می‌آورد.

# مقدمه

```python
DigiKalaScraper(config_file_path, log)
```
  - `config_file_path`: مسیر فایل پیکربندی. این فایل تعیین می‌کند که اسکرپر در حالت کنسول یا وب کار کند.
  - `log`: نمونه Logger برای ثبت پیام‌ها در طول فرآیند اسکرپینگ.
  
# متدها 

`_initialize_settings()`

تنظیمات اسکرپر را از فایل پیکربندی مقداردهی اولیه می‌کند. تنظیمات شامل مسیر پایگاه داده، مسیر وب درایور، گزینه حالت بی‌سر و نوع درایور است.

`initialize_driver(geko_path, driver_type, headless_mode, db_handler, logger)`

وب درایور را برای فرآیند اسکرپینگ مقداردهی اولیه می‌کند.
  - `geko_path`: مسیر GeckoDriver.
  - `driver_type`: نوع وب درایور (firefox یا chrome).
  - `headless_mode`: بولین که نشان می‌دهد آیا مرورگر باید در حالت بی‌سر اجرا شود.
  - `db_handler`: نمونه کلاس DataBaseHandler.
  - `logger`: نمونه Logger.

`get_sellers()`

لیست فروشندگان را از پایگاه داده بازیابی می‌کند.

`show_sellers()`

تمام فروشندگان موجود در پایگاه داده را نمایش می‌دهد و اجازه می‌دهد کاربر یک فروشنده را برای اسکرپینگ محصولاتش انتخاب کند.

`check_crawl_url(mode, input_url)`

URL ورودی را بر اساس حالت اسکرپینگ مشخص شده اعتبارسنجی می‌کند.

  - `mode`: حالت اسکرپینگ (SingleProductCrawlMode, SingleSellerCrawlMode, CategoryCrawlMode).
  - `input_url`: URL برای اعتبارسنجی.

`initialize_crawl_for_products(available_products)`

فرآیند اسکرپینگ را برای لیستی از URL‌های محصول مقداردهی اولیه می‌کند.

  - `available_products`: لیست URL‌های محصول برای اسکرپینگ.

`execute_crawl(mode, input_url, scroll_count, seller_info=None)`

فرآیند وب اسکرپینگ را بر اساس حالت و تنظیمات مشخص شده اجرا می‌کند.

  - `mode`: حالت اسکرپینگ.
  - `input_url`: URL نقطه شروع اسکرپ.
  - `scroll_count`: تعداد دفعات اسکرول صفحه (در صورت لزوم).
  - `seller_info`: اطلاعات اختیاری فروشنده برای اسکرپینگ هدفمند.

`remove_old_file(filename)`

یک فایل قدیمی را اگر وجود دارد حذف می‌کند.

  - `filename`: نام فایلی که باید حذف شود.

`save_to_csv(data, headers, filename)`

داده‌ها را به یک فایل CSV صادر می‌کند.

  - `data`: داده‌هایی که باید صادر شوند.
  - `headers`: سرصفحه‌های ستون برای فایل CSV.
  - `filename`: نام فایل CSV.

`export_table(table_name, seller_id=None, condition=None)`

داده‌ها از یک جدول مشخص را به یک فایل CSV صادر می‌کند.

  - `table_name`: نام جدول پایگاه داده.
  - `seller_id`: شناسه فروشنده اختیاری برای فیلتر کردن داده‌ها.
  - `condition`: شرایط اضافی برای فیلتر کردن داده‌ها.

`export_data_to_csv(export_mode, seller_id=None, seller_name=None)`

صدور داده‌ها به فایل‌های CSV را بر اساس حالت مشخص شده مدیریت می‌کند.

  - `export_mode`: حالت صدور داده (all_seller, seller_products و غیره).
  - `seller_id`: شناسه فروشنده اختیاری برای صدور هدفمند.
  - `seller_name`: نام فروشنده اختیاری برای صدور هدفمند.

`database_report()`

گزارشی از محتوای پایگاه داده تولید می‌کند، شامل تعداد فروشندگان، محصولات و اطلاعات استخراج شده.
نمونه استفاده

```python
logger = setup_logger()
scraper = DigiKalaScraper(config_file_path="config/console_config.ini", log=logger)
scraper.execute_crawl(mode="SingleProductCrawlMode", input_url="https://www.digikala.com/product/dkp-12345", scroll_count=3)
```


## `product_details_extractor.py` : 


## `seller_product_data_extractor.py` : 


## `driver_manager.py` : 


## `db_handler.py` : 


## `logger.py` : 


## `console_panel.py` : 


## `app.py` : 


## `TODOS.py` : 


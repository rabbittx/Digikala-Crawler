import argparse
from source.webScraper import DigiKalaScraper

def main():
    parser = argparse.ArgumentParser(description="DigiKala Scraper CLI")
    parser.add_argument("-mode", help="Crawling mode", required=True)
    parser.add_argument("-Url", help="URL to crawl", required=True)
    parser.add_argument("-Out", help="Output file path", required=True)
    
    args = parser.parse_args()
    
    # ایجاد نمونه از کلاس اسکریپر با تنظیمات پیش‌فرض یا بر اساس فایل پیکربندی
    scraper = DigiKalaScraper()
    
    # اجرای منطق بر اساس حالت ورودی
    if args.mode == "single_seller":
        # فرض بر این است که تابع execute_crawl پیاده‌سازی شده و می‌تواند اطلاعات را استخراج و در فایل خروجی ذخیره کند
        scraper.execute_crawl(mode=args.mode, input_url=args.Url, output_file=args.Out)
    
    # می‌توانید منطق مشابهی برای سایر حالت‌ها اضافه کنید

if __name__ == "__main__":
    main()
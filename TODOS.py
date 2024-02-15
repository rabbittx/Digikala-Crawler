# useing this file to show all TODO and BUG , (fixed),(planing to do),(done) 

### DOCUMENTS / README 
# TODO : - [ ] update the readme for new version (GUI) 
# TODO : - [ ] update the documents to show this how this project work and what can be done with it.

# ------------------------------------------------

# TODO : - [ ] add Docker to project (planing to do)


# ------------------------------------------------
### CONFIG 
## web app config

## console config 

# ------------------------------------------------
### PANELS 
# TODO : - [ ] check if there is internet conncetion before starting panel.
## web panel
# BUG : - [ ] When the panel starts working, the report is printed twice, but it is displayed only once in the rest of the program
## console panel 
# TODO : - [x] add option to reset the setting and reconfig everything . (FIXED) 


# ------------------------------------------------
### db_handler.py
# BUG : - [x] get_next_id need to be same when data need to replace with historyical table . ( updated need to check ids print(id) added for check ids value ) (FIXED) 

# ------------------------------------------------
### driver_manager.py
# TODO : - [ ] check for 404,503 pages and product not available page on open_page()
# TODO : - [ ] befor get page_source in driver_manager need to check if products in loading... with to it get load 
# TODO : - [ ] with full scrolling on seller page get products of 10 page at once need to add for more pages to get all products from seller


# ------------------------------------------------
### logger 

# ------------------------------------------------
### products_details_extractor.py

# TODO : - [ ]
    # Currently, 20 items are received in reviews and questions. To get more items, if available, 
            # get first page items click on the next page button get source and add it to temp in loop  
                # source_code = driver.source_code ->
                  # get_next_review/question_button ->
                    # click on button -> 
                      # source_code += driver.source_code ->
                        # send for extraction , (planing to do)


# ------------------------------------------------
### seller_product_data_extractor.py

# ------------------------------------------------
### webScraper.py
# TODO : - [ ] regex patterns need to get updated to check if link is valid => eq : link start with https(fixed),url split tokens length etc ...
# TODO : - [x] all mode name need to get update in all script files . (fixed)


# ------------------------------------------------

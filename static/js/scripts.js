
function validateForm() {
    var dbPath = document.forms["settingsForm"]["dbPath"].value;
    var gekoPath = document.forms["settingsForm"]["gekoPath"].value;

    if (dbPath == "" || dbPath == null) {
        alert("DB Path must be filled out");
        return false; 
    }
    if (gekoPath == "" || gekoPath == null) {
        alert("gekoPath must be filled out");
        return false; 
    }

    return true;
}


function showHelpPopup() {
    document.getElementById('helpPopup').style.display = 'block';
}

function hideHelpPopup() {
    document.getElementById('helpPopup').style.display = 'none';
}

function startWebScraping(mode) {
    if(mode === 'category') {
        const categoryUrl = document.getElementById('categorycrawl').value;
        const scrollCount = document.getElementById('scrollCount').value;
        fetch('/start-category-crawl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `categorycrawl=${encodeURIComponent(categoryUrl)}&scrollCount=${encodeURIComponent(scrollCount)}`
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }
    else if(mode === 'single_seller') {
        const categoryUrl = document.getElementById('single_seller_url_crawl').value;
        fetch('/start_single_seller', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `single_seller_url_crawl=${encodeURIComponent(categoryUrl)}`
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }
    else if(mode === 'single_seller_products') {
        const categoryUrl = document.getElementById('single_seller_products_id').value;
        fetch('/start_single_product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `single_seller_products_id=${encodeURIComponent(categoryUrl)}`
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }
    else if(mode === 'single_product') {
        const categoryUrl = document.getElementById('single_product_url').value;
        fetch('/single_prdoucts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `single_product_url=${encodeURIComponent(categoryUrl)}`
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }
    else if(mode === 'all_products') {
        fetch('/all_products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }





}
$(document).ready(function(){
$("#category_form").submit(function(e){
    e.preventDefault(); // جلوگیری از ارسال معمولی فرم
    $.ajax({
        type: "POST",
        url: "/start-category-crawl",
        data: $(this).serialize(), // ارسال داده‌های فرم
        success: function(response){
            if(response.status === "succsue"){
                $("#category_submit").prop('disabled', true); // غیرفعال کردن دکمه
                alert(response.message); // نمایش پیام موفقیت
            } else {
                alert(response.message); // نمایش پیام خطا
            }
        }
    });
});

$("#single_product_form").submit(function(e){
    e.preventDefault(); // جلوگیری از ارسال معمولی فرم
    $.ajax({
        type: "POST",
        url: "/single_prdoucts",
        data: $(this).serialize(), // ارسال داده‌های فرم
        success: function(response){
            if(response.status === "succsue"){
                $("#single_product_submit").prop('disabled', true); // غیرفعال کردن دکمه
                alert(response.message); // نمایش پیام موفقیت
            } else {
                alert(response.message); 
            }
        }
    });
});


});



function export_data(mode) {
    if(mode === 'all_seller') {
        fetch('/export_all_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }
    else if(mode === 'seller_products') {
        const seller_info = document.getElementById('seller_products_export').value
        fetch('/export_seller_products_id', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `seller_products_export=${encodeURIComponent(seller_info)}`
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }
    else if(mode === 'all_products') {
        fetch('/export_all_products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }

}
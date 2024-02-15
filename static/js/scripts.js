
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

// TODO : need to disable all button when driver is activate  and enable it after the process complete 
$(document).ready(function(){
$("#category_form").submit(function(e){
    e.preventDefault(); 
    $.ajax({
        type: "POST",
        url: "/start-category-crawl",
        data: $(this).serialize(), 
        success: function(response){
            if(response.status === "success"){
                $("#category_submit").prop('disabled', true);
                alert(response.message);
            } else {
                alert(response.message); 
            }
        }
    });
});

$("#single_product_form").submit(function(e){
    e.preventDefault(); 
    $.ajax({
        type: "POST",
        url: "/single_prdoucts",
        data: $(this).serialize(), 
        success: function(response){
            if(response.status === "success"){
                $("#single_product_submit").prop('disabled', true); 
                alert(response.message); 
            } else {
                alert(response.message); 
            }
        }
    });
});


});
function export_data(mode) {
    if(mode === 'all_seller') {
        fetch('/export_all_seller_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }
    else if(mode === 'export_seller_products_id') {
        const seller_info = document.getElementById('export_seller_products_id').value
        fetch('/export_seller_products_id', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `export_seller_products_id=${encodeURIComponent(seller_info)}`

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
    else if(mode === 'seller_products_specification_id') {
        const seller_info = document.getElementById('seller_products_specification_id').value;
        fetch('/seller_products_specification_id', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `seller_products_specification_id=${encodeURIComponent(seller_info)}`

        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }

    else if(mode === 'all_products_with_specifications') {
        fetch('/export_all_sellers_products_with_all_specifications', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },

        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }
    else if(mode === 'all_table_data') {
        fetch('/export_all_table_data', {
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
function data_reports() {
    fetch('/report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === "success") {
            document.getElementById("seller_count").textContent = `${data.data.seller_count} sellers in the table.`;
            document.getElementById("product_count").textContent = `${data.data.product_count} products in the table.`;
            document.getElementById("products_extrection_count").textContent = `${data.data.products_extrection_count} products with all specifications in the table.`;
            document.getElementById("seller_historical_count").textContent = `${data.data.seller_historical_count} historical sellers in the table.`;
            document.getElementById("products_historical_count").textContent = `${data.data.products_historical_count} historical products in the table.`;
            document.getElementById("products_extrection_historical_count").textContent = `${data.data.products_extrection_historical_count} products with all specifications in the historical table.`;
        } else {
            console.error('Error:', data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}


function fetchLogs() {
    fetch('/get-logs')
    .then(response => response.text())
    .then(data => {
        const lines = data.split('\n');  
        const lastLines = lines.slice(-10);  
        const formattedLogs = lastLines.join('<br>');
        document.getElementById('live-logs').innerHTML = formattedLogs;
    })
    .catch(error => console.error('Error fetching logs:', error));
}    
    setInterval(fetchLogs, 5000);

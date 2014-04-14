/**
 * Created by drain on 04.04.14.
 */
function validateInput(input){
    var regExp = /^[0-9]+$/;
    var match = regExp.test(input);
    if(match){
        // zero is also bad
        var result = parseInt(input);
        return result > 0;
    } else {
        return false
    }
}

function highlightCart(status){
    if (status === "ok"){
        $('#cart').addClass('summ_active')
    }
}

function addItemToCart(license_code){
    var quantity = $('#' + license_code).val();
    if(validateInput(quantity)){
        $.ajax({
            type: "POST",
            url: '/payment/cart/',
            data: {
                license_code: license_code,
                quantity: parseInt(quantity)
            },
            success: function(json){
                highlightCart(json.status)
            },
            dataType: "json"
        });
    }
    else{
        alert("bad input");
    }
}

function deleteItem(license_code){
    $.ajax({
        type: "POST",
        url: '/payment/cart/',
        data: {
            license_code: license_code,
            quantity: -1
        },
        success: function(json){
            alert(json)
        },
        dataType: "json"
    })
}
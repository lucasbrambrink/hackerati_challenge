/**
 * Created by lb on 4/29/15.
 */
function getCSRF(){
    var csrf_token = $.cookie('csrftoken');
    if (!csrf_token || csrf_token.length == 0){
        csrf_token = $('#csrf-token').text();
    }
    return csrf_token;
}

function AJAXsignalEnd(auctionID) {

    var data = {'auction_id': auctionID };

    $.ajax({
        type: 'POST',
        url: '/auction/auction/ending/',
        data: {
            csrfmiddlewaretoken: getCSRF(),
            data: JSON.stringify(data)
        },
        success: function (data) {
            console.log('success');
            $('#auction-' + id).remove();
            $('#auction-thumb-' + id).remove();
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });

}

function AJAXimportItemsFromCraigslist(import_type, query) {

    var data = {'import_type': import_type, 'query': query};

    $('.loading-div').css('visibility', 'visible');
    $.ajax({
        type: 'POST',
        url: '/auction/item/import/',
        data: {
            csrfmiddlewaretoken: getCSRF(),
            data: JSON.stringify(data)
        },
        success: function (data) {
            console.log('success');
            setTimeout(function(){
                location.reload();
            }, 5000)
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });
}

function AJAXcreateNewAuction(type, duration) {

    var data = {'type': type, 'duration': duration};

    $.ajax({
        type: 'POST',
        url: '/auction/auction/create/',
        data: {
            csrfmiddlewaretoken: getCSRF(),
            data: JSON.stringify(data)
        },
        success:     function (data) {
            console.log('success');
            location.reload();
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });


}

function AJAXcreateBid($highestBid, bidAmount, auctionID) {
    var data = { 'amount': bidAmount, 'id': auctionID };

    $.ajax({
        type: 'POST',
        url: '/auction/bid/create/',
        data: {
            csrfmiddlewaretoken: getCSRF(),
            data: JSON.stringify(data)
        },
        success: function (data) {
            var col1 = "<td>" + data['price'] + "</td>",
                col2 = "<td>" + data['username'] + "</td>",
                col3 = "<td>" + data['time'] + "</td>";
            var $tableBids = $('.current-bid-info-' + auctionID);

            console.log($tableBids);
            $tableBids.prepend("<tr>" + col1 + col2 + col3 + "</tr>");
            $highestBid.html(data['price']);

            $('#user-balance').html(data['balance']);
            console.log('success')
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });
}

function AJAXremoveItem(itemID) {

    var data = {'item_id': itemID};

    $.ajax({
        type: 'POST',
        url: '/auction/item/delete/',
        data: {
            csrfmiddlewaretoken: getCSRF(),
            data: JSON.stringify(data)
        },
        success: function (data) {
            var identifier = '#inventory-' + itemID;
            $(identifier).remove();

            console.log('success')
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });
}

function AJAXinitiateAuction(itemID, duration) {
    var data = {'item_id': itemID, 'duration': duration};

    $.ajax({
        type: 'POST',
        url: '/auction/item/init/',
        data: {
            csrfmiddlewaretoken: getCSRF(),
            data: JSON.stringify(data)
        },
        success: function (data) {
            location.reload();
            alert("Item offered for Auction!");

            console.log('success')
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });
}

function AJAXfetchGraphingData(itemID, duration) {

    $.ajax({
        type: 'GET',
        url: '/auction/auction/graph/',
        success: function (data) {
            console.log(data);
            auctionData('chart-container', data['auction_data'], data['inventory_data'])
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });
}

function AJAXtestUserCredentials(username, password) {
    var data = { 'username': username, 'password': password };

    $.ajax({
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCSRF(),
            data: JSON.stringify(data)
        },
        url: '/on-boarding/user/info/',
        success: function (data) {
            var data = data['data'];
            console.log(data);
            if (data['credential'] == 'username' && data['valid']){
                var $question = $('.pt-page-2').find('.question');
                $question.html('please enter your password');
                $('#password').addClass('validate')
            } else if (data['credential'] == 'password' && data['valid']){
                var $page = $('.pt-page-3')
                $page.find('.question').html('<br>Welcome back!');
                $page.find('input').css('display', 'none').css('visibility', 'hidden');
                // skip to last page
                $('#password').addClass('validated')
            } else if (data['credential'] == 'password' && !data['valid']){
                // stay on password
                $('.pt-page-2').find('.question').html('Password Invalid. Try Again!');
                setTimeout(function(){$('.trigger-prev').click()}, 1000);
                $('#password').addClass('invalid');
            }

            console.log(data);


        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });
}

function AJAXcreateNewItemManually() {
    var data = {};
    $('.create-new-item-form').each(function(){
        var $this = $(this);
        var type = $this.attr('name');
        data[type] = $this.val();
    });

    $.ajax({
        type: 'POST',
        url: '/auction/item/new/',
        data: {
            csrfmiddlewaretoken: getCSRF(),
            data: JSON.stringify(data)
        },
        success: function (data) {
            location.reload();
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });



}
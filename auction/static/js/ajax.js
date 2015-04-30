/**
 * Created by lb on 4/29/15.
 */


function AJAXsignalEnd(auctionID) {

    var data = {'auction_id': auctionID };

    var csrf_token = $.cookie('csrftoken');
    if (!csrf_token || csrf_token.length == 0){
        csrf_token = $('#csrf-token').text();
    }
    $.ajax({
        type: 'POST',
        url: '/auction/auction/ending/',
        data: {
            csrfmiddlewaretoken: csrf_token,
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
    var csrf_token = $.cookie('csrftoken');
    if (!csrf_token || csrf_token.length == 0){
        csrf_token = $('#csrf-token').text();
    }
    $('.loading-div').css('visibility', 'visible');
    $.ajax({
        type: 'POST',
        url: '/auction/item/import/',
        data: {
            csrfmiddlewaretoken: csrf_token,
            data: JSON.stringify(data)
        },
        success: function (data) {
            console.log('success');
            $('.loading-div').css('visibility', 'hidden');
            location.reload();
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });
}

function AJAXcreateNewAuction(type, duration) {

    var data = {'type': type, 'duration': duration};
    var csrf_token = $.cookie('csrftoken');
    if (!csrf_token || csrf_token.length == 0){
        csrf_token = $('#csrf-token').text();
    }
    $.ajax({
        type: 'POST',
        url: '/auction/auction/create/',
        data: {
            csrfmiddlewaretoken: csrf_token,
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
    var csrf_token = $.cookie('csrftoken');
    if (!csrf_token || csrf_token.length == 0){
        csrf_token = $('#csrf-token').text();
    }
    $.ajax({
        type: 'POST',
        url: '/auction/bid/create/',
        data: {
            csrfmiddlewaretoken: csrf_token,
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
    var csrf_token = $.cookie('csrftoken');
    if (!csrf_token || csrf_token.length == 0){
        csrf_token = $('#csrf-token').text();
    }
    console.log(data)
    $.ajax({
        type: 'POST',
        url: '/auction/item/delete/',
        data: {
            csrfmiddlewaretoken: csrf_token,
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
    console.log(data)
    var csrf_token = $.cookie('csrftoken');
    if (!csrf_token || csrf_token.length == 0){
        csrf_token = $('#csrf-token').text();
    }
    $.ajax({
        type: 'POST',
        url: '/auction/item/init/',
        data: {
            csrfmiddlewaretoken: csrf_token,
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
    console.log(data);

    var csrf_token = $.cookie('csrftoken');
    if (!csrf_token || csrf_token.length == 0){
        csrf_token = $('#csrf-token').text();
    }
    console.log(csrf_token)
    $.ajax({
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrf_token,
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

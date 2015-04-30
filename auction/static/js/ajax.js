/**
 * Created by lb on 4/29/15.
 */


function AJAXsignalEnd(auctionID) {

    var data = {'auction_id': auctionID };

    $.ajax({
        type: 'POST',
        url: '/auction/auction/ending/',
        data: {
            csrfmiddlewaretoken: $.cookie('csrftoken'),
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
        url: '/auction/auction/import/',
        data: {
            csrfmiddlewaretoken: $.cookie('csrftoken'),
            data: JSON.stringify(data)
        },
        success: function (data) {
            console.log('success');
            $('.loading-div').css('visibility', 'hidden');
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
            csrfmiddlewaretoken: $.cookie('csrftoken'),
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
            csrfmiddlewaretoken: $.cookie('csrftoken'),
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
    console.log(data)
    $.ajax({
        type: 'POST',
        url: '/auction/item/delete/',
        data: {
            csrfmiddlewaretoken: $.cookie('csrftoken'),
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

    $.ajax({
        type: 'POST',
        url: '/auction/item/init/',
        data: {
            csrfmiddlewaretoken: $.cookie('csrftoken'),
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

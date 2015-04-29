/**
 * Created by lb on 4/29/15.
 */


function AJAXsignalEnd(import_type) {

    var data = {'id': id, 'import_type': import_type};

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
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });

}

function AJAXimportItemsFromCraigslist(import_type) {

    var data = {'id': id, 'import_type': import_type};

    $.ajax({
        type: 'POST',
        url: '/auction/auction/import/',
        data: {
            csrfmiddlewaretoken: $.cookie('csrftoken'),
            data: JSON.stringify(data)
        },
        success: function (data) {
            console.log('success');
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });

}

function AJAXcreateBid(bidAmount, auctionID) {
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
            console.log('success')
        },
        error: function (xhr, errmsg, err) {
            alert("error");
        }
    });
}

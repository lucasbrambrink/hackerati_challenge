/**
 * Created by lb on 4/27/15.
 */


$(document).ready(function() {

    var seconds = 0;
    setInterval( function(){
        $("#seconds-since-loaded").html(seconds);
        seconds++
    }, 1000);

    setInterval( function() {
        var $active = $('.active-counter');
        var result = decrementCounter($active.text());
        if (!result) {
            var auctionId = $active.attr('id').split('-')[2];
            AJAXsignalEnd(auctionId);
        } else {
            $active.html(decrementCounter($active.text()));
        }

    }, 1000);

    $('.auction-item').hover(function(){
        var auctionID = $(this).context.id.split('-')[2];
        var matchingID = "#auction-" + auctionID;
        var counterId = "#auction-counter-" + auctionID;

        changeEachVisibility('.auction-container', 'hidden');
        $('.chart-container-div').css('display', 'none').css('visibility', 'hidden');

        $('.inventory-container').css('display', 'none');
        $('.counter-cell').each(function() {
            $(this).removeClass('active-counter')
        });

        var $auction = $(matchingID);
        var expiration = $auction.data('seconds-left');
        var counter = createDateObject(expiration);

        $auction.css('visibility', 'visible').css('display', 'block');
        $(counterId).addClass('active-counter').text(counter);
    });


    $('.bid-btn').on('click', function(){
        var $this = $(this);
        var $bidForm = $($this.context.previousElementSibling);
        var bidAmount = $bidForm.val();
        var auctionID = $bidForm.context.className.split(' ')[2].split('-')[2];
        var $highestBid = $('.highest-bid-' + auctionID);
        var highestBid = parseInt($highestBid.text().slice(1));
        var currentBalance = parseFloat($('#user-balance').text().slice(1));
        if (bidAmount && !isNaN(bidAmount) && bidAmount > highestBid && bidAmount <= currentBalance) {
            AJAXcreateBid($highestBid, bidAmount, auctionID);
        }
    });

    $('#view-inventory').on('click', function(){
        changeEachVisibility('.auction-container', 'hidden');
        $('.chart-container-div').css('display', 'none').css('visibility', 'hidden');
        $('.inventory-container').css('display', 'inline').css('visibility', 'visible');
    });

    $('#random-fetch').on('click', function(){
        AJAXimportItemsFromCraigslist('random', null)
    });

    $('#query-fetch').on('click', function(){
        var query = $('#query-term').val();
        AJAXimportItemsFromCraigslist('query', query)
    });

    $('#auction-all').on('click', function(){
        var duration = $('#auction-duration').val();
        AJAXcreateNewAuction('all', duration)
    });

    $('.btn-remove').on('click', function(){
        var itemID = $(this).data('item-id');
        AJAXremoveItem(itemID);
    });

    $('.btn-initiate-auction').on('click', function(){
        var itemID = $(this).data('item-id');
        var duration = $('#auction-duration').val();
        AJAXinitiateAuction(itemID, duration);
    });

    $('#view-graph').on('click', function(){
        $('.inventory-container').css('display', 'none').css('visibility', 'hidden');
        $('.auction-container').css('display', 'none').css('visibility', 'hidden');
        $('.chart-container-div').css('display', 'inline').css('visibility', 'visible');
        $('#chart-container').css('display', 'inline').css('visibility', 'visible');
        AJAXfetchGraphingData();
    })

});

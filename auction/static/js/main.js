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
            signalEnd(auctionId);
        } else {
            $active.html(decrementCounter($active.text()));
        }

    }, 1000);

    $('.auction-item').hover(function(){
        var auctionID = $(this).context.id.split('-')[2];
        var matchingID = "#auction-" + auctionID;
        var counterId = "#auction-counter-" + auctionID;

        changeEachVisibility('.auction-container', 'hidden');
        $('.counter-cell').each(function() {
            $(this).removeClass('active-counter')
        });

        var $auction = $(matchingID);
        var expiration = $auction.data('seconds-left');
        var counter = createDateObject(expiration);

        $auction.css('visibility', 'visible');
        $(counterId).addClass('active-counter').text(counter);
    });


    $('.bid-btn').on('click', function(){
        var $this = $(this);
        var $bidForm = $($this.context.previousElementSibling);
        var bidAmount = $bidForm.val();
        var auctionID = $bidForm.context.className.split(' ')[2].split('-')[2];
        var $highestBid = $('.highest-bid-' + auctionID);
        var highestBid = parseInt($highestBid.text().slice(1));

        if (bidAmount && !isNaN(bidAmount) && bidAmount > highestBid) {
            AJAXcreateBid(bidAmount, auctionID);
        }
    })

    $('')



});

/**
 * Created by lb on 4/27/15.
 */
$(document).ready(function() {

    $('.auction-item').hover(function(){
        var auctionID = $(this).context.id.split('-')[2];
        var matchingID = "#auction-" + auctionID;

        $('.auction-container').each(function() {
            $(this).css('visibility', 'hidden');
        });
        $(matchingID).css('visibility', 'visible');
    });

    $('.bid')



});

/**
 * Created by lb on 4/27/15.
 */

function counterTimeLeft(secondsLeft){
    var convertToHours = 60 * 60;

    var rest = secondsLeft / convertToHours;
    var hours = 0;
    while (rest > 1){ rest--; hours++; }

    rest *= 60;
    var minutes = 0;
    while (rest > 1){ rest--; minutes++; }

    rest *= 60;
    var seconds = 0;
    while (rest > 0){ rest--; seconds++; }

    var minutesStr = minutes.toString().length == 1 ? "0" + minutes : minutes;
    var secondsStr = seconds.toString().length == 1 ? "0" + seconds : seconds;

    return hours + " : " + minutesStr + " : " + secondsStr;
}

function createDateObject(totalSecondsLeft) {
    secondsSinceLoaded = $("#seconds-since-loaded").text();
    counter = counterTimeLeft(totalSecondsLeft - secondsSinceLoaded);
    return counter;
}

function decrementCounter(counter) {
    var times = counter.split(' : ');
    var hours = parseInt(times[0]);
    var minutes = parseInt(times[1]);
    var seconds = parseInt(times[2]);

    seconds--;
    if (seconds < 0) {
        minutes--;
        seconds = 59;
    }
    if (minutes < 0) {
        hours--;
        minutes = 59;
    }
    if (hours < 0) {
        console.log("AUCTION OVER")
    }
    var minutesStr = minutes.toString().length == 1 ? "0" + minutes : minutes;
    var secondsStr = seconds.toString().length == 1 ? "0" + seconds : seconds;

    return hours + " : " + minutesStr + " : " + secondsStr;
}

function changeEachVisibility(elem, visibility) {
    $(elem).each(function() {
        $(this).css('visibility', 'hidden');
    });
}

$(document).ready(function() {

    var seconds = 0;
    setInterval( function(){
        $("#seconds-since-loaded").html(seconds);
        seconds++
    }, 1000);

    setInterval( function() {
        var $active = $('.active-counter');
        $active.html(decrementCounter($active.text()));
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

            var data = { 'amount': bidAmount, 'id': auctionID };

            $.ajax({
                type: 'POST',
                url: '/auction/new/bid/',
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
    })

});

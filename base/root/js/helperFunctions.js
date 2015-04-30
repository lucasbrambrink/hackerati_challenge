/**
 * Created by lb on 4/29/15.
 */
function changeEachVisibility(elem, visibility) {
    $(elem).each(function() {
        $(this).css('visibility', 'hidden')
            .css('display', 'none');
    });
}

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
        return false;
    }
    var minutesStr = minutes.toString().length == 1 ? "0" + minutes : minutes;
    var secondsStr = seconds.toString().length == 1 ? "0" + seconds : seconds;

    return hours + " : " + minutesStr + " : " + secondsStr;
}


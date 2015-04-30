/**
 * Created by lb on 4/29/15.
 */
function auctionData(canvas_id, dataAuctions, dataInventory) {

    var data = {
        labels: ['$0 - $99', '$100 - $199', '$200 - $299', '$300 - $399', '$400 - $499', '+$500'],
        datasets: [
            {
                label: "Auctions",
                fillColor: "rgba(161, 0, 16, 0.7)",
                strokeColor: "rgba(161, 0, 16, 0.9)",
                pointColor: "rgba(161, 0, 16, 1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: dataAuctions
            },
            {
                label: "Total Inventory",
                fillColor: "rgba(46, 9, 175, 0.7)",
                strokeColor: "rgba(46, 9, 175, 0.9)",
                pointColor: "rgba(46, 9, 175, 1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(151,187,205,1)",
                data: dataInventory
            }
        ]
    };

    var canvas = document.getElementById(canvas_id).getContext("2d");
    var barChart = new Chart(canvas).Bar(data, {
    });

}
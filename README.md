# Hackerati Coding Challenge

## Consecutive Numbers
Quick algorithm to pick out indexes within an array that indicate the start of a consecutive ascending-
or descending triplet. It can be found in consecutive_numbers.py. Additionally, since I very recently
started learning Java, a Java implementation can be found in Main.java as an exercise for myself.


## Hackerati Auction

This is the main project of the repository. It exists solely as an MVP, as various features have yet to
be implemented. However, I was able to touch on a few important backend developing concepts. The project consists
of two main apps, base and auction.

### Base
Contains all front end packages (managed via Bower), media files, and houses the HackeratiUser model.
As such, it is also responsible for the On-Boarding funnel.
It contains a utility module, which for this project is just a Format Helper to parse strings,
but could be expanded as demand for encapsulated, reusable utilities increases.

I decided to implement the on-boarding funnel via PageTransitions.js, a front-end package that delegates
animated transitions between pages. For ease of quick use, the user can choose to skip providing any information,
in which case a dummy instance is created with fake credentials. If the provided username exists in the database,
the on-boarding changes to a log-in funnel.


### Auction
This is undoubtedly the heart of the project. The motivation was to loosely integrate craigslist.org with ebay,
providing a means for auctioning off items in a more public fashion that craiglist's current push-email method.

#### Models
The models are more-or-less straightforward. The schema does not extend past a few foreign keys to
appropriate owners and relations. Everything revolves around the InventoryItem,
which requires a user, name, reserved price, and a url to its image. This model has basic CRUD
functionality. Each item image is implemented as an ImageField, which inherits from Django's FileField.
However, I was having trouble serving these media files in production (on Heroku using whitenoise), therefor eventually
opted to host all files on imgur. Ideally, one would use a proper AWS/S3 pipeline.

The user can create new Auctions, Bids and Purchases (the latter, when fully implemented, would essentially serve
as a PO). Auctions are instantiated with a certain duration time, but can be closed prematurely by the
auctioneer. (Not yet implemented is extending the closing time if new bids were coming in within
the last few moments of the auction -- from the auctioneers perspective, doing this would only allow
the value to increase, as users are given more chances to bid ever higher).

#### Import
The motivation of this project was to integrate an auction-system with craigslist. The end result was rather
cumbersome, since craigslist does not provide an API. Moreover, the production environment is severely
hampered by the fact that craigslist.org blocks all Heroku IP addresses. So to my dismay, the deployed
project is unable to scrape new postings from craigslist. However, because this process can take several seconds,
I decided to 'unhinge' it from the web-layer as a separate process. I used a Redis queue to delegate
these asynchronous worker tasks. That is the fun stuff :)

As an additional note, a very important component of the craigslist market is the seller's location.
I chose to ignore this aspect for the MVP, but later iterations would certainly make use of it.
One could use GoogleMaps with ZIP codes to roughly pinpoint the item's location and calculate the distance
from the user (who would have provided a ZIP code during on-boarding).

As such, the MVP houses a little web-scraper module that queries craigslist, scrapes each posting for its
image, title and price, and imports them as new InventoryItems for the given user. Since this was not possible
in production, I implemented a quick-fix that scours a csv-file instead. I also added this function
as an additional manage.py command, (e.g. python manage.py run_import 'user_id') for ease of use.
Part of this pipeline was uploading the images to imgur as well.


#### Javascript
Admittedly, the JS-management in this project received short shrift. If I were to perform a larger scale refactor,
I would encapsulate most of my javascript into the Backbone.js framework. But as it stands, the javascript is a bit
dispersed, and overly reliant on jquery for event-delegation; Backbone would solve this very nicely. However,
I underestimated the scope of the final MVP when I conceived of the project. This was a lesson learned yet again:
always build for any scale.

I also wish for more documentation in my javascript code, but in the interest of an MVP decided to focus on backend and implementation.
After all, I am applying for a Backend position! However, along with the grand refactor this project might warrant comes proper code documentation.

#### Views
I forewent using django's REST framework in the interest of quick implementation (another mistake), and without
Backbone's MVVM pattern, I had to get a little creative with handling requests on the server. Therefore,
the url itself defines an 'action' that determines server-side event delegation. It was never meant to take on the
scale that it did, but it was fun to build this little mini-architecture.


#### Testing
There are no tests. This is merely a result of building a quick MVP, not because I don't adhere to TDD.
When working in a team on a mighty project, I firmly believe writing unit & integration test as you code are vital to the
sustainability and continuous integration of the project.

#### CSS
I used to LESS (which I much prefer) and compiled to CSS. I am rather unskilled at proper front-end design,
as it is not my strong suit, so please bear with this very shabby looking MVP :)


# Deployment
Deployed live at http://hackerati-auction-challenge.herokuapp.com
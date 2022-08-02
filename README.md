# Commerce Auction Site (Django)

## Project Description
Commerce is an e-commerce auction site like E-Bay, built using the Django Framework. It allows Users to post auction listings, bid on auctions, comment on listings, and watchlist them.

## Content

### 1. Django Models
Contains 5 Models for User, Listing, Bid, Comment, and Watchlist

### 2. Create Listing
![Picture for Creating a New Listing](./Images/Create%20Listing.png?raw=true "Create Listing")
When the User is authenticated, there is a navigation link that allows the User to create a new listing on the Navbar. The User can then specify the Title, Description, Starting Bid, and optionally provide an Image and/or Category as shown above.

### 3. Active Listings Page
![Picture for Active Listings](./Images/Active%20Listings.png?raw=true "Active Listings")
The default route for the web application, containing all the listings that are still active made by all the Users. Each listing displays the Title, Current Price, Description, and Photo (if there is one).

Clicking on any of the listings will redirect the User to that specific listing's page, allowing Users to view all the details about the listing.

### 4. Listing Page
![Picture for Listing Page](./Images/Listing.png?raw=true "Listing")

If the User is authenticated:
* They can watchlist the listing if it is not already in the Watchlist, or remove it otherwise.
* User can bid on an item, assuming the bid is at least as large as starting bid and larger than any other bids. Otherwise, an alert will notify the User of the error.
* If the User is the owner of the listing, they can close the auction, making the listing inactive and the current highest bidder, the winner.
* If the User has won the listing, there will be a notice, informing the User for winning the auction.
* Users can comment on the listing.

### 5. Watchlist
![Picture for Valid Watchlist](./Images/Valid%20Watchlist.png?raw=true "Valid Watchlist")
If the User is authenticated, the page will display all the listings that the User has watchlisted. Clicking any of the listings will bring the User to the specific listing page as well.

![Picture for Empty Watchlist](./Images/Empty%20Watchlist.png?raw=true "Empty Watchlist")
However, if the Watchlist is empty, there will be a notice notifying the User of the status.

### 6. Categories
![Picture for Categories](./Images/Categories.png?raw=true "Categories")
Clicking the Categories Tab on the Navbar will redirect the User to a page containing links to all the different categories available as shown above. Clicking on any of the categories will then bring the User to a page filled with listings that fulfil the criteria.

### 7. Django Admin Interface
![Picture of Admin Interface](./Images/Admin.png?raw=true "Admin Interface")
A site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.

## Learning Outcomes

* Learnt SQL and Relational Databases Basics.
* Familiarised with SQLite3.
* Learnt to use Django Models to work with Databases instead of SQL queries.
* Learnt about Django Migrations.
* Learnt to use the Python Shell to query our database using Python Commands.
* Learnt to make use of Django Admin to create, edit, and delete objects in the database.
* Learnt about Many-to-Many and One-to-Many Relationships.
* Learnt to implement User Authentication via Django

## Video Link
https://youtu.be/FYlje11QzKY
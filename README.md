## Welcome to the RentalApp wiki!
super simple contract manager for leased devices and service subscriptions

This app is written in Python 3 and tested on Python 3.7. The app doesn't look nice but it does its job. I wrote it in only 1 week throughout evening hours.

**Purpose:**

Simple tool to manage leases and service subscriptions.



**Data model:**

The app uses 3 tables only (business-partners, products and contracts). All 3 tables allow the addition, deletion or editing of records.



**Reporting:**

 1.   invoice run present month
 2.   invoice forecast next month
 3.   ending contracts next month



**Principle:**

The whole app is based on the principle that there are 3 different types of invoice records:

 1.   initial payment (start of the lease, arbitrary amount usually higher than regular lease rate)
 2.   regular fee (normal regular monthly lease) usually 11 or 23 times - depending on the contract duration
 3.   final purchase - the lease taker has the right to buy the product after the lease is completed
 
 
 Note: the db must be initialized first so the db file is created
 

 **Dependencies:**
 flask, flask-sqlalchemy, python-dateutil

## invoice-generator

A very simple python script for generating latex pdf invoices. Stores customer addresses in MongoDB table for now, but surely this should be changed. For python script to run module pymongo and mongodb must be installed (and mongod running on standard port on localhost). 

To use, simply clone repo and run "python main.py" and do setup, add customers and generate your invoices.

# TODO:
* Use simpler db (sqlite?)
* Multiple projects same invoice
* More/better templates
* Graphical interface (?)
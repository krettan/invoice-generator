#! /usr/bin/python
# coding: utf-8

def GetCustomer(name, customers):
	# find one in db
	db_results = customers.find_one({"!name": name})

	# from unicode to utf-8
	encoded_results = {}
	for k,v in db_results.items():
		if isinstance(v, unicode):
			encoded_results[k.encode('utf-8')] = v.encode('utf-8')

	return encoded_results

def AddCustomer(customers):
	# get info
	name = raw_input('Company name: ')
	address1 = raw_input('Address line 1: ')
	address2 = raw_input('Address line 2: ')
	city = raw_input('City: ')
	zip_code = raw_input('Zip code: ')
	country = raw_input('Country: ')

	# create dict and save to db
	custInfo = {"!name": name,
  						"!address1": address1,
  						"!address2": address2,
  						"!city": city,
  						"!zip_code": zip_code,
  						"!country": country}
	return customers.insert(custInfo)
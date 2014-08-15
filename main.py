#! /usr/bin/python
# coding: utf-8
import os, sys, re, pymongo
import ConfigParser
from subprocess import call
from customer import GetCustomer, AddCustomer
from invoice import CreateInvoice
from pymongo import MongoClient

def setup():
  # get info
  name = raw_input('Company name: ')
  address1 = raw_input('Address line 1:' )
  address2 = raw_input('Address line 2: ')
  city = raw_input('City: ')
  zip_code = raw_input('Zip code: ')
  country = raw_input('Country: ')
  
  # open config.ini
  config = ConfigParser.ConfigParser()
  config.read('config.ini')

  # if info section does not exist create all the rest
  if not config.has_section('info'):
    config.add_section('info')
    config.add_section('paths')
    config.add_section('templates')

  # if no invoice number has been set, start from 1
  if not config.has_option('info','invoice_number'):
    config.set('info','invoice_number',1)

  # information about invoice owner
  config.set('info','self_name',name)
  config.set('info','self_address1',address1)
  config.set('info','self_address2',address2)
  config.set('info','self_city',city)
  config.set('info','self_zip_code',zip_code)
  config.set('info','self_country',country)

  # paths
  config.set('paths','template_path','templates')
  config.set('paths','invoice_path','invoices')

  # available templates
  config.set('templates','standard','standard')
  config.set('templates','invoice','invoice')
  
  with open('config.ini','wb') as f:
    config.write(f)

  
if __name__ == '__main__':
  # create db-client and get customers table
  client = MongoClient('localhost', 27017)
  db = client.invoice_generator
  customers = db.customers

  # load config.ini
  config = ConfigParser.ConfigParser()
  config.read('config.ini')

  while True:
    argument = raw_input('Enter command, Setup (setup), add customer (add_customer), list customer (list_customer), create invoice (create_invoice) or exit (exit): ')
    if argument == 'setup':
      setup()
    if argument == 'add_customer':
      print AddCustomer(customers)
    if argument == 'list_customer':
      customerName = raw_input('Name of customer: ')
      customer = GetCustomer(customerName, customers)
      print customer
    if argument == 'create_invoice':
      # get info 
      customerName = raw_input('Name of recipient: ')
      customer = GetCustomer(customerName, customers)
      template = raw_input('Which template to use (standard, invoice): ')
      info = config._sections['info']

      # project info
      project_title = raw_input('Project title: ')
      activity = raw_input('Activity: ')
      vat = raw_input('VAT %: ')
      price = raw_input('Price per unit: ')
      qtty = raw_input('Quantity: ')
      invoice_name = raw_input('Invoice file name: ')  

      content = {'!invoice_number': config.get('info','invoice_number'),
                  '!project_name': project_title,
                  '!activity': activity,
                  '!vat': vat,
                  '!price': price,
                  '!qtty': qtty}

      # create invoice
      CreateInvoice(config.get('paths','template_path'),
                    config.get('templates',template),
                    config.get('paths','invoice_path'),
                    invoice_name,
                    info,
                    customer,
                    content)

      # update invoice number
      config.set('info','invoice_number', config.get('info', invoice_number) + 1)
      with open('config.ini','wb') as f:
        config.write(f)

    if argument == 'exit':
      break
#! /usr/bin/python
# coding: utf-8

import re
from subprocess import call

def CreateInvoice(template_path, template_name, 
                   invoice_path, invoice_name, info, customer, content):
  # combine dicts and replace tokens in template
  combined_dict = dict(info.items() + customer.items() + content.items())
  print combined_dict
  with open(invoice_path + '/'  + invoice_name + '.tex', 'w') as invoice_tex:
    with open(template_path + '/' + template_name + '.tex', 'r') as template_tex:
      for line in template_tex:
        invoice_tex.write(multiple_replace(combined_dict, line))
  
  # call pdflatex 
  call(['pdflatex', '-output-directory',
        invoice_path , invoice_path + '/' + invoice_name + '.tex'])

def multiple_replace(dict, text): 
  """ multiple_replace borrowed from: http://code.activestate.com/recipes/81330-single-pass-multiple-replace/"""

  """ Replace in 'text' all occurences of any key in the given
  dictionary by its corresponding value.  Returns the new tring.""" 

  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 
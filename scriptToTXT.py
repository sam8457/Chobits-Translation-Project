#!/usr/bin/env python3

# Use this to copy/paste into a text editor for spellcheck.

import json

tran_file = open('tran_script.json','r')
tran_data = json.loads(tran_file.read())
tran_file.close()

full_script = ""

for nth_box, box_data in tran_data.items():

    eng_text = box_data["tran"]
    full_script += eng_text + "\n"

with open('tran_script.txt','w') as file:
    file.write(full_script)



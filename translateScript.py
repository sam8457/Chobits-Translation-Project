#!/usr/bin/env python3

import deep_translator
import json
from API_key import API_key # must have a file containing your own API key

# These translators are free, but produce mid-tier results. Use for testing.
#translator = deep_translator.GoogleTranslator(source='ja', target='en') # decent
#translator = deep_translator.LingueeTranslator(source='japanese', target='english') # bad
#translator = deep_translator.MyMemoryTranslator(source='ja-JP', target='en-US') # decent

# Prefer this translator. It requires a paid API key from https://platform.openai.com
translator = deep_translator.ChatGptTranslator(api_key=API_key, source='japanese', target='english')

tran_file = open('tran_script.json','r')
tran_data = json.loads(tran_file.read())
tran_file.close()

''' Example from tran_script.json:
  "0": {
    "end_offset": 1061803,
    "orig": "東京か…やっぱ都会だよなぁ。\nオレの田舎なんか、緑と牛しか\nなくてまったりしてたんだけど、",
    "orig_len": 88,
    "custom?": false,
    "tran": "Tokyo... Really is the big\ncity, eh? Back home, there's\njust grass and cows, so lax.",
    "tran_len": null,
    "shorten?": null
  },
'''

req_limit = 10 # can adjust
req_count = 0

for nth_box, box_data in tran_data.items():

    if req_count >= req_limit: 
        break

    orig = box_data["orig"].replace("\n","")
    newline_count = orig.count("\n")
    orig = orig.replace("\n","")

    tran = box_data["tran"]

    if not (tran == None or len(tran) == 0):

        #print("Skipping box", nth_box)
        #print()

        continue

    print("For box", nth_box, "translating:", orig)

    try:
        auto_translation = translator.translate(orig)
        req_count += 1

        # clean autotranslation (Chat GPT likes to include extras)
        auto_translation = auto_translation.replace("\"","")
        auto_translation = auto_translation.replace("Translation: ","")

        box_data["tran"] = auto_translation
        box_data["tran_len"] = len(auto_translation)

        if box_data["orig_len"] < len(auto_translation) + newline_count:
            box_data["shorten?"] = True
        else:
            box_data["shorten?"] = False

    except:
        print("Translation error.") # can finish printing to file if this happens
        #raise
        break

    print("Translated to:", auto_translation)
    print()


with open('tran_script.json','w') as file:
    json.dump(tran_data, file, ensure_ascii=False, indent=2)
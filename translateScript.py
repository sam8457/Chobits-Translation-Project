#!/usr/bin/env python3

import deep_translator # type: ignore
import json
from API_key import API_key # must have a file containing your own API key
from openai import OpenAI # type: ignore
from pprint import pprint



def translateFree():
    # These translators are free, but produce worse results. Use for testing.

    translator = deep_translator.GoogleTranslator(source='ja', target='en') # decent
    #translator = deep_translator.LingueeTranslator(source='japanese', target='english') # bad
    #translator = deep_translator.MyMemoryTranslator(source='ja-JP', target='en-US') # decent

    tran_file = open('tran_script.json','r')
    tran_data = json.loads(tran_file.read())
    tran_file.close()

    req_limit = 10 # can adjust
    req_count = 0

    for nth_box, box_data in tran_data.items():

        if req_count >= req_limit: 
            break

        orig = box_data["orig"].replace("\n","")
        newline_count = orig.count("\n")
        orig = orig.replace("\n","")

        tran = box_data["tran"]

        if not tran == None:

            continue

        print("For box", nth_box, "translating:", orig)

        try:
            auto_translation = translator.translate(orig)
            req_count += 1

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



def translatePaid():
    # Prefer this translator. It requires a paid API key from https://platform.openai.com

    tran_file = open('tran_script.json','r')
    tran_data = json.loads(tran_file.read())
    tran_file.close()

    # Consider changing model to optimize for price/performance.
    #model = "gpt-3.5-turbo" # cheap, fast, ok results
    #model = "gpt-4.1-nano"
    #model = "gpt-4.1-mini"
    #model = "gpt-4.1"
    #model = "gpt-5-nano"
    #model = "gpt-5-mini"
    model = "gpt-5" # expensive, slow, good results

    client = OpenAI(api_key=API_key)
    prompt = "Give brief English translations of the following Japanese text including no additional remarks or quotes."
    total_tokens = 0

    req_limit = 10 # can adjust
    req_count = 0

    for nth_box, box_data in tran_data.items():

        if req_count >= req_limit: 
            break

        orig = box_data["orig"].replace("\n","")
        newline_count = orig.count("\n")
        orig = orig.replace("\n","")

        tran = box_data["tran"]

        if not tran == None:

            continue

        print("For box", nth_box, "translating:", orig)

        try:
            input = [
                {
                    "role": "developer",
                    "content":prompt
                },
                {
                    "role":"user",
                    "content":orig
                }
            ]

            response = client.responses.create(
                model=model,
                reasoning={"effort": "minimal"}, # comment out for models older than gpt-5
                input=input
            )   

            auto_translation = response.output_text
            total_tokens += response.usage.total_tokens
            req_count += 1

            box_data["tran"] = auto_translation
            box_data["tran_len"] = len(auto_translation)

            if box_data["orig_len"] < len(auto_translation) + newline_count:
                box_data["shorten?"] = True
            else:
                box_data["shorten?"] = False

            print("Translated to:", auto_translation)

        except:
            print("Translation error.") # can finish printing to file if this happens
            #raise
            break


    print("Total tokens used:", total_tokens)

    with open('tran_script.json','w') as file:
        json.dump(tran_data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":

    translatePaid()
    # Bookmark: 795
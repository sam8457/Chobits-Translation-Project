#!/usr/bin/env python3

import json
from tim2CompTools import *

import deepl

auth_key = "{YOUR_API_KEY}" # replace with your key
deepl_client = deepl.DeeplClient(auth_key)

result = deepl_client.translate_text("Hello, world!", target_lang="DE")
print(result.text)

# Todo: Use deepl api to translate items in script.json file
# https://developers.deepl.com/docs/getting-started/intro#python
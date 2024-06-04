""" Demo implementation for GPTALL"""

__author__ = "sgu"

#  Copyright (c) 2024.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from gpt4all import GPT4All
model = GPT4All(model_name='orca-mini-3b-gguf2-q4_0.gguf')  # /home/sgu/.cache/gpt4all/
with model.chat_session():
    response1 = model.generate(prompt='hello', temp=0)
    response2 = model.generate(prompt='write me a short poem', temp=0)
    response3 = model.generate(prompt='thank you', temp=0)
    print(model.current_chat_session)

# tokens = []
# with model.chat_session():
#     for token in model.generate("What is the capital of France?", streaming=True):
#         tokens.append(token)
# print(tokens)

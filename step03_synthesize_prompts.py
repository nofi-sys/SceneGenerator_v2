import os
import re
import openai
from time import time,sleep
from random import seed,shuffle,sample


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)


def save_json(filepath, payload):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=2)


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.0, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()  # force it to fix any unicode errors
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            #text = re.sub('\s+', ' ', text)
            #text = re.sub('^-\s*', ' ', text)
            text = re.sub('[\r\n]+', '\n', text)
            filename = '%s_gpt3.txt' % time()
            if not os.path.exists('gpt3_logs'):
                os.makedirs('gpt3_logs')
            save_file('gpt3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            #print('\n\nINPUT', prompt)
            #print('\n\nOUTPUT:', text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


openai.api_key = open_file('openaiapikey.txt')
description_prompts = ['prompt_description_characters.txt', 'prompt_description_style.txt', 'prompt_description_purpose.txt']
summary_prompts = ['prompt_list_detailed.txt', 'prompt_list_outline.txt', 'prompt_summary_concise.txt', 'prompt_summary_synopsis.txt']


def run_prompts(prompt_files, text_input):
    result = ''
    for pfile in prompt_files:
        prompt = open_file(pfile).replace('<<INPUT>>', text_input)
        completion = gpt3_completion(prompt)
        result = '%s\n\n%s' % (result, completion)
    return result.strip()


if __name__ == '__main__':
    files = os.listdir('chapter_bits/')
    seed()
    data = list()
    for file in files:
        completion = open_file('chapter_bits/%s' % file)
        #### SELECT PROMPTS
        prompts = list()
        prompts += sample(description_prompts, 2)
        prompts += sample(summary_prompts, 1)
        shuffle(prompts)
        print(prompts)
        #### GET INPUTS
        text = run_prompts(prompts, completion)
        save_file('prompts/%s' % file, text)
        print('\n\n\n', text)
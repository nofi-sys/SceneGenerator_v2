import os
import json


prompt_dir = 'prompts/'
completion_dir = 'chapter_bits/'


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


if __name__ == '__main__':
    files = os.listdir(prompt_dir)
    data = list()
    for file in files:
        prompt = open_file(prompt_dir + file).strip()
        completion = open_file(completion_dir + file).strip()
        prompt = prompt + '\n\nSCENE: '  # add demarc
        completion = ' ' + completion + ' THE END'  # add stop token
        info = {'prompt': prompt, 'completion': completion}
        data.append(info)
    with open('scenes.jsonl', 'w') as outfile:
        for i in data:
            json.dump(i, outfile)
            #json.dump(i, outfile, ensure_ascii=False)
            outfile.write('\n')
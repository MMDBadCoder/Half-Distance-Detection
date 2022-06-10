import codecs
import re

from main import get_cleaned_text

input_file_path = "./input.txt"
lines = [re.split(' ', x.strip()) for x in codecs.open(input_file_path, 'rU', 'utf-8').readlines()]
result = get_cleaned_text(lines)

for line in result:
    for sent in line:
        print(sent['sentence'], end=' ')
    print()

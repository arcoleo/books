#!/usr/bin/env python3

from ast import literal_eval
import os
from pprint import pprint

current_path = os.path.dirname(os.path.abspath(__file__))
# print(current_path)

file_list = []
for (dirpath, dirnames, filenames) in os.walk(os.path.join(current_path, '..', 'books')):
    file_list.extend(filenames)
    break
file_list = sorted(file_list)
# pprint(file_list)

# print(f)

toc_dict = {}
books_list = []

# parse_tags(tag_dict):

def generate_output(books):
    output = ['= Welcome to the Books Wiki']
    output.append('  David Arcoleo <david@arcoleo.org>')

    outline = {}

    for book in books:
        # Get subjects
        # print('--%s' % book)
        curr_subjects = book.get('subjects')
        for subject in curr_subjects:
            if subject in outline.keys():
                outline[subject]['books'].append({
                    'title': book.get('title'), 
                    'filename': book.get('filename'),
                    'authors': '; '.join(book.get('authors'))
                })
            else:
                outline[subject] = {
                    'level': 2, 
                    'books': [{
                        'title': book.get('title'), 
                        'filename': book.get('filename'),
                        'authors': '; '.join(book.get('authors'))
                    }]}

    for topic, value in sorted(outline.items()):
        # print(topic)
        
        output.append('')
        level = '=' * value['level']
        output.append('%s %s' % (level, topic))
        # print('--! %s' % value)
        for book in value['books']:
            # print('----! %s' % str(book))
            output.append('')
            output.append('link:books/%(filename)s[%(title)s], %(authors)s' % book)
        


    # pprint(outline)

    # print('------')
    for line in output:
        print(line)

for curr_file in file_list:
    open_file = os.path.join(current_path, '..', 'books', curr_file)
    with open(open_file) as f:
        lines = f.readlines()
        current_title = None
        dsa_dict = None
        author_line = None
        for idx, line in enumerate(lines):
            if line.startswith('==='):
                current_title = line[len('==='):].strip()
                author_line = idx + 1
            if idx == author_line:
                current_authors = line.split(';')
                current_authors = list(map(str.strip, current_authors))
                # print('-- %s --' % str(current_authors))
            if line.startswith(':dsa:'):
                # print('Hello -- %s' % line)
                current_line = line[len(':dsa:'):].strip()
                dsa_dict = literal_eval(current_line)
                dsa_dict['title'] = current_title
                dsa_dict['filename'] = curr_file
                dsa_dict['authors'] = current_authors
                books_list.append(dsa_dict)
                # print(dsa_dict)

# print('--- Books List ---')
# pprint(books_list)

# print('--- Generated ---')
generate_output(books_list)
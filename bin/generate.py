#!/usr/bin/env python3

import argparse
from ast import literal_eval
import logging
import os
from pprint import pprint



books_list = []
# parse_tags(tag_dict):

def generate_output(args, books, grouping='subjects'):
    output = ['= Welcome to the Books Wiki']
    output.append('David Arcoleo <david@arcoleo.org>')

    outline = {}

    if args.table:
        divider = ' | '
        prefix = '| '
    else:
        divider = ', '
        prefix = ''

    for book in books:
        # Get subjects / ratings
        
        curr_topic_index = grouping
        curr_topics = book.get(curr_topic_index)
        # only one rating, so make it a list of one item so iterator doesn't break
        if isinstance(curr_topics, int):
            curr_topics = [curr_topics]
        logging.warning(curr_topics)
        logging.warning(outline)
        for curr_item in curr_topics:
            if curr_item in outline.keys():
                outline[curr_item]['books'].append({
                    'title': book.get('title'), 
                    'filename': book.get('filename'),
                    'authors': '; '.join(book.get('authors', []))
                })
            else:
                try:
                    outline[curr_item] = {
                        'level': 2, 
                        'books': [{
                            'title': book.get('title'), 
                            'filename': book.get('filename'),
                            'authors': '; '.join(book.get('authors', []))
                        }]}
                except Exception as e:
                    logging.error(e)
                    logging.error(book)
                    logging.error(curr_topics)
                    raise
        

    for topic, value in sorted(outline.items()):
        # print(topic)
        logging.warning(topic)
        
        output.append('')
        level = '=' * value['level']
        output.append('%s %s' % (level, topic))
        if args.table:
            output.append('|====================')
        # print('--! %s' % value)
        for book in value['books']:
            # logging.debug(book)
            # print('----! %s' % str(book))
            if not args.table:
                output.append('')
            title = 'link:books/%(filename)s[%(title)s]' % book
            authors = '%(authors)s' % book
            line = '%s%s%s%s' % (prefix, title, divider, authors)
            output.append(line)

    if args.table:
        output.append('|====================')    

    for line in output:
        print(line)

    outfile = '%s.asciidoc' % grouping.upper()
    with open(outfile, 'w') as fp:
        fp.write("\n".join(output))


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--table', action='store_true')
    args = parser.parse_args()

    return args

def main():
    args = read_args()
    file_list = []

    current_path = os.path.dirname(os.path.abspath(__file__))
    # print(current_path)

    
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(current_path, '..', 'books')):
        file_list.extend(filenames)
        break
    file_list = sorted(file_list)
    # pprint(file_list)

    # print(f)

    toc_dict = {}
    


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
                    dsa_dict['rating'] = dsa_dict.get('rating', 0)
                    books_list.append(dsa_dict)
                    # print(dsa_dict)

    # print('--- Books List ---')
    pprint(books_list)

    # print('--- Generated ---')
    generate_output(args, books_list, grouping='subjects')
    generate_output(args, books_list, grouping='rating')

if __name__ == '__main__':
    main()
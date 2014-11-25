#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from util import *
from termcolor import colored
import readline
import json
import os
import platform

def parse_params(src_params) :
    src_params = src_params.split(' ')

    ret = {'cmd' : src_params[0]}

    if len(src_params) <= 1 :
        return ret

    for j in range(len(src_params))[:-1:2] :
        ret[ src_params[j+1] ] = src_params[j+2]

    return ret


def quit(params) :
    exit()

def cls(params) :
    if 'Windows' ==  platform.system() :
        os.system('cls')
    else :
        os.system('clear')

def print_content(content_id) :
    content = V2exHttpClient.get_content(content_id)
    print (
            '    %s \n'
            '                                                                                                                 \n'
            '    %s \n'
            '                                                                                                                 \n'
            '-----------------------------------------------------------------------------------------------------------------\n'
            ) % (content['title'], content['content'])
    j = 0
    for v in content['reply_contents'] :
        j += 1
        print (
                '---------------------------- floor %d ----------------------------\n'
                '%s\n\n\n'
                ) % (j, v)

def print_contents(path, params) :
    r = V2exAPI.get(path)

    limit = int(params.get('limit', params.get('l', 0)))
    offset = int(params.get('offset', params.get('o', 0)))

    def print_v(v) :
        print v['id']
        print v['title']
        print ''

    offset_j = 0
    count = 0
    for v in r :
        if offset and offset_j < offset :
            offset_j += 1
            continue

        count += 1
        offset_j += 1

        print_v(v)

        if limit and count >= limit :
            break

def print_node_contents(params) :
    path = params.get('path', params.get('p', None))
    contents = V2exHttpClient.get_contents(path)

    for v in contents :
        print v['id']
        print v['title']
        print ''

def list_nodes(params) :
    nodes = V2exHttpClient.get_all_nodes()
    output = ''
    j = 0
    for v in nodes :
        j += 1
        if j >= 5 :
            output = '%s\n' % output
            j = 0

        output = '%s [%s %s]' % (output, v['path'], v['name'])
    print output


def msg(params) :
    content_id = int(params.get('content_id', params.get('d', 0)))
    print_content(content_id)

def hot(params) :
    print_contents('topics/hot.json', params)
    

def latest(params) :
    print_contents('topics/latest.json', params)


_g = {
        'CMD_TOKEN' : {
            'quit'  : quit,
            'q'     : quit,

            'nodes' : list_nodes,
            'ns'    : list_nodes,

            'node'  : print_node_contents,
            'n'     : print_node_contents,

            'hot'   : hot,
            'h'     : hot,

            'latest': latest,
            'l'     : latest,

            'msg'   : msg,
            'm'     : msg,

            'cls'   : cls 
            }
        }

def main() :
    global _g 
    while True :
        r = parse_params(raw_input('>>> '))
        cmd = _g['CMD_TOKEN'].get(r['cmd'], None)
        if cmd :
            cmd(r)

if __name__ == '__main__' :
    main()

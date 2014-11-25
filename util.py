# v2ex api
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq
from lxml import etree
import urllib
import re


class V2exAPI(object) :
    BASEHOST = 'http://www.v2ex.com/api/'

    @classmethod
    def make_url(cls, path) :
        return '%s%s' % (cls.BASEHOST, path)

    @classmethod
    def _request(cls, method, path, params=None, files=None) :
        try :
            return requests.request(method, url=cls.make_url(path), params=params, files=files, verify=False)
        except :
            return None

    @classmethod
    def get(cls, path, params=None) :
        try :
            return requests.get(cls.make_url(path), params=params, verify=False).json()
        except :
            return None


class V2exHttpClient(object) :
    BASEHOST = 'http://www.v2ex.com/'

    @classmethod
    def make_url(cls, path) :
        return '%s%s' % (cls.BASEHOST, path)

    @classmethod
    def _request(cls, path) :
        return pq(url=cls.make_url(path))

    @classmethod
    def get_content(cls, content_id) :
        content = {}
        d = cls._request('t/%d' % content_id)
        content['title']    = d('#Main')('div.header')('h1').html()
        content['content']  = d('#Main')('div.topic_content').html()
        if content['content'] :
            content['content'] = content['content'].replace('<br />', '\n')

        content['reply_contents'] = []
        node = d('#Main')('div.reply_content')
        if node :
            for v in node.items() :
                content['reply_contents'].append(v.html().replace('<br />', '\n'))

        return content 

    @classmethod 
    def get_contents(cls, path) :
        contents = []
        d = cls._request(path)
        dom = d('#Main')('span.item_title')

        if not dom :
            return contents

        pattern = re.compile('[0-9]+')
        for v in dom.items() :
            content_dom = v('a')
            contents.append( {
                'id'    : pattern.findall(content_dom.attr('href'))[0],
                'title' : content_dom.html()
                })

        return contents


    @classmethod
    def get_all_nodes(cls) :
        nodes = []
        d = cls._request('planes')
        dom = d('#Main')('a.item_node')

        if not dom :
            return nodes

        for v in dom.items() :
            nodes.append( {'path':v.attr('href'), 'name':v.html()} )

        return nodes

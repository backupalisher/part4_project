from part4_project.apps.main.functions import preload
from .filter_func import *
from .search_func import *


class GetModels(object):

    def __init__(self):
        pass

    def all(self, limit, offset, url):
        return preload(limit, offset, url)

    def filtered(self, post, step):
        print(dict(post.lists()))
        checkboxs = {}
        ranges = {}
        radios = {}
        fbrands = []
        if dict(post.lists())['checkboxs'][0]:
            checkboxs = dict(post.lists())['checkboxs'][0]
        if dict(post.lists())['ranges'][0]:
            ranges = dict(post.lists())['ranges'][0]
        if dict(post.lists())['radios'][0]:
            radios = dict(post.lists())['radios'][0]
        if dict(post.lists())['brands'][0] and 'null' not in dict(post.lists())['brands'][0]:
            fbrands = dict(post.lists())['brands'][0].replace('[', '').replace(']', '').split(',')
        if len(checkboxs) != 0 or len(ranges) != 0 or len(radios) != 0:
            return get_filtered_model(fbrands, checkboxs, ranges, radios)
        else:
            return None

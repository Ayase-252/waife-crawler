"""
Unit test of waife_crawler
"""
from unittest import TestCase
import os
from datetime import date

from requests_mock import Mocker

from command.waife_crawler import run


def read_file(file_path):
    """
    Read a file and return all this content
    """
    file_ = open(file_path, encoding='utf-8')
    text = file_.read()
    file_.close()
    return text


def setup_testcase(mocker):
    """
    Set up Acceptance Test I requiring program to crawl two pages.
    """
    base_url = 'http://konachan.net'
    mocker.get(base_url + '/post?page=1',
               text=read_file('test/command/query_page_1.html'))
    mocker.get(base_url + '/post?page=2',
               text=read_file('test/command/query_page_2.html'))

    mocker.get('http://konachan.net/post/show/230239/akatsuki_-kancolle-group-hibiki_-kancolle-ikazuchi',
               text=read_file('test/command/230239.html'))
    mocker.get('http://konachan.net/post/show/230230/blonde_hair-bodysuit-boots-ddal-gun-hat-long_hair-',
               text=read_file('test/command/230230.html'))
    mocker.get('http://konachan.net/post/show/230237/kuroi_-liar-player-may_day_suisai_no_yume_yori_-vo',
               text=read_file('test/command/230237.html'))

    mocker.get('http://konachan.net/image/88482d765f640f78d94243117f3ef50d/Konachan.com%20-%20230237%20kuroi_%28liar-player%29%20may_day_suisai_no_yume_yori_%28vocaloid%29%20original%20waifu2x.png',
               text='230237')
    mocker.get('http://konachan.net/image/dbb993f5585763ceafeb075dd40cdced/Konachan.com%20-%20230230%20blonde_hair%20bodysuit%20boots%20ddal%20gun%20hat%20long_hair%20military%20original%20ponytail%20techgirl%20weapon%20yellow_eyes.jpg',
               text='230230')
    mocker.get('http://konachan.net/image/b922c0627fa2fd5f725a529b3d8fff0c/Konachan.com%20-%20230239%20akatsuki_%28kancolle%29%20group%20hibiki_%28kancolle%29%20ikazuchi_%28kancolle%29%20inazuma_%28kancolle%29%20kantai_collection%20kawai_%28purplrpouni%29%20loli.png',
               text='230239')


def clear_test_temporary_file():
    """
    Clear test temporary file
    """
    to_delete = ['230237.png', '230230.jpg', '230239.png']
    datestr = date.today().strftime('%Y-%m-%d')
    for file_ in to_delete:
        if os.path.isfile(datestr + '/' + file_):
            os.remove(datestr + '/' + file_)
    os.removedirs(datestr)

def make_full_path(file_name):
    datestr = date.today().strftime('%Y-%m-%d')
    return datestr + '/' + file_name

class WaifeCrawlerTest(TestCase):
    """
    """
    @Mocker()
    def test_acceptance_test_I(self, mocker):
        setup_testcase(mocker)

        run(page_limit=2, score_threshold=38)

        picture_230230 = read_file(make_full_path('230230.jpg'))
        picture_230237 = read_file(make_full_path('230237.png'))
        picture_230239 = read_file(make_full_path('230239.png'))

        clear_test_temporary_file()
        self.assertEqual(picture_230230, '230230')
        self.assertEqual(picture_230237, '230237')
        self.assertEqual(picture_230239, '230239')
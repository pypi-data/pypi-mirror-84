from __future__ import unicode_literals
import pytest
from textx import metamodel_from_str, TextXSyntaxError


def test_issue188_skipws_1():
    mm = metamodel_from_str(r'''
        File: 'foo' /\s/ 'bar';
    ''', skipws=False)
    mm.model_from_str('foo bar')


def test_issue188_skipws_2():
    mm = metamodel_from_str('''
        File: 'foo' ' ' 'bar';
    ''', skipws=False)
    mm.model_from_str('foo bar')


def test_issue188_skipws_3():
    mm = metamodel_from_str(r'''
        File[noskipws]: 'foo' SPACE 'bar';
        SPACE[noskipws]: /\s/;
    ''')
    mm.model_from_str('foo bar')


def test_issue188_skipws_4():
    mm = metamodel_from_str('''
        File[noskipws]: 'foo' SPACE 'bar';
        SPACE[noskipws]: ' ';
    ''')
    mm.model_from_str('foo bar')


def test_issue188_skipws_5():
    mm = metamodel_from_str('''
        File[noskipws]: ' foo' SPACE 'bar ';
        SPACE[noskipws]: ' ';
    ''')
    with pytest.raises(TextXSyntaxError,
                       match='.*Expected \'bar \' at position'):
        mm.model_from_str(' foo bar')
    mm.model_from_str(' foo bar ')

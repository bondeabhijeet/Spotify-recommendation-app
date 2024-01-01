

"""Tests for abp.filters.blocks."""

from __future__ import unicode_literals

import json
import os

import pytest

from abp.filters import parse_filterlist, SelectorType, FilterAction
from abp.filters.blocks import to_blocks

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture()
def fl_lines():
    with open(os.path.join(DATA_PATH, 'filterlist.txt')) as f:
        return list(parse_filterlist(f))


@pytest.fixture()
def expected_blocks():
    with open(os.path.join(DATA_PATH, 'expected_blocks.json')) as f:
        return json.load(f)


def test_to_blocks(fl_lines):
    blocks = list(to_blocks(fl_lines))
    assert len(blocks) == 3
    block = blocks[0]
    assert block.variables['foo'] == 'bar'
    assert block.variables['baz'] == ('some_tricky?variable=with&funny=chars#'
                                      'and-stuff')
    assert block.description == 'Example block 1\nAnother comment'
    # Don't test the filters thouroughly: filter parsing is tested elsewhere.
    assert len(block.filters) == 2
    assert block.filters[0].selector['type'] == SelectorType.URL_PATTERN
    assert block.filters[1].action == FilterAction.SHOW


def test_to_dict(fl_lines, expected_blocks):
    blocks = [b.to_dict() for b in to_blocks(fl_lines)]
    assert blocks == expected_blocks

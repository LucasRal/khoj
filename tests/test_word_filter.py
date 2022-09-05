# External Packages
import torch

# Application Packages
from src.search_filter.word_filter import WordFilter
from src.utils.config import SearchType


def test_no_word_filter(tmp_path):
    # Arrange
    word_filter = WordFilter(tmp_path, SearchType.Org)
    embeddings, entries = arrange_content()
    q_with_no_filter = 'head tail'

    # Act
    can_filter = word_filter.can_filter(q_with_no_filter)
    ret_query, entry_indices = word_filter.apply(q_with_no_filter, entries)

    # Assert
    assert can_filter == False
    assert ret_query == 'head tail'
    assert entry_indices == {0, 1, 2, 3}


def test_word_exclude_filter(tmp_path):
    # Arrange
    word_filter = WordFilter(tmp_path, SearchType.Org)
    embeddings, entries = arrange_content()
    q_with_exclude_filter = 'head -"exclude_word" tail'

    # Act
    can_filter = word_filter.can_filter(q_with_exclude_filter)
    ret_query, entry_indices = word_filter.apply(q_with_exclude_filter, entries)

    # Assert
    assert can_filter == True
    assert ret_query == 'head tail'
    assert entry_indices == {0, 2}


def test_word_include_filter(tmp_path):
    # Arrange
    word_filter = WordFilter(tmp_path, SearchType.Org)
    embeddings, entries = arrange_content()
    query_with_include_filter = 'head +"include_word" tail'

    # Act
    can_filter = word_filter.can_filter(query_with_include_filter)
    ret_query, entry_indices = word_filter.apply(query_with_include_filter, entries)

    # Assert
    assert can_filter == True
    assert ret_query == 'head tail'
    assert entry_indices == {2, 3}


def test_word_include_and_exclude_filter(tmp_path):
    # Arrange
    word_filter = WordFilter(tmp_path, SearchType.Org)
    embeddings, entries = arrange_content()
    query_with_include_and_exclude_filter = 'head +"include_word" -"exclude_word" tail'

    # Act
    can_filter = word_filter.can_filter(query_with_include_and_exclude_filter)
    ret_query, entry_indices = word_filter.apply(query_with_include_and_exclude_filter, entries)

    # Assert
    assert can_filter == True
    assert ret_query == 'head tail'
    assert entry_indices == {2}


def arrange_content():
    embeddings = torch.randn(4, 10)
    entries = [
        {'compiled': '', 'raw': 'Minimal Entry'},
        {'compiled': '', 'raw': 'Entry with exclude_word'},
        {'compiled': '', 'raw': 'Entry with include_word'},
        {'compiled': '', 'raw': 'Entry with include_word and exclude_word'}]

    return embeddings, entries

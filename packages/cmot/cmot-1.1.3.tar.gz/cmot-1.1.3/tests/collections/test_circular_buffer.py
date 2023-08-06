import pytest

from cmot.collections.circular_buffer import CircularBuffer


def test_circular_buffer_init_unsized_error():
    with pytest.raises(TypeError):
        CircularBuffer()


def test_circular_buffer_init_empty():
    b = CircularBuffer(5)
    assert list(b) == []


def test_circular_buffer_init_partial():
    b = CircularBuffer(5, range(3))
    assert list(b) == [0, 1, 2]


def test_circular_buffer_init_full():
    b = CircularBuffer(5, range(5))
    assert list(b) == [0, 1, 2, 3, 4]


def test_circular_buffer_init_overfull():
    b = CircularBuffer(5, range(7))
    assert list(b) == [2, 3, 4, 5, 6]


def test_circular_buffer_str():
    b = CircularBuffer(3, range(4))
    assert str(b) == "[1, 2, 3]"


def test_circular_buffer_repr():
    b = CircularBuffer(3, range(4))
    assert repr(b) == "CircularBuffer(3, [1, 2, 3])"


def test_circular_buffer_len_empty():
    assert len(CircularBuffer(5)) == 0


def test_circular_buffer_len_partial():
    assert len(CircularBuffer(5, range(3))) == 3


def test_circular_buffer_len_full():
    assert len(CircularBuffer(5, range(5))) == 5


def test_circular_buffer_len_overfull():
    assert len(CircularBuffer(5, range(7))) == 5


def test_circular_buffer_len_overfull_pop():
    b = CircularBuffer(5, range(7))
    b.pop()
    assert len(b) == 4


def test_circular_buffer_len_overfull_popleft():
    b = CircularBuffer(5, range(7))
    b.popleft()
    assert len(b) == 4


def test_circular_buffer_maxlen():
    b = CircularBuffer(5)
    assert b.maxlen == 5


def test_circular_buffer_getitem_empty_invalid():
    b = CircularBuffer(5)
    with pytest.raises(IndexError):
        b[0]


def test_circular_buffer_getitem_partial():
    b = CircularBuffer(5, range(3))
    assert b[0] == 0
    assert b[1] == 1
    assert b[2] == 2


def test_circular_buffer_getitem_partial_negative():
    b = CircularBuffer(5, range(3))
    assert b[-1] == 2


def test_circular_buffer_getitem_partial_invalid():
    b = CircularBuffer(5, range(3))
    with pytest.raises(IndexError):
        b[4]


def test_circular_buffer_getitem_partial_invalid_negative():
    b = CircularBuffer(5, range(3))
    with pytest.raises(IndexError):
        b[-10]


def test_circular_buffer_getitem_overfull():
    b = CircularBuffer(5, range(7))
    assert [b[i] for i in range(5)] == [2, 3, 4, 5, 6]


def test_circular_buffer_getitem_overfull_invalid():
    b = CircularBuffer(5, range(3))
    with pytest.raises(IndexError):
        b[5]


def test_circular_buffer_getitem_overfull_invalid_negative():
    b = CircularBuffer(5, range(3))
    with pytest.raises(IndexError):
        b[-10]


def test_circular_buffer_setitem_empty_invalid():
    b = CircularBuffer(5)
    with pytest.raises(IndexError):
        b[0] = 1


def test_circular_buffer_setitem_partial():
    b = CircularBuffer(5, range(3))
    b[0] = -1
    b[1] = -2
    b[2] = -3
    assert list(b) == [-1, -2, -3]


def test_circular_buffer_setitem_partial_invalid():
    b = CircularBuffer(5, range(3))
    with pytest.raises(IndexError):
        b[4] = 1


def test_circular_buffer_setitem_overfull():
    b = CircularBuffer(5, range(7))
    b[1] = -1
    b[2] = -2
    b[3] = -3
    assert list(b) == [2, -1, -2, -3, 6]


def test_circular_buffer_setitem_overfull_invalid():
    b = CircularBuffer(5, range(7))
    with pytest.raises(IndexError):
        b[5] = 1


def test_circular_buffer_delitem_empty_invalid():
    b = CircularBuffer(5)
    with pytest.raises(IndexError):
        del b[0]


def test_circular_buffer_delitem_partial_start():
    b = CircularBuffer(5, range(3))
    del b[0]
    assert list(b) == [1, 2]


def test_circular_buffer_delitem_partial_mid():
    b = CircularBuffer(5, range(3))
    del b[1]
    assert list(b) == [0, 2]


def test_circular_buffer_delitem_partial_end():
    b = CircularBuffer(5, range(3))
    del b[2]
    assert list(b) == [0, 1]


def test_circular_buffer_delitem_overfull_start():
    b = CircularBuffer(5, range(7))
    del b[0]
    assert list(b) == [3, 4, 5, 6]


def test_circular_buffer_delitem_overfull_mid1():
    b = CircularBuffer(5, range(7))
    del b[1]
    assert list(b) == [2, 4, 5, 6]


def test_circular_buffer_delitem_overfull_mid2():
    b = CircularBuffer(5, range(7))
    del b[3]
    assert list(b) == [2, 3, 4, 6]


def test_circular_buffer_delitem_overfull_end():
    b = CircularBuffer(5, range(7))
    del b[4]
    assert list(b) == [2, 3, 4, 5]


def test_circular_buffer_delitem_overfull_negative():
    b = CircularBuffer(5, range(7))
    del b[-3]
    assert list(b) == [2, 3, 5, 6]


def test_circular_buffer_insert_empty():
    b = CircularBuffer(5)
    b.insert(0, 1)
    assert list(b) == [1]


def test_circular_buffer_insert_partial_start():
    b = CircularBuffer(5, range(3))
    b.insert(0, -1)
    assert list(b) == [-1, 0, 1, 2]


def test_circular_buffer_insert_partial_mid():
    b = CircularBuffer(5, range(3))
    b.insert(1, -1)
    assert list(b) == [0, -1, 1, 2]


def test_circular_buffer_insert_partial_last():
    b = CircularBuffer(5, range(3))
    b.insert(2, -1)
    assert list(b) == [0, 1, -1, 2]


def test_circular_buffer_insert_partial_end():
    b = CircularBuffer(5, range(3))
    b.insert(5, -1)
    assert list(b) == [0, 1, 2, -1]


def test_circular_buffer_insert_partial_several():
    b = CircularBuffer(5, range(3))
    b.insert(1, -1)
    assert list(b) == [0, -1, 1, 2]
    b.insert(0, -2)
    assert list(b) == [-2, 0, -1, 1, 2]
    b.insert(0, -3)
    assert list(b) == [-3, 0, -1, 1, 2]
    b.insert(4, -4)
    assert list(b) == [0, -1, 1, 2, -4]
    b.insert(0, -5)
    assert list(b) == [-5, -1, 1, 2, -4]


def test_circular_buffer_insert_full_start():
    b = CircularBuffer(5, range(5))
    b.insert(0, -1)
    assert list(b) == [-1, 1, 2, 3, 4]


def test_circular_buffer_insert_full_mid():
    b = CircularBuffer(5, range(5))
    b.insert(2, -1)
    assert list(b) == [1, 2, -1, 3, 4]


def test_circular_buffer_insert_full_last():
    b = CircularBuffer(5, range(5))
    b.insert(4, -1)
    assert list(b) == [1, 2, 3, 4, -1]


def test_circular_buffer_insert_full_end():
    b = CircularBuffer(5, range(5))
    b.insert(5, -1)
    assert list(b) == [1, 2, 3, 4, -1]


def test_circular_buffer_insert_overfull_start():
    b = CircularBuffer(5, range(7))
    b.insert(0, -1)
    assert list(b) == [-1, 3, 4, 5, 6]


def test_circular_buffer_insert_overfull_mid():
    b = CircularBuffer(5, range(7))
    b.insert(2, -1)
    assert list(b) == [3, 4, -1, 5, 6]


def test_circular_buffer_insert_overfull_last():
    b = CircularBuffer(5, range(7))
    b.insert(4, -1)
    assert list(b) == [3, 4, 5, 6, -1]


def test_circular_buffer_insert_overfull_end():
    b = CircularBuffer(5, range(7))
    b.insert(5, -1)
    assert list(b) == [3, 4, 5, 6, -1]


def test_circular_buffer_append():
    b = CircularBuffer(3)
    b.append(0)
    assert list(b) == [0]
    b.append(1)
    assert list(b) == [0, 1]
    b.append(2)
    assert list(b) == [0, 1, 2]
    b.append(3)
    assert list(b) == [1, 2, 3]
    b.append(4)
    assert list(b) == [2, 3, 4]
    b.append(5)
    assert list(b) == [3, 4, 5]


def test_circular_buffer_pop_empty_invalid():
    b = CircularBuffer(5)
    with pytest.raises(IndexError):
        b.pop()


def test_circular_buffer_pop_partial():
    b = CircularBuffer(5, range(3))
    assert b.pop() == 2
    assert list(b) == [0, 1]
    assert b.pop() == 1
    assert list(b) == [0]


def test_circular_buffer_pop_overfull():
    b = CircularBuffer(5, range(7))
    assert b.pop() == 6
    assert list(b) == [2, 3, 4, 5]
    assert b.pop() == 5
    assert list(b) == [2, 3, 4]


def test_circular_buffer_appendleft():
    b = CircularBuffer(3)
    b.append(0)
    assert list(b) == [0]
    b.appendleft(1)
    assert list(b) == [1, 0]
    b.appendleft(2)
    assert list(b) == [2, 1, 0]
    b.appendleft(3)
    assert list(b) == [3, 2, 1]
    b.appendleft(4)
    assert list(b) == [4, 3, 2]
    b.appendleft(5)
    assert list(b) == [5, 4, 3]


def test_circular_buffer_extendleft_short():
    b = CircularBuffer(4, [-1, -2, -3])
    b.extendleft(range(2))
    assert list(b) == [1, 0, -1, -2]


def test_circular_buffer_extendleft_long():
    b = CircularBuffer(5, [-1, -2, -3])
    b.extendleft(range(7))
    assert list(b) == [6, 5, 4, 3, 2]


def test_circular_buffer_popleft_empty_invalid():
    b = CircularBuffer(5)
    with pytest.raises(IndexError):
        b.popleft()


def test_circular_buffer_popleft_partial():
    b = CircularBuffer(5, range(3))
    assert b.popleft() == 0
    assert list(b) == [1, 2]
    assert b.popleft() == 1
    assert list(b) == [2]


def test_circular_buffer_popleft_overfull():
    b = CircularBuffer(5, range(7))
    assert b.popleft() == 2
    assert list(b) == [3, 4, 5, 6]
    assert b.popleft() == 3
    assert list(b) == [4, 5, 6]


def test_circular_buffer_appends_pops_partial():
    b = CircularBuffer(5)
    b.append(1)
    b.append(2)
    assert list(b) == [1, 2]
    assert b.pop() == 2
    assert list(b) == [1]
    b.append(3)
    b.append(4)
    assert list(b) == [1, 3, 4]
    assert b.popleft() == 1
    assert b.popleft() == 3
    assert list(b) == [4]
    b.appendleft(5)
    assert list(b) == [5, 4]
    assert b.popleft() == 5


def test_circular_buffer_appends_pops_overfull():
    b = CircularBuffer(5, range(7))
    b.append(-1)
    b.append(-2)
    assert list(b) == [4, 5, 6, -1, -2]
    assert b.pop() == -2
    assert b.popleft() == 4
    assert list(b) == [5, 6, -1]
    b.append(-3)
    b.append(-4)
    assert list(b) == [5, 6, -1, -3, -4]
    b.appendleft(-5)
    assert list(b) == [-5, 5, 6, -1, -3]
    assert b.popleft() == -5
    assert b.popleft() == 5
    assert list(b) == [6, -1, -3]
    b.appendleft(-6)
    assert list(b) == [-6, 6, -1, -3]
    assert b.popleft() == -6


def test_circular_buffer_iter_empty():
    b = CircularBuffer(5)
    assert list(iter(b)) == []


def test_circular_buffer_iter_partial():
    b = CircularBuffer(5, range(3))
    assert list(iter(b)) == [0, 1, 2]


def test_circular_buffer_iter_full():
    b = CircularBuffer(5, range(5))
    assert list(iter(b)) == [0, 1, 2, 3, 4]


def test_circular_buffer_iter_overfull():
    b = CircularBuffer(5, range(7))
    assert list(iter(b)) == [2, 3, 4, 5, 6]


def test_circular_buffer_reversed_empty():
    b = CircularBuffer(5)
    assert list(reversed(b)) == []


def test_circular_buffer_reversed_partial():
    b = CircularBuffer(5, range(3))
    assert list(reversed(b)) == [2, 1, 0]


def test_circular_buffer_reversed_full():
    b = CircularBuffer(5, range(5))
    assert list(reversed(b)) == [4, 3, 2, 1, 0]


def test_circular_buffer_reversed_overfull():
    b = CircularBuffer(5, range(7))
    assert list(reversed(b)) == [6, 5, 4, 3, 2]


def test_circular_buffer_contains_partial_true():
    b = CircularBuffer(5, range(3))
    assert 0 in b
    assert 1 in b
    assert 2 in b


def test_circular_buffer_contains_partial_false_int():
    b = CircularBuffer(5, range(3))
    assert -1 not in b
    assert 3 not in b


def test_circular_buffer_contains_partial_false_none():
    b = CircularBuffer(5, range(3))
    assert None not in b


def test_circular_buffer_contains_partial_false_obj():
    b = CircularBuffer(5, range(3))
    assert "foo" not in b


def test_circular_buffer_contains_overfull_true():
    b = CircularBuffer(5, range(7))
    assert 2 in b
    assert 3 in b
    assert 6 in b


def test_circular_buffer_contains_overfull_false_int():
    b = CircularBuffer(5, range(7))
    assert -1 not in b
    assert 0 not in b
    assert 1 not in b
    assert 7 not in b


def test_circular_buffer_contains_overfull_false_none():
    b = CircularBuffer(5, range(7))
    assert None not in b


def test_circular_buffer_contains_overfull_false_obj():
    b = CircularBuffer(5, range(7))
    assert "foo" not in b

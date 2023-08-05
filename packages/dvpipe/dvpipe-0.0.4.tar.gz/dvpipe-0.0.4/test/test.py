import unittest
from dvpipe import pipe

raw_data = {'foo': 1, 'bar': 2}


def subtract_foo(data):
    data['foo'] = data['foo'] - 1
    return data


def add_bar(data):
    data['bar'] = data['bar'] + 1
    return data


def add_entry(data, entry):
    data.update(entry)
    return data


class DvPipeTestCase(unittest.TestCase):

    def test_pipe(self):
        data = (pipe(raw_data,
                    subtract_foo,
                    add_bar,
                    (add_entry, {'foobar': 5})))
        self.assertEqual(data, {'foo': 0, 'foobar': 5, 'bar': 3})


if __name__ == "__main__":
    unittest.main()

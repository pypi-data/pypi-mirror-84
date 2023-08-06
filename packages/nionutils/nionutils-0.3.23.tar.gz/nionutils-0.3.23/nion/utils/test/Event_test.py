# standard libraries
import unittest

# third party libraries

# local libraries
from nion.utils import Event


class TestEventClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_event_owner(self):
        class A:
            def __init__(self):
                pass

        a = A()
        e = Event.Event()
        h = [0]

        def up():
            h[0] += 1

        e.listen(up, owner=a)
        e.fire()
        self.assertEqual(h[0], 1)
        del a
        e.fire()
        self.assertEqual(h[0], 1)

    def test_multiple_event_owner(self):
        class A:
            def __init__(self):
                pass

        a = A()
        e = Event.Event()
        h = [0]
        i = [10]

        def up():
            h[0] += 1

        def down():
            i[0] -= 1

        e.listen(up, owner=a)
        e.listen(down, owner=a)
        e.fire()
        self.assertEqual(h[0], 1)
        self.assertEqual(i[0], 9)
        del a
        e.fire()
        self.assertEqual(h[0], 1)
        self.assertEqual(i[0], 9)

    def test_event_listen(self):
        count = 0

        def handle_event():
            nonlocal count
            count += 1

        e = Event.Event()
        with e.listen(handle_event):
            e.fire()
        self.assertEqual(1, count)
        e.fire()
        self.assertEqual(1, count)

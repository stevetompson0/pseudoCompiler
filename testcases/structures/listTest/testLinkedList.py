import unittest
from structure.config import *

class MyTestCase(unittest.TestCase):
    def test_node(self):
        x = ListNode(3)
        print(x)

    def test_add(self):
        x = LinkedList()
        x.addLast(1)
        x.addLast(2)
        x.addLast(3)
        x.addLast(4)

        print(x)
        print(x.eleFlags)
        print(x.head)
        print(x.head.next)


    def test_add_with_index(self):
        x = LinkedList()
        x.addLast(1)
        x.addLast(2)
        x.addLast(3)
        print(x)
        print(x.eleFlags)
        x.add(1,4)
        print(x)
        print(x.eleFlags)

    def test_get(self):
        x = LinkedList()
        x.addLast(1)
        x.addLast(2)
        x.addLast(3)
        self.assertEquals(x.get(1).item, 2)
        self.assertEquals(x.get(1).prev.item, 1)
        self.assertEquals(x.get(1).next.item, 3)

    def test_pop(self):
        x = LinkedList()
        x.addLast(1)
        x.addLast(2)
        x.addLast(3)
        print(x.pop())

    def test_search(self):
        x = LinkedList()
        x.addLast(1)
        x.addLast(2)
        x.addLast(1)
        print(x.search(1))

    def test_remove(self):
        x = LinkedList()
        x.addLast(1)
        x.addLast(2)
        x.addLast(3)
        x.remove(2)
        print(x)
        print(x.get(1).next)


    def test_remove_obj(self):
        x = LinkedList()
        x.addLast(1)
        x.addLast(2)
        x.addLast(3)
        x.removeValue(2)
        print(x)
        print(x.get(1).next)

    def test_swap(self):
        x = LinkedList()
        x.addLast(1)
        x.addLast(2)
        x.addLast(3)

        x.swap(0,1)
        print(x)
        print(x.get(0))
        print(x.get(0).next)
        print(x.eleFlags)

    def test_clear_reset(self):
        x = LinkedList()
        x.addLast(1)
        x.addLast(2)
        x.addLast(3)
        x.resetFlags()
        print(x)
        print(x.eleFlags)

    def test_random(self):
        x = LinkedList.random()
        print(x)

if __name__ == '__main__':
    unittest.main()

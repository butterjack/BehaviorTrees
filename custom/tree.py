
##############################################################################
SUCCESS = "Success"
FAILURE = "Failure"
RUNNING = "Running"

class Node(object):
    def __init__(self):
        self.desc = None
        self._name = None

    @property
    def name(self):
        return self._name or self.__class__.__name__

    @name.setter
    def name(self, value):
        self._name = value

    def clone(self):
        c = self.__class__()
        c.copy_from(self)
        return c

    def copy_from(self, other):
        self.desc = other.desc

    def __or__(self, sibling):
        return Select([self, sibling])

    def __rshift__(self, sibling):
        return Sequence([self, sibling])

    def __floordiv__(self, desc):
        c = self.clone()
        c.desc = desc
        return c


class Composite(Node):
    def __init__(self, children=None):
        super(Composite, self).__init__()
        self.children = children or []

    def copy_from(self, other):
        super(Composite, self).copy_from(other)
        self.children = other.children[:]

class Select(Composite):
    def __or__(self, child):
        children = self.children[:]
        children.append(child)
        return Select(children)

    class Iterator(object):
        def __init__(self, bb, node):
            self.iterations = self._make_iterations(bb, node)

        def _make_iterations(self, bb, node):
            for c in node.children:
                it = bb.new_iterator(c)
                while True:
                    x = it()
                    if x == RUNNING:
                        yield x
                    elif x == SUCCESS:
                        yield x
                        return
                    else:
                        assert x == FAILURE
                        break

            # all children are failed
            yield FAILURE

        def __call__(self):
            return next(self.iterations)


class Sequence(Composite):
    def __rshift__(self, child):
        children = self.children[:]
        children.append(child)
        return Sequence(children)

    class Iterator(object):
        def __init__(self, bb, node, *args, **kwargs):
            self.iterations = self._make_iterations(bb, node)

        def _make_iterations(self, bb, node):
            for c in node.children:
                it = bb.new_iterator(c)
                while True:
                    x = it()
                    if x == RUNNING:
                        yield x
                    elif x == FAILURE:
                        yield x
                        return
                    else:
                        assert x == SUCCESS
                        break

            # all children are failed
            yield SUCCESS

        def __call__(self):
            return next(self.iterations)
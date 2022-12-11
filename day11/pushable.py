class Pushable:
    """
    Wraps any iterator so that you can peek ahead, push values back onto the stream and check for empty.
    See my post https://stackoverflow.com/a/51032721/735952
    """

    def __init__(self, iter):
        self.source = iter
        self.stored = []

    def __iter__(self):
        return self

    def __bool__(self):
        if self.stored:
            return True
        try:
            self.stored.append(next(self.source))
        except StopIteration:
            return False
        return True

    def push(self, value):
        self.stored.append(value)

    def peek(self):
        if self.stored:
            return self.stored[-1]
        value = next(self.source)
        self.stored.append(value)
        return value

    def __next__(self):
        if self.stored:
            return self.stored.pop()
        return next(self.source)
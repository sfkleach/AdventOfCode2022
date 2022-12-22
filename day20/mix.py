
class Link:

    def __init__( self, value ):
        self.value = value
        self.prev = self
        self.next = self


class Mix:

    def __init__( self, data ):
        self._items = tuple( data )
        start = Link( 'DUMMY' )
        latest = start
        for d in data:
            new = Link( d )
            old = latest.next
            latest.next = new
            new.next = old
            old.prev = new
            new.prev = latest
            latest = new
        lhs = start.prev
        rhs = start.next
        lhs.next = rhs
        rhs.prev = lhs
        self._cycle = rhs

    def mv( self, item ):
        A = self._cycle
        for _ in range( 0, len( self._items ) ):
            if A.value == item:
                if item > 0:
                    for i in range( 0, item ):
                        lhs = A.prev
                        B = A.next
                        rhs = B.next
                        A.prev = B
                        A.next = rhs
                        B.prev = lhs
                        B.next = A
                        lhs.next = B
                        rhs.prev = A
                elif item < 0:
                    for i in range( 0, abs( item ) ):
                        GOT HERE

                        

def readMixFile( fname ):
    data = []
    with open( fname, 'r' ) as file:
        for line in file:
            data.append( int( line.strip() ) )
    return Mix( data )

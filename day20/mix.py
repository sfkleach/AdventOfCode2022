class Mix:

    def __init__( self, data ):
        self._original_order = tuple( data )
        self._items = list( data )

    def __len__( self ):
        return len( self._original_order )
        
    def mv( self, item ):
        N = len( self._items )
        i = self.find( item )
        ntransposes = item % (N-1)
        for k in range( 0, ntransposes ):
            self._items[(i+k)%N] = self._items[(i+k+1)%N]
        self._items[(i + ntransposes)%N] = item

    def mix( self ):
        for item in self._original_order:
            self.mv( item )

    def find( self, item ):
        N = len( self._items )
        for i in range( 0, N ):
            if self._items[i] == item:
                return i

    def lookup( self, index ):
        base = self.find( 0 )
        # print( index, ( base + index ), len( self ), ( base + index ) % len( self ), self._items[ ( base + index ) % len( self ) ] )
        return self._items[ ( base + index ) % len( self ) ]


def readMixFile( fname ):
    data = []
    with open( fname, 'r' ) as file:
        for line in file:
            data.append( int( line.strip() ) )
    return Mix( data )

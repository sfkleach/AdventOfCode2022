class DataBuilder:

    def __init__( self ):
        self._current = []
        self._data = []

    def add( self, number ):
        self._current.append( number )

    def end( self ):
        if self._current:
            self._data.append( self._current )
            self._current = []

    def result( self ):
        self.end()
        d = self._data
        self._data = []
        return d

def parseCaloriesFile( fname ):
    g = DataBuilder()
    with open( fname, 'r' ) as file:
        for line in map( lambda L: L.strip(), file ):
            if line:
                g.add( int( line ) )
            else:
                g.end()
    return g.result()

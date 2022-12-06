def findMarker( line, ndistinct ):
    for i in range( 0, len(line) - ndistinct + 1 ):
        if len( set( line[i:i+ndistinct] ) ) == ndistinct:
            return i+ndistinct
    return None

def findStartOfPacketMarker( line ):
    return findMarker( line, 4 )

def findStartOfMessageMarker( line ):
    return findMarker( line, 14 )
    
def readSignalFile( fname ):
    with open( fname, 'r' ) as file:
        return file.read()

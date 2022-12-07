import re 

class File:

    def __init__( self, size ):
        self._size = size

    def size( self ):
        return self._size

class Dir:

    def __init__( self ):
        self._files = {}

    def addFileInfo( self, fname, size ):
        if fname in self._files:
            raise Exception( "Did not expect this" )
        self._files[ fname ] = File( size )

    def totalFileSizes( self ):
        return sum( f.size() for f in self._files.values() )

class FileSystemInfo:

    def __init__( self ):
        self._info = {}

    def _addEmptyDirectories( self, path ):
        if path not in self._info:
            self._info[ path ] = Dir()
        if path:
            self._addEmptyDirectories( path[:-1] )

    def addFileInfo( self, path, fname, size ):
        self._addEmptyDirectories( path )
        dir = self._info[ path ]
        dir.addFileInfo( fname, size )

    def directories( self ):
        return self._info.keys()

    # @staticmethod
    # def isStrictSubpath( subpath, path ):
    #     return len( path ) < len( subpath ) and all( a==b for a,b in zip( path, subpath ) )

    @staticmethod
    def isSubpath( subpath, path ):
        return len( path ) <= len( subpath ) and all( a==b for a,b in zip( path, subpath ) )

    # def strictSubPaths( self, path ):
    #     for p in self.directories():
    #         if FileSystemInfo.isStrictSubpath( p, path ):
    #             yield p

    def subPaths( self, path ):
        for p in self.directories():
            if FileSystemInfo.isSubpath( p, path ):
                yield p

    def totalSize( self, path ):
        return sum( self._info[ p ].totalFileSizes() for p in self.subPaths( path ) )

def readConsoleTraceFile( fname ):
    info = FileSystemInfo()
    with open ( fname, 'r' ) as file:
        path = []
        lineno = 0
        for line in file:
            lineno += 1
            words = line.split()
            N = len( words )
            if re.match( r'\$ cd /', line ):
                path = [] 
            elif re.match( r'\$ cd \.\.', line ):
                if not path:
                    print( 'LINENO', lineno )
                path.pop()
            elif re.match( r'\$ cd [^ ]+', line ):
                dir = words[2]
                path.append( dir )
            elif re.match( r'\$ ls', line ):
                pass
            elif re.match( 'dir [^ ]+', line ):
                pass
            elif re.match( '[0-9]+ [^ ]+', line ):
                info.addFileInfo( tuple( path ), words[1], int( words[0] ) )
            else:
                raise Exception( f"Bad line {line} on line {lineno}")
    return info

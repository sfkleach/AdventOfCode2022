import re 

class File:

    def __init__( self, size ):
        self._size = size

    def size( self ):
        return self._size

class Dir:

    def __init__( self, name ):
        self._name = name
        self._files = {}
        self._subdirs = {}

    def addFileInfo( self, fname, size ):
        if fname in self._files:
            raise Exception( "Did not expect this" )
        self._files[ fname ] = File( size )

    def fetchSubDir( self, name ):
        try:
            return self._subdirs[ name ]
        except KeyError:
            d = Dir(name)
            self._subdirs[ name ] = d
            return d

    def sumFileSizes( self ):
        return sum( f.size() for f in self._files.values() )

    def totalSize( self ):
        return self.sumFileSizes() + sum( d.totalSize() for d in self._subdirs.values() )

    def scanDirs( self ):
        yield self
        for d in self._subdirs.values():
            yield from d.scanDirs()

class FileSystemInfo:

    def __init__( self ):
        self._root = Dir('')

    def addFileInfo( self, path, fname, size ):
        dir = self._root
        for dname in path:
            dir = dir.fetchSubDir( dname )
        dir.addFileInfo( fname, size )

    def scanDirs( self ):
        return self._root.scanDirs()

    def totalSize( self ):
        return self._root.totalSize()

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

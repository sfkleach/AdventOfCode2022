import abc

class Monkey:
    @abc.abstractmethod
    def eval( self, env ):
        ...

class Constant( Monkey ):
    def __init__( self, n ):
        self._value = n
    def __repr__( self ):
        return str( self._value )
    def eval( self, env ):
        return self._value

class Operation( Monkey ):
    def __init__( self, *, op, lhs, rhs ):
        self._op = op
        self._lhs = lhs
        self._rhs = rhs
    def __repr__( self ):
        return f'<{self._lhs} {self._op} {self._rhs}>'
    def eval( self, env ):
        L = env[ self._lhs ].eval( env )
        R = env[ self._rhs ].eval( env )
        if self._op == "-":
            return L - R
        elif self._op == "+":
            return L + R
        elif self._op == "*":
            return L * R
        elif self._op == "/":
            return L // R
        else:
            raise Exception( 'BAD: ' + self._op )


def readMonkeysFile( fname ):
    monkey_map = {}
    with open( fname, 'r' ) as file:
        for line in file:
            words = line.split()
            assert words[0][-1] == ":"
            name = words[0][:-1]
            if len( words ) == 2:
                monkey_map[ name ] = Constant( int( words[1] ) )
            elif len( words ) == 4:
                monkey_map[ name ] = Operation( op=words[2], lhs=words[1], rhs=words[3] )
            else:
                raise Exception( 'BAD INPUT' )
    return monkey_map


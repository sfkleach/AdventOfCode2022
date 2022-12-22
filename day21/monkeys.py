import abc

class Monkey:
    def __init__( self, name ):
        self.name = name
    @abc.abstractmethod
    def eval( self ):
        ...
    def isConstant( self ) -> bool:
        return False
    def simplify( self ):
        return self
    def resolve( self, map ):
        pass
    @abc.abstractmethod
    def solve( self, N ):
        ...

class Constant( Monkey ):
    def __init__( self, name, n ):
        super().__init__( name )
        self._value = n
    def __repr__( self ):
        return str( self._value )
    def eval( self ):
        return self._value
    def value( self ):
        return self._value
    def isConstant( self ):
        return True
    def solve( self, N ):
        if self._value != N:
            raise Exception( 'CONSTANT' )

class Variable( Monkey ):
    def __init__( self, name, n ):
        super().__init__( name )
        self.value = n
    def __repr__( self ):
        return f"^self.value"
    def eval( self ):
        return self.value    
    def solve( self, N ):
        print( 'SOLUTION', N )

class Operation( Monkey ):
    def __init__( self, name, *, op, lhs, rhs ):
        super().__init__( name )
        self._op = op
        self._lhs = lhs
        self._rhs = rhs
    def resolve( self, map ):
        if isinstance( self._lhs, str ):
            self._lhs = map[ self._lhs ]
            self._lhs.resolve( map )
        if isinstance( self._rhs, str ):
            self._rhs = map[ self._rhs ]           
            self._rhs.resolve( map )
    def __repr__( self ):
        return f'<{self._lhs} {self._op} {self._rhs}>'
    def eval( self ):
        L = self._lhs.eval()
        R = self._rhs.eval()
        if self._op == "-":
            return L - R
        elif self._op == "+":
            return L + R
        elif self._op == "*":
            return L * R
        elif self._op == "/":
            if ( L % R ) != 0:
                print( 'AHA', L, R, L // R, L % R )
            return L // R
        elif self._op == "==":
            return L == R
        else:
            raise Exception( 'BAD: ' + self._op )
    def simplify( self ):
        L = self._lhs.simplify()
        R = self._rhs.simplify()  
        if L.isConstant() and R.isConstant():
            if self._op == "-":
                return Constant( 'anon', L.value() - R.value() )
            elif self._op == "+":
                return Constant( 'anon', L.value() + R.value() )
            elif self._op == "*":
                return Constant( 'anon', L.value() * R.value() )
            elif self._op == "/":
                return Constant( 'anon', L.value() // R.value() )
            elif self._op == "==":
                return Constant( 'anon', L.value() == R.value() )
            else:
                raise Exception( 'BAD: ' + self._op )                 
        else:
            return Operation( self.name, op=self._op, lhs=L, rhs=R )
    def solve( self, N ):
        L = self._lhs
        R = self._rhs
        if L.isConstant():
            if self._op == "-":
                # N = L - R => R = L - N
                R.solve( L.value() - N )
            elif self._op == "+":
                # N = L + R => R = N - L
                R.solve( N - L.value() )
            elif self._op == "*":
                # N = L * R => R = N / L
                R.solve( N // L.value() )
            elif self._op == "/":
                # N = L / R => R = L / N
                R.solve( L.value() // N )
            elif self._op == "==":
                R.solve( L.value() )
            else:
                raise Exception( 'BAD: ' + self._op )
        elif R.isConstant():
            if self._op == "-":
                # N = L - R => L = N + R
                L.solve( N + R.value() )
            elif self._op == "+":
                # N = L + R => L = N - R 
                L.solve( N - R.value() )
            elif self._op == "*":
                # N = L * R => L = N / R
                L.solve( N // R.value() )
            elif self._op == "/":
                # N = L / R => R = L / N
                L.solve( R.value() * N )
            elif self._op == "==":
                L.solve( R.value() )
            else:
                raise Exception( 'BAD: ' + self._op )
        else:
            raise Exception( 'BAD' )

def readMonkeysFile( fname, var ):
    monkey_map = {}
    with open( fname, 'r' ) as file:
        for line in file:
            words = line.split()
            assert words[0][-1] == ":"
            name = words[0][:-1]
            if len( words ) == 2:
                monkey_map[ name ] = ( Variable if var == name else Constant )( name, int( words[1] ) )
            elif len( words ) == 4:
                monkey_map[ name ] = Operation( name, op=words[2], lhs=words[1], rhs=words[3] )
            else:
                raise Exception( 'BAD INPUT' )
    root = monkey_map['root']
    root.resolve( monkey_map )
    return monkey_map


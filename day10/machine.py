import abc

class Machine:

    def __init__( self, instructions ):
        self._x = 1
        self._cycles_completed = 0
        self._pc = 0
        self._instructions = tuple( insertTimingNoops( instructions ) )

    def tick( self ):
        inst = self._instructions[ self._pc ]
        self._pc += 1
        self._cycles_completed += 1
        inst.run( self )

    def runTo( self, start_of_cycle ):
        while self.atStartOfCycle() < start_of_cycle:
            self.tick()

    def signalStrength( self ):
        return self._x * self.atStartOfCycle()

    def atStartOfCycle( self ):
        return self._cycles_completed + 1

    def vram( self, N ):
        """video ram value = is the sprite pixel at position N on?"""
        return abs( self._x - N ) <= 1

    def noop( self ):
        pass

    def add( self, n ):
        self._x += n

class Instruction:

    @abc.abstractmethod
    def run( self, a_mc ): ...
    
    def __iter__( self ):
        yield self


class NoopInstruction( Instruction ):
    
    def run( self, mc ):
        mc.noop()

    def __repr__( self ):
        return 'NOOP'


class AddInstruction( Instruction ):
    
    def __init__( self, n ):
        self._n = n

    def __repr__( self ):
        return f"ADD({self._n})"

    def __iter__( self ):
        yield NoopInstruction()
        yield self

    def run( self, mc ):
        mc.add( self._n )


def insertTimingNoops( instructions ):
    for inst in instructions:
        yield from inst

def readSignalProgram( fname ):
    with open( fname, 'r' ) as file:
        for line in file:
            words = line.split()
            if len( words ) == 1:
                yield NoopInstruction()
            else:
                yield AddInstruction( int( words[1] ) )

import abc

class Machine:

    def __init__( self, instructions ):
        # The single X register.
        self._x: int= 1
        # A count of completed work cycles. Note this is less than the notion 
        # of "during a cycle".
        self._cycles_completed: int = 0
        # Virtual program counter.
        self._pc: int = 0
        # A vector of instructions that is expanded into single tick instructions.
        # [It could actually be an instruction stream, given we have no backward jumps.]
        self._instructions = tuple( insertTimingNoops( instructions ) )

    def tick( self ):
        """Load an instruction, bump the virtual program counter and cycle count, execute the instruction"""
        inst = self._instructions[ self._pc ]
        self._pc += 1
        self._cycles_completed += 1
        inst.run( self )

    def runTo( self, start_of_cycle ):
        """Run until a particular clock value is reached/exceeded."""
        while self.atStartOfCycle() < start_of_cycle:
            self.tick()

    def signalStrength( self ) -> int:
        return self._x * self.atStartOfCycle()

    def atStartOfCycle( self ) -> int:
        return self._cycles_completed + 1

    def vram( self, N ) -> str:
        """
        No need to implement an virtual VRAM. It's enough to dynamically 
        compute the value since it is only 3 '#'s in a row.
        video ram value at N = Is the sprite pixel # or .?
        """
        return '#' if abs( self._x - N ) <= 1 else '.'

    def noop( self ):
        """These are the visitor callbacks."""
        pass

    def add( self, n ):
        """These are the visitor callbacks."""
        self._x += n

class Instruction:
    """
    Instructions follow the Visitor pattern. They also know how to
    expand themselves into a sequence of single-tick instructions.
    """

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
        """Insert a no-op to simulate the effect of an add taking two ticks."""
        yield NoopInstruction()
        yield self

    def run( self, mc ):
        mc.add( self._n )


def insertTimingNoops( instructions ):
    """
    To avoid dealing with multi-tick instructions I insert no-ops in
    front of 2-tick add instructions. This works fine as there are no jumps or
    microcode loops in this instruction set. In effect this converts the 
    instruction set into single tick instructions.
    """
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

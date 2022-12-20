from factory import *

B = readBlueprintsFile( 'ex1.txt' )
F = Factory( bluedata=B[0]._bluedata )
S = Simulation( F )
while S._best_factory is None:
    S.tick()

print( S._best_factory.bestPossibleScore() )

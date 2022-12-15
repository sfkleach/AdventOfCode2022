import re
from collections import deque

from vector import Vector


class Sensor:

    def __init__( self, x, y, bx, by ):
        self._xy = Vector( x, y )
        self._bxy = Vector( bx, by )

    def radius( self ):
        return ( self._xy - self._bxy ).manhattan()

    def x( self ):
        return self._xy.x()

    def y( self ):
        return self._xy.y()

    def beacon( self ):
        return self._bxy


def tryMergeRanges( r1, r2 ):
    if r1.stop < r2.start:
        [ r1, r2 ]
    elif r2.stop < r1.start:
        [ r2, r1 ]
    else:
        [ range( min( r1.start, r2.start ), max( r1.stop, r2.stop ) ) ]
        

class InAnyOf:

    def __init__( self, ranges ):
        self._ranges = tuple()   # Main as sorted disjoint ranges.
        for r in ranges:
            # print( 'RANGE', self._ranges )
            self._ranges = tuple( self._addRange( r ) )

    def _addRange( self, new_range ):
        ranges = deque( self._ranges )
        while ranges:
            r = ranges.popleft()
            if r.stop < new_range.start:
                yield r
            elif new_range.stop < r.start:
                yield new_range
                yield r
                yield from ranges
                return
            else:
                new_range = range( min( r.start, new_range.start ), max( r.stop, new_range.stop ) )
        yield new_range

    def covers( self, a_range ):
        for r in self._ranges:
            if r.stop < a_range.start:
                pass
            elif a_range.stop < r.start:
                return False
            else:
                return r.start <= a_range.start and r.stop >= a_range.stop

    def __contains__( self, x ):
        for p in self._ranges:
            if x in p:
                return True
        return False

    def __iter__( self ):
        for p in self._ranges:
            yield from p


class SensorArray:

    def __init__( self, sensors ):
        self._sensors = tuple( sensors )

    def _intersect( self, line_y ):
        for sensor in self._sensors:
            r = sensor.radius()
            dy = abs( sensor.y() - line_y )
            delta = r - dy
            if delta >= 0:
                # print( sensor.x(), sensor.y(), sensor.radius(), delta, 2 * delta + 1 )
                yield range( sensor.x() - delta, sensor.x() + delta + 1 )

    def intersect( self, line_y ):
        return InAnyOf( self._intersect( line_y ) )

    def beacons( self, line_y ):
        for sensor in self._sensors:
            bxy = sensor.beacon()
            if bxy.y() == line_y:
                yield bxy.x()
    

def readSensorArrayFile( fname ):
    with open( fname, 'r' ) as file:
        return SensorArray( Sensor( *map( int, re.findall( '[-]?[0-9]+', line ) ) ) for line in file )

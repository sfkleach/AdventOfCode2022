# [AX] = rock 
# [BY] = paper
# [CZ] = scissors
#                   win loss draw
# rock < paper      AY  AZ   AX
# paper < scissors  BZ  BX   BY
# scissors < rock   CX  CY   CZ
# 
#   X = +1, Y = +2, Z = +3

DECODE_AS_MOVE = { 'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y': 1, 'Z': 2 }

def score( them_code, us_code ):
    d = (us_code - them_code) % 3
    bonus = 6 if d == 1 else 3 if d == 0 else 0
    us_score = us_code + 1
    return bonus + us_score

def eval_play( them_us ):
    ( them_play, us_play ) = them_us
    them_code = DECODE_AS_MOVE[ them_play ]
    us_code = DECODE_AS_MOVE[ us_play ]
    return score( them_code, us_code )

def mapUsOutcomeToUsCode( them_code, us_outcome ):
    # X = lose, Y = draw, Z = win
    if us_outcome == 'Y':
        return them_code
    elif us_outcome == 'Z':
        return ( them_code + 1 ) % 3
    elif us_outcome == 'X':
        return ( them_code + 2 ) % 3

def eval_outcome( them_us ):
    ( them_play, us_outcome ) = them_us
    them_code = DECODE_AS_MOVE[ them_play ]
    us_code = mapUsOutcomeToUsCode( them_code, us_outcome )
    return score( them_code, us_code )

def entriesOfRockPaperScissorsFile( fname ):
    with open( fname, 'r' ) as file:
        for line in file:
            yield tuple(line.split())

def parseRockPaperScissorsFile( fname ):
    return list( entriesOfRockPaperScissorsFile( fname ) )
        
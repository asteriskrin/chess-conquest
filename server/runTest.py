'''
Run unit test
'''

from tests.buyPawnTest import buyPawnTest
from tests.fusionTest import fusionTest
from tests.promotePawnNotEnoughStar import promotePawnNotEnoughStar
from tests.promotePawnWhenNotTurnTest import promotePawnWhenNotTurnTest
from tests.promotePawnTest import promotePawnTest
from tests.startGameTest import startGameTest
from tests.makeMoveWhenNotTurn import makeMoveWhenNotTurn
from tests.turnTest import turnTest
from tests.roomTest import roomTest
from tests.movePieceTest import movePieceTest
from tests.nonHostStartGameTest import nonHostStartGameTest
from tests.illegalMoveTest import illegalMoveTest
from tests.eatOwnPawnTest import eatOwnPawnTest
from tests.disconnectWinnerTest import disconnectWinnerTest
from tests.joinWithSameNameTest import joinWithSameNameTest
from tests.fusionOnNotEmptyBoxTest import fusionOnNotEmptyBoxTest
from tests.disconnectAtTurnTest import disconnectAtTurnTest
from tests.disconnectWithUnalivePlayerTest import disconnectWithUnalivePlayerTest

def main():
    test = 0
    success = 0

    test += 1
    if roomTest(): success += 1

    test += 1
    if movePieceTest(): success += 1

    test += 1
    if turnTest(): success += 1

    test += 1
    if makeMoveWhenNotTurn(): success += 1

    test += 1
    if startGameTest(): success += 1

    test += 1
    if nonHostStartGameTest(): success += 1

    test += 1
    if illegalMoveTest(): success += 1

    test += 1
    if eatOwnPawnTest(): success += 1

    test += 1
    if promotePawnTest(): success += 1

    test += 1
    if promotePawnWhenNotTurnTest(): success += 1

    test += 1
    if promotePawnNotEnoughStar(): success += 1

    test += 1
    if fusionTest(): success += 1

    test += 1
    if buyPawnTest(): success += 1

    test += 1
    if disconnectWinnerTest(): success += 1

    test += 1
    if joinWithSameNameTest(): success += 1

    test += 1
    if fusionOnNotEmptyBoxTest(): success += 1

    test += 1
    if disconnectAtTurnTest(): success += 1

    test += 1
    if disconnectWithUnalivePlayerTest(): success += 1

    print("{}/{} test passed.".format(success, test))

if __name__ == "__main__":
    main()
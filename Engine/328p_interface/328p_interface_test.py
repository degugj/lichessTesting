# Testing module for 328p_inteface.py integration

#  WARNING: TEST WILL NOT WORK WITHOUT MODIFICATION TO GAMESTATE. CONSTRUCTOR MUST SUPPORT NONE FOR GAMEQUEUE

from Engine.gameState import GameState as gs
interface = __import__('328p_interface')

gamestate = gs() # Instantiate test gamestate

posMap = interface.gamestate_to_position_map(gamestate) # convert 8x8 to position map
interface.print_posMap(posMap)
print('')
heurMap = interface.create_heuristic_map(posMap, 'f1')
interface.print_posMap(heurMap)

print(interface.astar(heurMap, heurMap[0][0]))

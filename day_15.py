
# Before doing this puzzle, create a new branch, refactor part n into new main() functions and call those from if __name__
# this way you can add tests to act on actual puzzle inputs. Reason being, sometimes testcases aren't enough or are too small.
# * Take latest iteration of IntCodeMachine and copy it into a new shared file/module.

# Steps of Day 15
#   Part 1: use intcoderobot to map whole dungeon, create a graph from that mapping and apply A* to get shortest path between starting position and O2 position, since this graph is useful later on, don't bother to reduce intersteps, just keep all nodes as discovered (barring any performance issues). On secound note, graph could be a nested dict, which would have neightbours built-in. This could be helpful for Djikstras and part 2.
#   Part 2: using previously obtained graph, perform a floodfill while tracking ticks

# Use robot to get graph G of maze and O2 system

# Apply A* to G to get optimal path from Start to O2

# Apply floodfill to G from O2, track steps to fill all non wall nodes
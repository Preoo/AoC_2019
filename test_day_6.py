import unittest
from day_6 import StarSystem
class Day6_Orbits_TestCase(unittest.TestCase):
    sample_data = \
            '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L'''

    def test_SampleOrbits(self):
        starsystem = StarSystem.from_string(self.sample_data)
        self.assertEqual(3, starsystem.get_total_orbits_to_COM('D'), f'Wrong count of direct and indirect orbits')
        self.assertEqual(7, starsystem.get_total_orbits_to_COM('L'), f'Wrong count of direct and indirect orbits')
        self.assertEqual(0, starsystem.get_total_orbits_to_COM(starsystem.center_of_mass), f'COM should not orbit anything')
    def test_CountAllOrbits(self):
        
        starsystem = StarSystem.from_string(self.sample_data)
        self.assertEqual(42, len(starsystem), f'Wrong count of direct and indirect orbits')
    def test_Find_COM_Node(self):

        starsystem = StarSystem.from_string(self.sample_data)
        self.assertEqual('COM', starsystem.center_of_mass, f'Failed to set correct root node')

    def test_HopsRequiredToMigrateOrbits(self):

        starsystem = StarSystem.from_string(self.sample_data)

        self.assertEqual(4, starsystem.get_migration_hops('K', 'I') + 2, f'Incorrect count of hops to migrate to same orbit' )

if __name__ == "__main__":
    unittest.main()
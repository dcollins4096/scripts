import PreviousRun
import RunTrackerStuff
import unittest

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        self.userParam = RunTrackerStuff.rtStuff()
        self.previous = PreviousRun.PreviousRun('./RunTracker.xml')

    def testshuffle(self):
        # make sure the shuffled sequence does not lose any elements
        self.assert_(self.userParam.submitCommand)
        self.assertEqual(self.previous.Name,"TestSim0")
                    
if __name__ == '__main__':
    unittest.main()

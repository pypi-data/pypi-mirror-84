from unittest import TestCase

import pier_mob

class TestVersion(TestCase):
    def test_version(self):
        self.assertTrue(pier_mob.version() == pier_mob.cli.__version__)
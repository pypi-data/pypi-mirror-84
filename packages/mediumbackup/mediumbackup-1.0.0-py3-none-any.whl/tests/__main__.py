import unittest
import filecmp
import os
import shutil

import mediumbackup as mb

TEST_BACKUP_DIR = os.path.join("tests","backup")
REFERENCE_STORY_NAME = "2020-10-05 come-aggiungere-i-caratteri-ma"

class MediumStoriesTest(unittest.TestCase):
    
    def test_story(self):
        for format in ("html", "md"):
            mb.backup_stories(username="lucafrance", backup_dir=TEST_BACKUP_DIR, format=format)
            file_extension = "." + format
            test_file = os.path.join(TEST_BACKUP_DIR, REFERENCE_STORY_NAME) + file_extension
            reference_file = os.path.join("tests", REFERENCE_STORY_NAME) + file_extension
            self.assertTrue(os.path.exists(test_file))
            self.assertTrue(filecmp.cmp(test_file, reference_file, shallow=False))
        shutil.rmtree(TEST_BACKUP_DIR)
        return
        
        
if __name__ == "__main__":
    unittest.main()

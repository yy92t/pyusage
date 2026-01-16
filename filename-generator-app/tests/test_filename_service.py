import unittest
from app.services.filename_service import generate_file_name

class TestFilenameService(unittest.TestCase):

    def test_generate_file_name(self):
        prefix = "report_"
        suffix = "_v1"
        extension = "txt"
        file_name = generate_file_name(prefix=prefix, suffix=suffix, extension=extension)
        
        self.assertTrue(file_name.startswith(prefix))
        self.assertIn("_", file_name)
        self.assertTrue(file_name.endswith(f"{suffix}.{extension}"))
        self.assertIn(str(datetime.datetime.now().year), file_name)

    def test_generate_file_name_without_suffix(self):
        prefix = "data_"
        extension = "csv"
        file_name = generate_file_name(prefix=prefix, extension=extension)
        
        self.assertTrue(file_name.startswith(prefix))
        self.assertTrue(file_name.endswith(f".{extension}"))

    def test_generate_file_name_with_different_extension(self):
        prefix = "log_"
        suffix = "_v2"
        extension = "log"
        file_name = generate_file_name(prefix=prefix, suffix=suffix, extension=extension)
        
        self.assertTrue(file_name.endswith(f"{suffix}.{extension}"))

if __name__ == '__main__':
    unittest.main()
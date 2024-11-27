import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TheFirstConfig.emulator import Emulator
from TheFirstConfig.commands import chmod, date, tail, ls, cd, exit

class TestEmulator(unittest.TestCase):
    def setUp(self):
        with patch('xml.etree.ElementTree.parse') as mock_parse:
            mock_parse.return_value.getroot.return_value.find.side_effect = [
                type('obj', (object,), {'text': 'test-pc'})(),
                type('obj', (object,), {'text': 'virtual_fs.tar'})()
            ]
            self.emulator = Emulator('config.xml')
        self.emulator.fs = {
            '/': None,
            '/file1.txt': type('obj', (object,), {'mode': 0o644})(),
            '/file2.txt': type('obj', (object,), {'mode': 0o644})(),
            '/dir1/': None,
            '/dir1/file3.txt': type('obj', (object,), {'mode': 0o644})()
        }

class TestChmod(TestEmulator):
    def test_chmod_success(self):
        with patch('builtins.print') as mock_print:
            chmod.run(self.emulator, ['755', '/file1.txt'])
            mock_print.assert_called_with("Changed mode of /file1.txt to 755")
        self.assertEqual(self.emulator.fs['/file1.txt'].mode, 0o755)

    def test_chmod_file_not_found(self):
        with patch('builtins.print') as mock_print:
            chmod.run(self.emulator, ['755', '/nonexistent.txt'])
            mock_print.assert_called_with("File not found: /nonexistent.txt")

    def test_chmod_invalid_args(self):
        with patch('builtins.print') as mock_print:
            chmod.run(self.emulator, ['755'])
            mock_print.assert_called_with("Usage: chmod <mode> <file>")

class TestDate(TestEmulator):
    def test_date_output(self):
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 17, 12, 0, 0)
            result = date.run(self.emulator, [])
            self.assertEqual(result, "2023-05-17 12:00:00")

    def test_date_no_args(self):
        result = date.run(self.emulator, [])
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_date_ignore_args(self):
        result1 = date.run(self.emulator, [])
        result2 = date.run(self.emulator, ['ignored', 'args'])
        self.assertEqual(result1, result2)

class TestTail(TestEmulator):
    @patch('tarfile.open')
    def test_tail_success(self, mock_tarfile):
        mock_tarfile.return_value.__enter__.return_value.extractfile.return_value.read.return_value = b"line1\nline2\nline3\nline4\nline5\nline6\nline7\nline8\nline9\nline10\nline11\n"
        result = tail.run(self.emulator, ['/file1.txt'])
        expected = "line2\nline3\nline4\nline5\nline6\nline7\nline8\nline9\nline10\nline11"
        self.assertEqual(result, expected)

    def test_tail_file_not_found(self):
        with patch('builtins.print') as mock_print:
            tail.run(self.emulator, ['/nonexistent.txt'])
            mock_print.assert_called_with("File not found: /nonexistent.txt")

    def test_tail_invalid_args(self):
        with patch('builtins.print') as mock_print:
            tail.run(self.emulator, [])
            mock_print.assert_called_with("Usage: tail <file>")

class TestLs(TestEmulator):
    def test_ls_root(self):
        result = ls.run(self.emulator, [])
        self.assertEqual(result, '/ /file1.txt /file2.txt /dir1/')

    def test_ls_specific_directory(self):
        result = ls.run(self.emulator, ['/dir1'])
        self.assertEqual(result, '/dir1/ /dir1/file3.txt')

    def test_ls_nonexistent_directory(self):
        result = ls.run(self.emulator, ['/nonexistent'])
        self.assertEqual(result, '')

class TestCd(TestEmulator):
    def test_cd_to_existing_directory(self):
        result = cd.run(self.emulator, ['/dir1'])
        self.assertEqual(result, '/dir1')

    def test_cd_to_nonexistent_directory(self):
        with patch('builtins.print') as mock_print:
            result = cd.run(self.emulator, ['/nonexistent'])
            mock_print.assert_called_with("Directory not found: /nonexistent")
        self.assertEqual(result, '/')

    def test_cd_no_args(self):
        result = cd.run(self.emulator, [])
        self.assertEqual(result, '/')

class TestExit(TestEmulator):
    def test_exit_called(self):
        with self.assertRaises(SystemExit) as cm:
            exit.run(self.emulator, [])
        self.assertEqual(cm.exception.code, 0)

    def test_exit_print_message(self):
        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit):
                exit.run(self.emulator, [])
            mock_print.assert_called_with("Exiting emulator...")

    def test_exit_ignore_args(self):
        with self.assertRaises(SystemExit) as cm:
            exit.run(self.emulator, ['ignored', 'args'])
        self.assertEqual(cm.exception.code, 0)

if __name__ == '__main__':
    unittest.main()
from emulator import Emulator
import unittest
import os
import tarfile
import datetime

class TestEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_tar = 'test_fs.tar'
        cls.emulator = Emulator('config.xml')
        cls.emulator.fs_path = cls.test_tar
        cls.emulator.load_virtual_fs()

    @classmethod
    def tearDownClass(cls):
        # Удаление тестового tar-архива, если он существует
        if os.path.exists(cls.test_tar):
            os.remove(cls.test_tar)
        # Удаление временной директории после тестов
        virtual_fs_dir = '/tmp/virtual_fs'
        if os.path.exists(virtual_fs_dir):
            for file in os.listdir(virtual_fs_dir):
                os.remove(os.path.join(virtual_fs_dir, file))
            os.rmdir(virtual_fs_dir)

    def test_ls(self):
        expected_files = ['file1.txt', 'file2.txt']
        result = self.emulator.ls()
        self.assertTrue(set(expected_files).issubset(set(result)))

    def test_cd_valid(self):
        self.emulator.cd('test_fs')
        self.assertEqual(self.emulator.current_dir, os.path.join(self.emulator.virtual_fs, 'test_fs'))

    def test_cd_invalid(self):
        result = self.emulator.cd('invalid_dir')
        self.assertEqual(result, "Directory not found.")

    def test_exit(self):
        result = self.emulator.exit()
        self.assertFalse(result)

    def test_chmod(self):
        result = self.emulator.chmod('755', 'file1.txt')
        self.assertEqual(result, "Changed mode of file1.txt to 755")

    def test_date(self):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = self.emulator.date()
        self.assertEqual(result, current_date)

    def test_tail_valid(self):
        result = self.emulator.tail('file1.txt', 1)
        self.assertEqual(result.strip(), 'This is file 1.')

    def test_tail_invalid(self):
        result = self.emulator.tail('invalid_file.txt', 1)
        self.assertEqual(result, "File not found.")

    def test_tail_no_lines(self):
        result = self.emulator.tail('file1.txt', 0)
        self.assertEqual(result, '')

    def test_create_test_tar(self):
        # Убедимся, что тестовый tar-файл создан
        self.assertTrue(os.path.exists(self.test_tar))

    def test_load_virtual_fs(self):
        # Проверим, что виртуальная файловая система загружена
        self.assertTrue(os.path.exists('/tmp/virtual_fs'))
        self.assertTrue('file1.txt' in os.listdir('/tmp/virtual_fs'))
        self.assertTrue('file2.txt' in os.listdir('/tmp/virtual_fs'))

if __name__ == '__main__':
    unittest.main()

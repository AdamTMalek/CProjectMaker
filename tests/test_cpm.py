import os
import shutil
import unittest
import linecache
import tests.loader as loader

cpm = loader.load("cpm")


class TestMain(unittest.TestCase):
    """
    Test the cpm module
    """

    def test_invalid_name(self):
        """
        We expect the method to only accept alphabetic characters.
        Test with some numbers, special characters to check if the function accepts the input
        """
        invalid_names = {"hello world", "!project", "\"project\""}
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(cpm.valid_name(name))

    def test_valid_name(self):
        """
        Test if name validator accepts valid name
        """
        valid_names = {"helloworld", "project1", "12project", "3301", "1project1"}
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(cpm.valid_name(name))

    @staticmethod
    def create_project(project_name):
        """
        Create project with the given name
        """
        args = ["project", project_name]
        cpm.main(args)

    def test_create_project(self):
        """
        Test if a project is created
        """
        project_name = "foo"
        self.create_project(project_name)

        with self.subTest(msg="Main directory"):
            self.assertTrue(os.path.exists(project_name))
        with self.subTest(msg='build directory'):
            self.assertTrue(os.path.exists(os.path.join(project_name, 'build')))
        with self.subTest(msg='src directory'):
            self.assertTrue(os.path.exists(os.path.join(project_name, 'src')))
        with self.subTest(msg='main.c'):
            self.assertTrue(os.path.exists(os.path.join(project_name, 'src/main.c')))
        with self.subTest(msg='makefile'):
            self.assertTrue(os.path.exists(os.path.join(project_name, 'makefile')))

        shutil.rmtree(project_name)

    def test_rename_project(self):
        """
        Test if renaming project works
        """
        project_name = "foo"
        self.create_project(project_name)

        new_project_name = "bar"
        args = ["project", "-r", project_name, new_project_name]
        cpm.main(args)

        with self.subTest(msg="Main directory"):
            self.assertTrue(os.path.exists(new_project_name))
        with self.subTest(msg="makefile"):
            template_line = linecache.getline('../templates/makefile.txt', 27)
            project_line = linecache.getline(new_project_name + '/makefile', 27)
            template_line = template_line.replace('[PROJECT_NAME]', new_project_name)
            self.assertTrue(template_line == project_line)

        shutil.rmtree(new_project_name)

    def test_create_module_no_dir(self):
        """
        Test if source and header files will be created
        """
        name = "foo"
        args = ["module", "foo"]
        cpm.main(args)

        source_name = name + '.c'
        header_name = name + '.h'

        with self.subTest(msg=source_name):
            self.assertTrue(os.path.exists(source_name))
        with self.subTest(msg="Header included"):
            expected_line = '#include "{}"'.format(header_name)
            line = linecache.getline(source_name, 1).strip("\n")
            self.assertEqual(line, expected_line)
        with self.subTest(msg=header_name):
            self.assertTrue(os.path.exists(header_name))

        os.remove(source_name)
        os.remove(header_name)

    @staticmethod
    def create_module_dir(name):
        """
        Create module with a directory
        """
        args = ["module", "-d", name]
        cpm.main(args)

    def test_create_module_dir(self):
        """
        Test if a module directory will be created with source and header files in it
        """
        name = "foo"
        self.create_module_dir(name)

        source_rel_path = "{0}/{0}.c".format(name)
        header_rel_path = "{0}/{0}.h".format(name)

        with self.subTest(msg="Directory"):
            self.assertTrue(os.path.exists(name))
        with self.subTest(msg=source_rel_path):
            self.assertTrue(os.path.exists(source_rel_path))
        with self.subTest(msg=header_rel_path):
            self.assertTrue(os.path.exists(header_rel_path))

        shutil.rmtree(name)

    def test_rename_module(self):
        """
        Test if renaming module works
        """
        name = "foo"
        self.create_module_dir(name)

        new_name = "bar"
        args = ["module", "-r", name, new_name]
        cpm.main(args)

        source_rel_path = "{0}/{0}.c".format(new_name)
        header_rel_path = "{0}/{0}.h".format(new_name)

        with self.subTest(msg="Directory"):
            self.assertTrue(os.path.exists(new_name))  # Check if the directory was renamed
        with self.subTest(msg=source_rel_path):
            self.assertTrue(os.path.exists(source_rel_path))  # Check if the source file was renamed
        with self.subTest(msg=header_rel_path):
            self.assertTrue(os.path.exists(header_rel_path))  # Header file

        shutil.rmtree(new_name)

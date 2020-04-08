""" Unit tests for all the methods in HW09 """
import unittest
from Student_Repository_MeghanaBhat_Manikal import  Student, Instructor, University


class StudentTest(unittest.TestCase):
    """ Unit tests for all the methods in Student """

    def test_add_course(self)-> None:
        st = Student('10446083', 'Meghana', 'Computer_Science')
        st.add_grade('SSW-810-A', 'A')
        st.add_grade('SSW-810-A', 'A-')
        st.add_grade('SSW-812-A', 'A')

        self.assertEqual(len(st.courses_grades), 2)
        self.assertEqual(st.courses_grades['SSW-810-A'], 'A-')


    def test_get_student_summary(self) -> None:
        """ to test get_student_summary method"""
        
        st = Student('10446083', 'Meghana', 'Computer_Science')
        st.add_grade('SSW-810-A', 'A')
        st.add_grade('SSW-810-A', 'A-')
        st.add_grade('SSW-812-A', 'A')

        st_tuple: Tuple = st.get_student_summary()
        print(st_tuple)

        self.assertEqual(st_tuple[0],'10446083')
    
class UniversityTest(unittest.TestCase):
    """ Unit tests for all the methods in University """


    def test_check_validity(self)-> None:
        """ unittest to test all the functionalities of check_validity"""

        uni = University()

        with self.assertRaises(FileNotFoundError):_= uni.check_validity('./Dummy')
        with self.assertRaises(NotADirectoryError):_= uni.check_validity('./Student_Repository_MeghanaBhat_Manikal.py')

    def test_populate_instructor(self)-> None:
        """ unittest for populate_instructor() """

        uni = University() 
        # chdir('./Stevens') # Local Directory for testing purposes
        uni.populate_instructor('./Stevens')

        self.assertEqual(len(uni.instructors), 6)
        self.assertEqual(uni.instructors.__contains__('98763'), True)
    
    def test_populate_students(self)-> None:
        """unittest for populate_students()"""

        uni = University() 
        # chdir('./Stevens') # Local Directory for testing purposes
        uni.populate_students('./Stevens')

        self.assertEqual(len(uni.students), 10)
        self.assertEqual(uni.instructors.__contains__('98763'), False)

    def file_exception(self,directory:str, path: str)->None:
        """ Helper function to test FileNotFoundError"""
    
        uni = University()
        for cwid, name, major in uni.file_reader(directory, path, 3, sep='\t', header=False):   
            print(tuple([cwid, name, major]))
    
    def value_error_function(self, directory:str, path: str)->None:
        """ Helper function to test ValueError"""

        uni = University()
        for cwid, name, major in uni.file_reader(directory, path, 2, sep='\t', header=False):   
            print(tuple([cwid, name, major]))

    def test_file_reader(self)-> None:
        """ testing file_reader method """ 
        
        lst: list = []

        uni = University()
        for cwid, name, major in uni.file_reader("Stevens","students.txt", 3, sep='\t', header=False):   
            lst.append(tuple([cwid, name, major]))

        self.assertEqual(10, len(lst))
        self.assertEqual('10103', lst[0][0])
        self.assertEqual('SFEN', lst[2][2])

          
        with self.assertRaises(FileNotFoundError):_= self.file_exception("dummyDirectory","dummy.txt")
        with self.assertRaises(ValueError):_= self.value_error_function("Stevens","students.txt")

    def test_populate_grades(self)-> None:
        """ unittest for populate_grades() """

        uni = University()        
        uni.populate_students('./Stevens')
        uni.populate_instructor('./Stevens')
        uni.populate_grades('./Stevens')
        print("Hello")
        self.assertEqual(len(uni.students['10103'].courses_grades), 4)
        self.assertEqual(uni.students['10103'].courses_grades['CS 501'], 'B')
        self.assertEqual(len(uni.instructors['98760'].courses_scount), 4)
        self.assertEqual(uni.instructors['98760'].courses_scount['SYS 611'], 2)
        uni.pretty_print_students()
        uni.pretty_print_instructor()
        
    
    def test_valid_grade(self) -> None:
        """ unittest for valid_grade() """

        uni = University()
        uni.populate_students('./Stevens')
        uni.populate_instructor('./Stevens')
        self.assertEqual(uni.valid_grade('10103','98765'), True)
        with self.assertRaises(ValueError):_= uni.valid_grade('1010','98765')
        with self.assertRaises(ValueError):_= uni.valid_grade('10103','9876')



class InstructorTest(unittest.TestCase):
    """ Unit tests for all the methods in Instructor """


    def test_add_course(self)-> None:
        """ To test add_course methos"""
        inst = Instructor('10239444', 'Prof.Megh', 'SSW')
        inst.add_course('Python')
        inst.add_course('Agile')
        inst.add_course('Agile')
        self.assertEqual(inst.courses_scount['Agile'], 2)
        self.assertEqual(inst.courses_scount['Python'], 1)
        self.assertEqual(inst.courses_scount.__contains__('Key'), False )

    def test_get_intstructor_summary(self) -> None:
        """ to test get_intsructor_summary method"""
        inst = Instructor('10239444', 'Prof.Megh', 'SSW')
        inst.add_course('Python')
        inst.add_course('Agile')
        inst.add_course('Agile')

        inst_tuple: Tuple = inst.get_instructor_summary('Python')
        

        self.assertEqual(inst_tuple[0],'10239444')
        
if __name__ == "__main__":
    unittest.main(exit =False, verbosity=2)
""" Unit tests for all the methods in HW09 """
import unittest
from Student_Repository_MeghanaBhat_Manikal import  Student, Instructor, University, Major


class StudentTest(unittest.TestCase):
    """ Unit tests for all the methods in Student """

    def test_add_grade(self)-> None:
        """ to test add_grades method"""
        st = Student('10446083', 'Meghana', 'Computer_Science')
        st.add_grade('SSW-810-A', 'A')
        st.add_grade('SSW-810-C', 'A-')
        st.add_grade('SSW-812-B', 'A')
        st.add_grade('SSW-812-A', 'D')

        self.assertEqual(len(st.courses_grades), 4)
        self.assertEqual(len(st.passed_courses), 3)
        self.assertEqual(st.courses_grades['SSW-810-C'], 'A-')


    def test_get_student_summary(self) -> None:
        """ to test get_student_summary method"""
        
        st = Student('10446083', 'Meghana', 'Computer_Science')
        st.add_grade('SSW-810-A', 'A')
        st.add_grade('SSW-810-A', 'A-')
        st.add_grade('SSW-812-A', 'A')

        st_tuple: Tuple = st.get_student_summary()
        print(st_tuple)

        self.assertEqual(st_tuple[0],'10446083')

    def test_add_remaining(self)-> None:
        """ to test add_remaining method"""
        
        mj = Major('SFEN', 'R' , 'SSW-810')
        mj.add_course('R', 'Python')
        mj.add_course('E', 'Agile')
        mj.add_course('R', 'OS')

        st = Student('10446083', 'Meghana', 'SFEN')
        st.add_remaining(mj)
        self.assertEqual(len(st.remaining_ec), 1)
        self.assertEqual(len(st.remaining_rc), 3)
    
    def test_calc_gpa(self)->None:
        """ to test calc_gpa method """
        st = Student('10446083', 'Meghana', 'Computer_Science')
        st.add_grade('SSW-810-A', 'A')
        st.add_grade('SSW-810-C', 'A-')
        st.add_grade('SSW-812-B', 'A')
        st.add_grade('SSW-812-A', 'D')
        st_tuple: Tuple = st.get_student_summary()        
        st.calc_gpa()          
        self.assertEqual(round(st.gpa,2),3.92)



class MajorTest(unittest.TestCase):
    def test_get_major_summary(self) -> None:
        """ to test get_student_summary method"""
        
        major = Major('SFEN', 'R', 'SSW 810')
        major.add_course('R', 'SSW 810')
        
        major_tuple: Tuple = major.get_major_summary('SFEN')
        print(major_tuple)

        self.assertEqual(major_tuple[0],'SFEN')

    def test_add_course(self) -> None:
        """ to test add_course method of Major class """
        major = Major('SFEN', 'R', 'SSW 810')
        major.add_course('R', 'SSW 811')

        self.assertEqual(len(major.rcourses), 2)

    def test_populate_major(self)-> None:
        """ unittest for populate_major() """

        uni = University() 
        uni.populate_major('./Stevens')

        self.assertEqual(len(uni.majors), 2)
        self.assertEqual(uni.majors.__contains__('SFEN'), True)
    
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

        self.assertEqual(len(uni.instructors), 3)
        self.assertEqual(uni.instructors.__contains__('98763'), True)
    
    def test_populate_students(self)-> None:
        """unittest for populate_students()"""

        uni = University() 
        # chdir('./Stevens') # Local Directory for testing purposes
        uni.populate_students('./Stevens')

        self.assertEqual(len(uni.students), 4)
        self.assertEqual(uni.instructors.__contains__('98763'), False)

    def file_exception(self,directory:str, path: str)->None:
        """ Helper function to test FileNotFoundError"""
    
        uni = University()
        for cwid, name, major in uni.file_reader(directory, path, 3, sep='\t', header=True):   
            print(tuple([cwid, name, major]))
    
    def value_error_function(self, directory:str, path: str)->None:
        """ Helper function to test ValueError"""

        uni = University()
        for cwid, name, major in uni.file_reader(directory, path, 2, sep='\t', header=True):   
            print(tuple([cwid, name, major]))

    def test_file_reader(self)-> None:
        """ testing file_reader method """ 
        
        lst: list = []

        uni = University()
        for cwid, name, major in uni.file_reader("Stevens","students.txt", 3, sep='\t', header=True):   
            lst.append(tuple([cwid, name, major]))

        self.assertEqual(4, len(lst))
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
        uni.populate_major('./Stevens')
        
        self.assertEqual(len(uni.students['10103'].courses_grades), 2)
        self.assertEqual(uni.students['10103'].courses_grades['CS 501'], 'B')
        self.assertEqual(len(uni.instructors['98764'].courses_scount), 1)
        self.assertEqual(uni.instructors['98764'].courses_scount['SYS 611'], 0)
        uni.pretty_print_major()
        uni.pretty_print_students()
        uni.pretty_print_instructor()
        uni.pretty_print_student_grade()
        
    
    def test_valid_grade(self) -> None:
        """ unittest for valid_grade() """

        uni = University()
        uni.populate_students('./Stevens')
        uni.populate_instructor('./Stevens')
        
        self.assertEqual(uni.valid_grade('10103','98764'), True)
        with self.assertRaises(ValueError):_= uni.valid_grade('1010','98765')
        with self.assertRaises(ValueError):_= uni.valid_grade('10103','9876')

    def test_student_grades_table_db(self) -> None:
        """ unit test for student_grades_table_db()"""


        uni = University()
        sg_list: List = []
        for sg in  uni.student_grades_table_db("./810_student.db"):
            sg_list.append(sg)
        print(sg_list[1])
        self.assertEqual(len(sg_list),9)
        self.assertEqual(sg_list[0][1], '10115')
        self.assertEqual(sg_list[8][1], '10183')
       

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
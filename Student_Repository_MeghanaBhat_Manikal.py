"""  This program creates repositories for different sets of data files"""

from typing import List, Dict, Tuple, Optional
from os import listdir
from prettytable import PrettyTable
from collections import defaultdict
import os

class Student:
    """ Student class is used to store student entity object"""

    # cwid: str
    # name: str
    # major: str
    # courses_grades: Dict[str, str]

    def __init__(self,cwid: str, name: str, major: str)-> None:
        """ initializing the Student"""

        self.cwid:str = cwid
        self.name: str = name
        self.major: str = major
        self.courses_grades:Dict[str, str]  = {}

    def add_grade(self, course: str, grade: str) -> None:
        """ adding course and grades in a dict of a particular student"""

        self.courses_grades[course] = grade
    def get_student_summary(self)-> Tuple:
        """ student summary print related method"""

        return [self.cwid, self.name, sorted( self.courses_grades.keys() ) ]

class Instructor:
    """ Instructor class is used to store instructor entity object """

    # name: str
    # cwid: str
    # dept: str
    # courses_scount: Dict[str, int]
    
    def __init__(self,cwid: str, name: str, dept: str)-> None:
        """ Initializing the Instructor"""

        self.cwid: str = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses_scount: defaultdict[str,int] = defaultdict(int) 

    def add_course(self, course: str)-> None:
        """ Adding and updating the course and the number of students who have taken the course"""
        
        self.courses_scount[course] += 1 
    
    def get_instructor_summary(self,course: Optional[str] = None)-> Tuple:
        """ instructor summary print related method"""
        
        if course == None:
           return [self.cwid, self.name, self.dept, '', '' ]
        else:
            return [self.cwid, self.name, self.dept, course, self.courses_scount[course] ]
    
            
class University:
    """ University class to university entity object and has multiple methods to populate relevant data"""

    students: Dict[str, Student]
    instructors: Dict[str, Instructor]

    def __init__(self, directory: Optional[str]=None) -> None:
        """ Initializing the University"""

        self.students = {}
        self.instructors = {}
        if directory != None:
            self.check_validity(directory)
            self.populate_university(directory)
            self.print_university_details()

    def print_university_details(self) -> None:
        """ To print pretty table"""

        self.pretty_print_students()
        self.pretty_print_instructor()

    def populate_university(self, directory: str) -> None:
        """ to populate students and instructor entities"""

        self.populate_instructor(directory)
        self.populate_students(directory)
        self.populate_grades(directory)

    def check_validity(self,directory:str)-> None:
        """ Validation for the directory"""

        try:
            files: list = listdir(directory)
        except FileNotFoundError:
            raise FileNotFoundError("Directory not found")
        except NotADirectoryError:
            raise NotADirectoryError("given path is not a valid directory")

        if len(files) < 3:
            raise ValueError("Number of file in the director is not equal to 3")

        # print(files)

        if not 'students.txt' in files:
            raise FileNotFoundError("students.txt file not fpund of the expected ")
        
        if not 'grades.txt' in files:
            raise FileNotFoundError("grades.txt file not fpund of the expected ")
        if not 'instructors.txt' in files:
            raise FileNotFoundError("instructors.txt file not fpund of the expected ")
    
    def populate_instructor(self, directory: str) -> None:
        """ populates the instructor dict"""

        # for cwid, name, dept in self.file_reader(directory + "/instructors.txt", 3, sep='\t', header=False):
        for cwid, name, dept in self.file_reader(directory ,"instructors.txt", 3, sep='\t', header=False):
            instructor = Instructor(cwid, name, dept)
            self.instructors[cwid] = instructor

    def populate_students(self,directory) -> None:
        """ populates the student dict"""
        for cwid, name, major in self.file_reader(directory , "students.txt", 3, sep='\t', header=False):
            student = Student(cwid, name, major)
            self.students[cwid] = student
    
    def populate_grades(self,directory) -> None:
        """ populates the gardes dict """
        for s_cwid, course, grade, i_cwid in self.file_reader(directory, "grades.txt", 4, sep='\t', header=False):
            if self.valid_grade(s_cwid, i_cwid):
                self.students[s_cwid].add_grade(course, grade)
                self.instructors[i_cwid].add_course(course)

    def valid_grade(self,s_cwid: str, i_cwid: str ) -> bool:
        """ Checks if the student and instructor cwid is valid """
        if not self.students.__contains__(s_cwid):
            raise ValueError(f"Student with {s_cwid} is not present")
        if not self.instructors.__contains__(i_cwid):
            raise ValueError(f"Instructir with {i_cwid} is not present")      
        return True 

    def file_reader(self, directory:str, file: str,fields: int,sep: str,header: bool)-> Tuple:

        """ reads field-separated text files and yield a tuple with all 
        of the values from a single line in the file on each call to next() """
        path:str = os.path.join(directory, file)
        line_count: int = 1
        if type(path) != str:
            raise TypeError("Please enter a valid path")

        file_name: str = path

        try:
            fp: IO = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"File {path} not Found")
        else:
            with fp:
                for line in fp:
                    # line = line.strip()
                    line = line.replace('\n','')
                    tup = line.split(sep)
                    if fields != len(tup):
                        raise ValueError(f"Number of fileds  in the line {line_count} in the {path} does not match. \n Expected Value: {fields} \n Actual Value: {len(tup)} ")
                    else:
                        if line_count == 1 and header == True:
                            line_count += 1
                            continue
                        else:
                            line_count += 1
                            yield tup
        fp.close()

    def pretty_print_students(self) -> None:
        """ Prints the prettytable of the students summary"""

        print("Student Summary")
        pt: PrettyTable = PrettyTable(field_names=('CWID', 'Name','Completed Courses'))
        for student in self.students.values():
            pt.add_row(student.get_student_summary())
        print(pt)
    

    def pretty_print_instructor(self) -> None:
        """ Prints the prettytable of the instructor summary"""

        print("Instructor Summary")
        pt: PrettyTable = PrettyTable(field_names=('CWID', 'Name', 'Dept', 'Course', 'Students'))
        for instructor in self.instructors.values():
            if len(instructor.courses_scount) == 0:
                pt.add_row(instructor.get_instructor_summary())
            for course in instructor.courses_scount:
                pt.add_row(instructor.get_instructor_summary(course))
        print(pt)

def main() -> None:
    directory_name = './Stevens'
    uni = University(directory_name)
if __name__ == '__main__':
    main()

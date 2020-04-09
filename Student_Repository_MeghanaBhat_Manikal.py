"""  This program creates repositories for different sets of data files"""

from typing import List, Dict, Tuple, Optional, Set
from os import listdir
from prettytable import PrettyTable
from collections import defaultdict
import os

class Major:
    def __init__(self,major: str, r_or_e: str, course: str)-> None:
        """ Initializing the Instructor"""

        self.major: str = major
        self.rcourses: Set[str] =set()
        self.ecourses: Set[str] =set()
        self.add_course(r_or_e,course)

    def add_course(self, r_or_e: str, course: str)-> None:
        """ adding courses into required or elective courses to the respective set """
        if r_or_e == 'R':
            self.rcourses.add(course)
        else:
            self.ecourses.add(course)

    def get_major_summary(self,major: str)-> Tuple[str, Set[str], Set[str]]:
        """ instructor summary print related method"""   
        return [self.major, self.rcourses, self.ecourses]

class Student:
    """ Student class is used to store student entity object"""

    # cwid: str
    # name: str
    # major: str
    # courses_grades: Dict[str, str]
    # passing_grades: Set[str] = set(['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C' ])
    # passing_grades: Set[str] = set(['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C' ])
    

    def __init__(self,cwid: str, name: str, major: str)-> None:
        """ initializing the Student"""

        self.cwid:str = cwid
        self.name: str = name
        self.major: str = major
        self.courses_grades:Dict[str, str]  = {}
        self.passed_courses: Set[str] = set()
        self.remaining_rc: Set[str] = set()
        self.remaining_ec: Set[str] = set()
        self.passing_grades: Set[str] = set(['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C' ])
        self.gpa : float = 0.0
        self.grade_score: Dict[str] = {"A" : 4.0,
                            "A-": 3.75,
                            "B+" :3.25,
                            "B" :3.0,
                            "B-":2.75,
                            "C+":2.25,
                            "C":2.0,
                            "C-": 0,
                            "D+":0,
                            "D": 0,
                            "D-": 0,
                            "F" : 0}
        

        

    def add_grade(self, course: str, grade: str) -> None:
        """ adding course and grades in a dict of a particular student"""        
        self.courses_grades[course] = grade
        if(grade in self.passing_grades):
            self.passed_courses.add(course)
            
    def add_remaining(self, major: Major)->None:
        """ adding remaining courses to a set""" 
        self.remaining_rc = major.rcourses - self.passed_courses
        
        if(len(self.passed_courses.intersection(major.ecourses)) ==0 ):
            self.remaining_ec = major.ecourses - self.passed_courses
    
    def calc_gpa(self) -> None:
        """ calculating gpa """
        sum: float = 0
        for course in self.passed_courses:
            sum = sum + self.grade_score[self.courses_grades[course]]
        if(len(self.passed_courses)>0):
            
            self.gpa  = float(sum) / float(len(self.passed_courses))
        else:
            self.gpa = 0.0
        
      
        
    def get_student_summary(self)-> Tuple[str, str, List[str]]:
        """ student summary print related method"""
        
        return [self.cwid, self.name,self.major,sorted(self.passed_courses),sorted(self.remaining_rc),sorted(self.remaining_ec),round(self.gpa,2)]

    

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
        self.courses_scount: DefaultDict[str,int] = defaultdict(int) 

    def add_course(self, course: str)-> None:
        """ Adding and updating the course and the number of students who have taken the course"""
        
        self.courses_scount[course] += 1 
    
    def get_instructor_summary(self,course: Optional[str] = None)-> Tuple[str, str, List[str]]:
        """ instructor summary print related method"""
        
        return [self.cwid, self.name, self.dept, course, self.courses_scount[course] ]


    
            
class University:
    """ University class to university entity object and has multiple methods to populate relevant data"""

    students: Dict[str, Student]
    instructors: Dict[str, Instructor]
    majors: Dict[str, Major]

    def __init__(self, directory: Optional[str]=None) -> None:
        """ Initializing the University"""

        self.students = {}
        self.instructors = {}
        self.majors = {}
        if directory != None:
            self.check_validity(directory)
            self.populate_university(directory)
            self.print_university_details()

    def print_university_details(self) -> None:
        """ To print pretty table"""

        self.pretty_print_major()
        self.pretty_print_students()
        self.pretty_print_instructor()
        

    def populate_university(self, directory: str) -> None:
        """ to populate students and instructor entities"""

        self.populate_major(directory)
        self.populate_instructor(directory)
        self.populate_students(directory)
        self.populate_grades(directory)
        self.populate_remaining()
        self.calculate_gpa_students()
        
       
    def check_validity(self,directory:str)-> None:
        """ Validation for the directory"""

        try:
            files: list = listdir(directory)
        except FileNotFoundError:
            raise FileNotFoundError("Directory not found")
        except NotADirectoryError:
            raise NotADirectoryError("given path is not a valid directory")

        if len(files) < 4:
            raise ValueError("Number of file in the directory is not equal to 4")

        # print(files)

        if not 'students.txt' in files:
            raise FileNotFoundError("students.txt file not fpund of the expected ")        
        if not 'grades.txt' in files:
            raise FileNotFoundError("grades.txt file not fpund of the expected ")
        if not 'instructors.txt' in files:
            raise FileNotFoundError("instructors.txt file not fpund of the expected ")
        if not 'majors.txt' in files:
            raise FileNotFoundError("majors.txt file not fpund of the expected ")
    def populate_remaining(self) ->None:
        for student in self.students.values():
            student.add_remaining( self.majors[student.major])
    def populate_major(self, directory: str) -> None:
        """ populate the major dict"""
        
        for major, r_or_e, course in self.file_reader(directory ,"majors.txt", 3, sep='\t', header=True):
            if(major in self.majors):
                major_obj = self.majors[major] 
                major_obj.add_course(r_or_e,course)
            else:
                major_obj = Major(major,r_or_e,course)
                self.majors[major] = major_obj

    def populate_instructor(self, directory: str) -> None:
        """ populates the instructor dict"""

        # for cwid, name, dept in self.file_reader(directory + "/instructors.txt", 3, sep='\t', header=False):
        for cwid, name, dept in self.file_reader(directory ,"instructors.txt", 3, sep='|', header=True):
            instructor = Instructor(cwid, name, dept)
            self.instructors[cwid] = instructor

    def populate_students(self,directory) -> None:
        """ populates the student dict"""
        
        for cwid, name, major in self.file_reader(directory , "students.txt", 3, sep=';', header=True):
            student = Student(cwid, name, major)
            self.students[cwid] = student
    
    def populate_grades(self,directory) -> None:
        """ populates the gardes dict """
        
        for s_cwid, course, grade, i_cwid in self.file_reader(directory, "grades.txt", 4, sep='|', header=True):
            if self.valid_grade(s_cwid, i_cwid):
                self.students[s_cwid].add_grade(course, grade)
                self.instructors[i_cwid].add_course(course)
                
    def calculate_gpa_students(self)->None:

        """ calculating gpa """
        for student in self.students.values():
            student.calc_gpa()

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

    def pretty_print_major(self)-> None:
        """ Prints the prettytable of the Major summary"""
        print("Major Summary")

        pt: PrettyTable = PrettyTable(field_names=('Major', 'Required COurses', 'Electives'))
        for major in self.majors.values():
            pt.add_row(major.get_major_summary(major))
        print(pt)


    def pretty_print_students(self) -> None:
        """ Prints the prettytable of the students summary"""

        print("Student Summary")
        pt: PrettyTable = PrettyTable(field_names=('CWID', 'Name','Major','Completed Courses','Remaining Required','Remaining Electives','GPA'))
        for student in self.students.values():
            pt.add_row(student.get_student_summary())
        print(pt)
    

    def pretty_print_instructor(self) -> None:
        """ Prints the prettytable of the instructor summary"""

        print("Instructor Summary")
        pt: PrettyTable = PrettyTable(field_names=('CWID', 'Name', 'Dept', 'Course', 'Students'))
        for instructor in self.instructors.values():
            for course in instructor.courses_scount:
                pt.add_row(instructor.get_instructor_summary(course))
        print(pt)

        
def main() -> None:
    directory_name = './Stevens/'
    try:
        uni = University(directory_name)    
    except ValueError as ve:
        print(ve)
    except FileNotFoundError as fne:
        print(fne)
    except NotADirectoryError as nd:
        print(nd)
    except TypeError as te:
        print(te)
  
if __name__ == '__main__':
    main()

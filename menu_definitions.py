from Menu import Menu
from Option import Option

"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "add(db)"),
    Option("List", "list_objects(db)"),
    Option("Delete", "delete(db)"),
    Option("Boilerplate", "boilerplate(db)"),
    Option("Exit this application", "pass")
])

add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option("Department", "add_department(db)"),
    Option("Course", "add_course(db)"),
    Option("Section", "add_section(db)"),
    Option("Major", "add_major(db)"),
    Option("Student", "add_student(db)"),
    Option("Student Major", "add_student_major(db)"),
    Option("Enrollment", "add_enrollment(db)"),
    Option("Exit", "pass")
])

delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option("Department", "delete_department(db)"),
    Option("Course", "delete_course(db)"),
    Option("Sections", "delete_section(db)"),
    Option("Major", "delete_major(db)"),
    Option("Student", "delete_student(db)"),
    Option("Student's major", "delete_student_major(db)"),
    Option("Enrollment", "delete_enrollment(db)"),
    Option("Exit", "pass")
])

list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option("Department", "list_department(db)"),
    Option("Course", "list_course(db)"),
    Option("Course belongs to Department", "list_departments_courses(db)"),
    Option("Sections", "list_section(db)"),
    Option("ALL - Courses/Section", "list_courses_sections(db)"),
    Option("Section belongs to one course", "list_course_sections(db)"),
    Option("Major", "list_major(db)"),
    Option("Student", "list_student(db)"),
    Option("Major's students", "list_major_students(db)"),
    Option("Student's majors", "list_student_majors(db)"),
    Option("Enrollments for one section", "list_section_students(db)"),
    Option("Student's enrollments", "list_student_sections(db)"),
    Option("Exit", "pass")
])

schedule_menu = Menu('schedule', 'Please indicate the section schedule:', [
    Option("Monday/Wednesday", "MW"),
    Option("Monday/Wednesday/Friday", "MWF"),
    Option("Tuesday/Thursday", "TuTh"),
    Option("Friday only", "F"),
    Option("Saturday only", "S"),
])

semester_menu = Menu('semester', 'Please indicate the section semester:', [
    Option("Fall", "Fall"),
    Option("Spring", "Spring"),
    Option("Winter", "Winter"),
    Option("Summer I", "Summer I"),
    Option("Summer II", "Summer II"),
    Option("Summer III", "Summer III")
])

enrollment_menu = Menu('enrollment', 'Enter enrollment (passfail/lettergrade):', [
    Option("passfail", "passfail"),
    Option("lettergrade", "lettergrade")
])

yes_no_menu = Menu('answer', 'Would you like to list detail information? (1/2 for yes/no) :', [
    Option("yes", "yes"),
    Option("no", "no")
])

grade_menu = Menu('grade', 'Enter the number of minimum satisfactory grade (A/B/C):', [
    Option("A", "A"),
    Option("B", "B"),
    Option("C", "C")
])
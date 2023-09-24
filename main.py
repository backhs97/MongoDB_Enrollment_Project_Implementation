import pymongo
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from menu_definitions import semester_menu
from menu_definitions import schedule_menu
from menu_definitions import enrollment_menu
from menu_definitions import yes_no_menu
from menu_definitions import grade_menu


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(db):
    """
    Add a new department, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    departments collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    dep_validator = {
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "abbreviation", "chair_name", "building", "office", "description"],
                "properties": {
                    "abbreviation": {
                        "bsonType": "string",
                        "maxLength": 6,
                        "description": "Department abbreviation"
                    },
                    "chair_name": {
                        "bsonType": "string",
                        "maxLength": 80,
                        "description": "A faculty member in the department"
                    },
                    "building": {
                        "bsonType": "string",
                        "description": "The building that depart,ent located in CSULB",
                        "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC']
                    },
                    "office": {
                        "bsonType": "int",
                        "minimum": 0,
                        "description": "The office number in integer type"
                    },
                    "description": {
                        "bsonType": "string",
                        "minLength": 10,
                        "maxLength": 80,
                        "description": "'description' must be a string that is > 10 but < 80 and is required"
                    }
                }
            }
        }
    }
    db.command('collMod', 'departments', **dep_validator)
    collection = db["departments"]
    # unique_name: bool = False
    # unique_abbreviation: bool = False
    # unique_chair_name: bool = False
    # unique_building: bool = False
    # unique_office: bool = False
    # unique_description: bool = False
    name = ''
    abbreviation = ''
    chair_name = ''
    building = ''
    office = 0
    description = ''

    name = input("Department name--> ")
    abbreviation = input("Abbreviation--> ")
    chair_name = input("Chair name--> ")
    building = input("Building name--> ")
    office = int(input("Office--> "))
    description = input("Description--> ")

    # while not unique_name or not unique_abbreviation or not unique_chair_name or not unique_building or not unique_office:
    #     name = input("Department name--> ")
    #     abbreviation = input("Abbreviation--> ")
    #     chair_name = input("Chair name--> ")
    #     building = input("Building name--> ")
    #     office = int(input("Office--> "))
    #     description = input("Description--> ")
    #
    #     name_count: int = collection.count_documents({"name": name})
    #     unique_name = name_count == 0
    #
    #     if not unique_name:
    #         print("We already have a department with that name.  Try again.")
    #     if unique_name:
    #         abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
    #         unique_abbreviation = abbreviation_count == 0
    #         if not unique_abbreviation:
    #             print("We already have a department with that department abbreviation.  Try again.")
    #         if unique_abbreviation:
    #             chair_name_count = collection.count_documents({"chair_name": chair_name})
    #             unique_chair_name = chair_name_count == 0
    #             if not unique_chair_name:
    #                 print("We already have a department with that chair name.  Try again.")
    #             if unique_chair_name:
    #                 building_count: int = collection.count_documents({"building": building})
    #                 unique_building = building_count == 0
    #                 if not unique_building:
    #                     print("We already have a department with that same occupied building. Try again.")
    #                 if unique_chair_name:
    #                     location_count = collection.count_documents({"building": building, "office": office})
    #                     unique_location = location_count == 0
    #                 if not unique_location:
    #                     print("The location is occupied by a different department")

    # Build a new department document preparatory to storing it
    department = {
        "name": name,
        "abbreviation": abbreviation,
        "chair_name": chair_name,
        "building": building,
        "office": office,
        "description": description,
    }
    try:
        results = collection.insert_one(department)
        print("Department added successfully")
    except Exception as user:
        print(f"Failed to add the department because violates one or more of your constraints, "
              f"pleas try again. INPUT: {user}")
        add_department(db)


def add_course(db):
    # include schema
    course_validator = {
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["department_abbreviation", "course_number", "name", "description", "units"],
                "properties": {
                    "course_number": {
                        "bsonType": "int",
                        "minimum": 100,
                        "maximum": 699,
                        "description": "Number of the course"
                    },
                    "units": {
                        "bsonType": "int",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Number of units for a given course"
                    }
                }
            }
        }
    }
    # Create a connection to the courses collection from this database
    db.command('collMod', 'courses', **course_validator)
    course_col = db["courses"]
    department_col = db["departments"]
    department = select_department(db)
    course_number: int = -1
    name: str = ''
    description = ''
    units = -1

    name = input("Course full name--> ")
    course_number = int(input("Course number--> "))
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))

    course = {
        "department_abbreviation": department['abbreviation'],
        "name": name,
        "course_number": course_number,
        "description": description,
        "units": units,
    }
    try:
        result = course_col.insert_one(course)

        department_col.update_one(
            {"abbreviation": department['abbreviation']},
            {"$addToSet": {"courses": course['course_number']}}
        )
        print("Course added successfully!")
    except Exception as user:
        print(f"Failed to add department, please check your input: {user}")
        add_course(db)


def add_section(db):
    section_validator = {
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["department_abbreviation", "course_number", "number", "semester", "year", "building",
                             "room", "schedule", "startTime", "instructor"],
                "properties": {
                    "semester": {
                        "bsonType": "string",
                        "maxLength": 20,
                        "description": "Season of an academic year",
                        "enum": ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter']
                    },
                    "year": {
                        "bsonType": "int",
                        "maxLength": 5,
                        "description": "Current year"
                    },
                    "building": {
                        "bsonType": "string",
                        "description": "The building that the department is located at",
                        "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC']
                    },
                    "room": {
                        "bsonType": "int",
                        "minLength": 1,
                        "maxLength": 999,
                        "description": "The room the class resdides in, no ten story buildings on campus"
                    },
                    "schedule": {
                        "bsonType": "string",
                        "maxLength": 10,
                        "description": "Days of the week for a given class",
                        "enum": ['MW', 'TuTh', 'MWF', 'F', 'S']
                    }
                }
            }
        }
    }

    db.command('collMod', 'sections', **section_validator)
    print('Please provide the course that this section belongs to:')
    course = select_course(db)
    collection = db["sections"]

    sectionNumber = 0
    semester = ''
    sectionYear = 0
    building = ''
    room = 0
    schedule = ''
    startTime = datetime(1970, 1, 1, 0, 0, 0)
    instructor = ''

    sectionNumber = int(input('What is the section number -->'))
    semester = semester_menu.menu_prompt()
    sectionYear = int(input('Which year is this section? --> '))
    building = input('Which building is this section? --> ')
    room = int(input(f'Which room of building {building} is this section offered in? --> '))
    schedule = schedule_menu.menu_prompt()
    start_hour = None
    while start_hour not in range(8, 20):
        start_hour = int(input('Start hour (8 to 19) --> '))
    start_minute = None
    while start_minute not in range(60):
        start_minute = int(input('Start minute (0 to 59) --> '))
    startTime = datetime(sectionYear, 1, 1, start_hour, start_minute, 0)
    instructor = input('Instructor full name --> ')

    section = {
        "department_abbreviation": course['department_abbreviation'],
        "course_number": course['course_number'],
        "number": sectionNumber,
        "semester": semester,
        "year": sectionYear,
        "building": building,
        "room": room,
        "schedule": schedule,
        "startTime": startTime,
        "instructor": instructor,
    }
    try:
        results = collection.insert_one(section)
        db["courses"].update_one(
            {"department_abbreviation": course['department_abbreviation']},
            {"$addToSet": {"sections": sectionNumber}}
        )
        print("Section added successfully!")
    except Exception as e:
        print(f"Failed to add section, please check your input: {e}")
        add_section(db)


def add_major(db):

    department_col = db["departments"]
    collection = db["majors"]
    print("Which department offers this major?")
    department = select_department(db)
    unique_name = False
    name = ''
    while not unique_name:
        name = input("Major name--> ")
        name_count = collection.count_documents({"name": name, "department_abbreviation": department['abbreviation']})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department.  Try again.")
    description: str = input('Please give this major a description -->')
    major = {
        "department_abbreviation": department['abbreviation'],
        "name": name,
        "description": description,
    }
    try:
        results = collection.insert_one(major)
        department_col.update_one(
            {"abbreviation": department['abbreviation']},
            {"$addToSet": {"majors": major['name']}}
        )
        print("Major added successfully!")
    except Exception as e:
        print(f"Failed to add major, please check your input: {e}")
        add_major(db)


def add_student(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["students"]
    lastName: str = ''
    firstName: str = ''
    email: str = ''

    lastName = input("Student last name--> ")
    firstName = input("Student first name--> ")
    email = input("Student e-mail address--> ")

    # Build a new students document preparatory to storing it
    student = {
        "last_name": lastName,
        "first_name": firstName,
        "e_mail": email
    }
    try:
        results = collection.insert_one(student)
        print("Student added successfully!")
    except Exception as e:
        print(f"Failed to add a student because {e}")
        add_student(db)


def add_enrollment(db):
    enrollments = db["enrollments"]
    students_col = db["students"]

    print("What student to enroll:")
    student = select_student(db)
    print("Pick section you want this student to enroll in?")
    section = select_section(db)
    enrollment_type = enrollment_menu.menu_prompt()

    existing_enrollment = enrollments.find_one({"section": section["_id"], "student": student["_id"]})
    if existing_enrollment:
        print("Error: Student is already enrolled in this section.")
        return

    enrollment = {
        "department_abbreviation": section['department_abbreviation'],
        "course_number": section['course_number'],
        "student": student['_id'],
        "section": section['_id'],
        "enrollment_type": enrollment_type,
        "application_date": datetime.now()
    }

    if enrollment_type == "lettergrade":
        min_satisfactory = grade_menu.menu_prompt()
        enrollment["min_satisfactory"] = min_satisfactory
    elif enrollment_type != "passfail":
        print("Error: Invalid enrollment type.")
        return

    try:
        result = enrollments.insert_one(enrollment)
        if result.acknowledged:
            students_col.update_one(
                {"_id": student["_id"]},
                {"$addToSet": {"sections": section['number']}}
            )
            print("Enrollment successful.")
    except Exception as e:
        print(f"Error: Enrollment failed.: {e}")
        add_enrollment(db)


def add_student_major(db):
    student = select_student(db)
    major = select_major(db)
    declaration_date = datetime.now()
    try:
        result = db.students.update_one(
            {"_id": student["_id"], "majors.name": {"$ne": major['name']}},
            {"$push": {"majors": {"$each": [{"name": major['name'], "declaration_date": declaration_date}]}}}
        )
        if result.modified_count > 0:
            print("Major added successfully!")
        else:
            print("Student already has this major.")
    except Exception as e:
        print(f"Failed to add major to a student, please check your input: {e}")
        add_student_major(db)


def select_department(db):
    collection = db["departments"]
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Department's abbreviation--> ")
        abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
        found = abbreviation_count == 1
        if not found:
            print("No department found by that abbreviation.  Try again.")
    department = collection.find_one({"abbreviation": abbreviation})
    return department


def select_course(db):
    collection = db["courses"]
    found = False
    while not found:
        # Call function to select department for verification
        department = select_department(db)
        # Prompt user to enter course number
        number = int(input("Course Number--> "))
        number_count = collection.count_documents(
            {"department_abbreviation": department['abbreviation'], "course_number": number})
        found = number_count == 1
        if not found:
            print("No course found by that number. Try again.")
    course = collection.find_one({
        "department_abbreviation": department['abbreviation'],
        "course_number": number
    })
    return course


def select_section(db):
    # Create a connection to the sections collection from this database
    collection = db["sections"]
    course = select_course(db)
    found = False
    while not found:
        number = int(input("Section number--> "))
        semester = semester_menu.menu_prompt()
        section_year = int(input("Section year--> "))
        number_count = collection.count_documents(
            {"department_abbreviation": course['department_abbreviation'], "course_number": course['course_number'],
             "number": number, "semester": semester, "year": section_year})
        found = number_count == 1
        if not found:
            print("No section found by that number.  Try again.")
    found_course = collection.find_one(
        {"department_abbreviation": course['department_abbreviation'], "course_number": course['course_number'],
         "number": number, "semester": semester, "year": section_year})
    return found_course


def select_major(db):
    collection = db["majors"]
    found = False
    name = ''
    while not found:
        name = input("Major's name--> ")
        name_count: int = collection.count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No major found by that name.  Try again.")
    major = collection.find_one({"name": name})
    return major


def select_student(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["students"]
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student's last name--> ")
        firstName = input("Student's first name--> ")
        name_count: int = collection.count_documents({
            "last_name": lastName,
            "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({
        "last_name": lastName,
        "first_name": firstName})
    return found_student

#delete


def delete_department(db):
    """
    Delete a department from the database if its courses array is empty.
    :param db:  The current database connection.
    :return:    None
    """
    department = select_department(db)
    departments = db["departments"]
    courses = db["courses"]
    sections = db["sections"]

    # Check if there are any courses associated with the department
    courses_count = courses.count_documents({"department_abbreviation": department['abbreviation']})
    if courses_count > 0:
        print("Cannot delete department. First delete its courses.")
        return

    # Check if there are any sections associated with the department
    sections_count = sections.count_documents({"department_abbreviation": department['abbreviation']})
    if sections_count > 0:
        print("Cannot delete department. First delete its sections.")
        return

    # Delete the department if it has no associated courses or sections
    deleted = departments.delete_one({"abbreviation": department['abbreviation']})
    print(f"We just deleted: {deleted.deleted_count} department.")


def delete_course(db):
    course = select_course(db)
    courses = db["courses"]
    departments = db["departments"]
    sections_count = db["sections"].count_documents({"course_number": course["course_number"]})
    if sections_count > 0:
        print("Cannot delete course, first delete its sections.")
        return
    result = courses.delete_one({"_id": course["_id"]})
    if result.deleted_count == 1:
        departments.update_one(
            {"abbreviation": course["department_abbreviation"]},
            {"$pull": {"courses": course["course_number"]}}
        )
        print("Course deleted successfully.")
    else:
        print("Error: Course not found.")


def delete_section(db):
    section = select_section(db)
    enrollments_col = db["enrollments"]
    sections_col = db["sections"]
    count = enrollments_col.count_documents({"section": section['_id']})
    if count > 0:
        print("Cannot delete section, first delete its enrollments.")
        return
    deleted = sections_col.delete_one({"_id": section["_id"]})
    if deleted.deleted_count == 1:
        print(f"We just deleted: {deleted.deleted_count} section.")
    else:
        print("Error: Section not deleted.")


def delete_major(db):
    major = select_major(db)
    students = db["students"]
    result = students.count_documents({"majors.name": major["name"]})
    if result == 0:
        db["departments"].update_one(
            {"abbreviation": major["department_abbreviation"]},
            {"$pull": {"majors": major["name"]}}
        )
        db["majors"].delete_one({"_id": major["_id"]})
        print(f"{major['name']} major has been deleted because it was not used by any student.")
    else:
        print('Cannot delete major, first delete its students.')

# def delete_major(db):
#     major = select_major(db)
#     students = db["students"]
#     result = students.count_documents({"majors.name": major["name"]})
#     if result == 0:
#         departments = db["departments"]
#         departments.update_one(
#             {"abbreviation": major["department_abbreviation"]},
#             {"$pull": {"majors": major["name"]}}
#         )
#         majors = db["majors"]
#         deleted = majors.delete_one({"_id": major["_id"]})
#         if deleted.deleted_count == 1:
#             print(f"{major['name']} major has been deleted because it was not used by any student.")
#         else:
#             print("Error: Major not deleted.")
#     else:
#         print('Cannot delete major, first delete its students.')

def delete_student(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """

    student = select_student(db)
    students = db["students"]
    # check if student has any sections
    if "sections" in student and student["sections"]:
        print("Cannot delete student, first delete its enrollments.")
        return
    # check if student has any majors
    if "majors" in student and student["majors"]:
        print("Cannot delete student, first delete its majors.")
        return
    deleted = students.delete_one({"_id": student["_id"]})
    print(f"We just deleted: {deleted.deleted_count} students.")

def delete_student_major(db):
    student = select_student(db)
    major = select_major(db)
    students = db["students"]
    if students is not None and student.get('sections'):
        print("Cannot delete student, first delete its enrollments.")
        return
    students.update_one({"_id": student["_id"]}, {"$pull": {"majors": {"name": major["name"]}}})
    print(f"Successfully deleted major: {major['name']} from student: {student['first_name']} {student['last_name']}.")


def delete_enrollment(db):
    enrollments = db["enrollments"]
    students = db["students"]

    # select the enrollment to delete
    student = select_student(db)
    section = select_section(db)
    enrollment = enrollments.find_one({"student": student["_id"], "section": section["_id"]})
    if not enrollment:
        print("Error: Enrollment not found.")
        return

    # delete the enrollment
    result = enrollments.delete_one({"_id": enrollment["_id"]})
    if result.deleted_count == 1:
        print("Enrollment deleted.")
    else:
        print("Error: Failed to delete enrollment.")

    # update the student's sections array
    students.update_one(
        {"_id": student["_id"]},
        {"$pull": {"sections": section["number"]}}
    )

#list
def list_department(db):
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING)])
    for department in departments:
        pprint(department)


def list_course(db):
    courses = db["courses"].find({}).sort([("number", pymongo.ASCENDING)])
    for course in courses:
        pprint(course)


def list_departments_courses(db):
    departments = db["departments"].aggregate([
        {
            "$lookup": {
                "from": "courses",
                "localField": "abbreviation",
                "foreignField": "department_abbreviation",
                "as": "courses"
            }
        },
        {
            "$sort": {
                "abbreviation": pymongo.ASCENDING
            }
        }
    ])
    for department in departments:
        pprint(department)


def list_section(db):
    sections = db["sections"].find({}).sort([("number", pymongo.ASCENDING)])
    for section in sections:
        pprint(section)


def list_courses_sections(db):
    courses = db["courses"].aggregate([
        {
            "$lookup": {
                "from": "sections",
                "localField": "course_number",
                "foreignField": "course_number",
                "as": "sections"
            }
        },
        {
            "$sort": {
                "number": pymongo.ASCENDING
            }
        }
    ])
    for course in courses:
        pprint(course)


def list_course_sections(db):
    collection = db["sections"]
    course = select_course(db)
    sections = collection.find(
        {"department_abbreviation": course['department_abbreviation'], "course_number": course['course_number']})
    print(f"Sections for {course['department_abbreviation']} {course['course_number']} - {course['name']}:")
    for section in sections:
        print(
            f"Section {section['number']}: {section['semester']} {section['year']}, taught by {section['instructor']}")
    answer = yes_no_menu.menu_prompt()
    if answer == "yes":
        courses = db["courses"].aggregate([
            {
                "$match": {
                    "department_abbreviation": course['department_abbreviation'],
                    "course_number": course['course_number']
                }
            },
            {
                "$lookup": {
                    "from": "sections",
                    "localField": "course_number",
                    "foreignField": "course_number",
                    "as": "sections"
                }
            },
            {
                "$sort": {
                    "number": pymongo.ASCENDING
                }
            }
        ])
        for course in courses:
            pprint(course)


def list_major(db):
    majors = db["majors"].find({}).sort([("name", pymongo.ASCENDING)])
    for major in majors:
        pprint(major)


def list_student(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for student in students:
        pprint(student)


def list_major_students(db):
    major = select_major(db)
    students = db.students.find({"majors": {"$elemMatch": {"name": major['name']}}})
    print(f"Students with major {major['name']}:")
    for student in students:
        print(f"{'_' * 20}")
        print(f"Name: {student['first_name']} {student['last_name']}")


def list_student_majors(db):
    student = select_student(db)
    print(f"Majors for student {student['first_name']} {student['last_name']}:")
    for major in student['majors']:
        print(major)


def list_section_students(db):
    section_id = select_section(db)['_id']
    enrollments = db.enrollments.find({"section": section_id})
    print(f"Students enrolled in that section:")
    for enrollment in enrollments:
        student = db.students.find_one({"_id": enrollment['student']})
        print(f"- {student['first_name']} {student['last_name']}")


def list_student_sections(db):
    student = select_student(db)
    enrollments = db.enrollments.find({"student": student["_id"]})
    print(f"Enrollments for student {student['first_name']} {student['last_name']}:")
    for enrollment in enrollments:
        section = db.sections.find_one({"_id": enrollment['section']})
        print(f"- Section - {section['number']} ({section['course_number']}) ({section['department_abbreviation']})")


from pymongo import MongoClient


def boilerplate(db):
    """
    Add boilerplate data initially to jump start the testing.  Remember that there is no
    checking of this data, so only run this option once from the console, or you will
    get a uniqueness constraint violation from the database.
    :param db: The MongoDB instance that's open.
    :return: None
    """
    department = {'abbreviation': 'CECS', 'name': 'Computer Engineering Computer Science',
                  'chair_name': 'Jane Koo', 'building': 'ECS', 'office': 100, 'description': 'CECS department'}

    db.departments.insert_one(department)

    major1 = {'department_abbreviation': department['abbreviation'], 'name': 'Computer Science', 'description': 'Fun with blinking lights'}
    major2 = {'department_abbreviation': department['abbreviation'], 'name': 'Computer Engineering', 'description': 'Much closer'}
    major3 = {'department_abbreviation': department['abbreviation'], 'name': 'Chemical Engineering', 'description': 'Much closer to the cell'}
    student1 = {'first_name': 'Jake', 'last_name': 'Back', 'e_mail': 'david.brown@gmail.com'}
    student2 = {'first_name': 'Jae', 'last_name': 'Jang', 'e_mail': 'marydenni.brown@gmail.com'}
    student3 = {'first_name': 'Sam', 'last_name': 'Kim', 'e_mail': 'disposable.bandit@gmail.com'}
    course1 = {'department_abbreviation': department['abbreviation'], 'course_number': 323, 'name': "Database Design Fundamentals",
               'description': "Basics of database design", 'units': 3}
    course2 = {'department_abbreviation': department['abbreviation'], 'course_number': 174, 'name': "Intro to Programming",
               'description': "First real programming course", 'units': 3}
    section1 = {'department_abbreviation': course1['department_abbreviation'], "course_number": course1['course_number'], 'number': 1, 'semester': 'Fall', 'year': 2023, 'building': 'ECS', 'room': 416,
                'schedule': 'MW', 'startTime': '13:00:00', 'instructor': 'Brown'}
    section2 = {'department_abbreviation': course2['department_abbreviation'], "course_number": course2['course_number'], 'number': 2, 'semester': 'Spring', 'year': 2023, 'building': 'ECS', 'room': 415,
                'schedule': 'MWF', 'startTime': '13:00:00', 'instructor': 'David'}

    # db.departments.insert_one(department)
    db.majors.insert_many([major1, major2, major3])
    db.students.insert_many([student1, student2, student3])
    db.courses.insert_many([course1, course2])
    db.sections.insert_many([section1, section2])



if __name__ == '__main__':
    """
    password: str = getpass.getpass('Mongo DB password -->')
    username: str = input('Database username [CECS-323-Spring-2023-user] -->') or \
                    "CECS-323-Spring-2023-user"
    project: str = input('Mongo project name [cecs-323-spring-2023] -->') or \
                   "CECS-323-Spring-2023"
    hash_name: str = input('7-character database hash [puxnikb] -->') or "puxnikb"
    """
    cluster = f"mongodb+srv://jaebumjang01:V2ss2931@cluster0.7xrzh4c.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(cluster)
    t = datetime(2023, 6, 29, 12, 30, 0)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    """
    for collection_name in db.list_collection_names():
        db[collection_name].drop()

    print("All collections have been deleted.")
    """
    # student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.
    students = db["students"]
    student_count = students.count_documents({})
    print(f"Students in the collection so far: {student_count}")

    # ************************** Set up the students collection
    students_indexes = students.index_information()
    if 'students_last_and_first_names' in students_indexes.keys():
        print("first and last name index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        students.create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
                              unique=True,
                              name="students_last_and_first_names")
    if 'students_e_mail' in students_indexes.keys():
        print("e-mail address index present.")
    else:
        # Create a UNIQUE index on just the e-mail address
        students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')
    pprint(students.index_information())

    # we insert our first document into this collection.
    departments = db["departments"]
    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")

    # ************************** Set up the departments collection
    departments_indexes = departments.index_information()
    if 'departments_name' in departments_indexes.keys():
        print("departments name index present.")
    else:
        departments.create_index([('name', pymongo.ASCENDING)], unique=True,
                                 name="departments_name")

    if 'departments_abbreviation' in departments_indexes.keys():
        print("abbreviation index present.")
    else:
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name='departments_abbreviation')
    pprint(departments.index_information())

    if 'departments_chair_name' in departments_indexes.keys():
        print("chair name index present.")
    else:
        departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True,
                                 name="departments_chair_name")

    if 'location' in departments_indexes.keys():
        print("location index present.")
    else:
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True,
                                 name="location")
    # new code
    courses = db["courses"]
    course_count = courses.count_documents({})
    print(f"Courses in the collection so far: {course_count}")
    # ************************** Set up the courses collection
    courses_indexes = courses.index_information()
    if 'course_number' in courses_indexes.keys():
        print("course number index present.")
    else:
        courses.create_index([('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING)],
                             unique=True,
                             name="course_number")

    if 'course_name' in students_indexes.keys():
        print("course name index present.")
    else:
        courses.create_index([('department_abbreviation', pymongo.ASCENDING), ('name', pymongo.ASCENDING)],
                             unique=True,
                             name="course_name")

    pprint(courses.index_information())

    # we insert our first document into this collection.
    sections = db["sections"]
    section_count = sections.count_documents({})
    print(f"Sections in the collection so far: {section_count}")
    sections_indexes = sections.index_information()
    if 'sections_year' in sections_indexes.keys():
        print("sections year index present.")
    else:
        sections.create_index(
            [('course_number', pymongo.ASCENDING), ('number', pymongo.ASCENDING), ('semester', pymongo.ASCENDING),
             ('year', pymongo.ASCENDING)], unique=True,
            name="sections_year")

    if 'sections_location' in sections_indexes.keys():
        print("Section location index present.")
    else:
        sections.create_index(
            [('semester', pymongo.ASCENDING), ('year', pymongo.ASCENDING), ('building', pymongo.ASCENDING),
             ('room', pymongo.ASCENDING), ('schedule', pymongo.ASCENDING), ('startTime', pymongo.ASCENDING)],
            unique=True, name='sections_location')

    if 'sections_instructor' in sections_indexes.keys():
        print("Section instructor index present.")
    else:
        sections.create_index(
            [('semester', pymongo.ASCENDING), ('year', pymongo.ASCENDING), ('schedule', pymongo.ASCENDING),
             ('startTime', pymongo.ASCENDING), ('instructor', pymongo.ASCENDING)], unique=True,
            name='sections_instructor')

    pprint(sections.index_information())

    majors = db["majors"]
    major_count = majors.count_documents({})
    print(f"Majors in the collection so far: {major_count}")

    # ************************** Set up the majors collection
    majors_indexes = majors.index_information()
    if 'majors_name' in majors_indexes.keys():
        print("majors name index present.")
    else:
        majors.create_index([('name', pymongo.ASCENDING)], unique=True,
                            name="majors_name")
    pprint(majors.index_information())

    enrollments = db["enrollments"]
    enrollment_count = enrollments.count_documents({})
    print(f"Enrollments in the collection so far: {enrollment_count}")
    # ************************** Set up the enrollments collection
    enrollment_indexes = enrollments.index_information()
    if 'enrollment' in enrollment_indexes.keys():
        print("Course enrollment index present.")
    else:
        enrollments.create_index([('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING), ('student', pymongo.ASCENDING)],
                             unique=True,
                             name="enrollment")

    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)

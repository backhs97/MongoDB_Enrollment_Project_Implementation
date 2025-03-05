# MongoDB Enrollment Project

A Python-based university enrollment management system using MongoDB for data storage and management. This project provides a command-line interface for managing academic departments, courses, sections, students, majors, and enrollments.

## DEMO



## Features

### Data Management Operations
- **Add Operations**
  - Add Departments
  - Add Courses
  - Add Course Sections
  - Add Majors
  - Add Students
  - Assign Majors to Students
  - Create Student Enrollments

- **Delete Operations**
  - Delete Departments
  - Delete Courses
  - Delete Sections
  - Delete Majors
  - Delete Students
  - Remove Student's Major
  - Remove Enrollments

- **List Operations**
  - List Departments
  - List Courses
  - List Courses by Department
  - List Sections
  - List All Courses with Sections
  - List Sections for a Specific Course
  - List Majors
  - List Students
  - List Students by Major
  - List Student's Majors
  - List Enrollments by Section
  - List Student's Enrollments

### Database Structure

The system uses the following MongoDB collections:
- `departments`: Stores department information
- `courses`: Stores course information
- `sections`: Stores course section details
- `students`: Stores student information
- `majors`: Stores major information
- `enrollments`: Stores student enrollment records

### Unique Constraints

The system implements various unique indexes to maintain data integrity:

#### Students Collection
- Combined unique index on last name and first name
- Unique index on email address

#### Departments Collection
- Unique index on department name
- Unique index on department abbreviation
- Unique index on chair name
- Combined unique index on building and office

#### Courses Collection
- Combined unique index on department abbreviation and course number
- Combined unique index on department abbreviation and course name

#### Sections Collection
- Combined unique index on course number, section number, semester, and year
- Combined unique index on semester, year, building, room, schedule, and start time
- Combined unique index on semester, year, schedule, start time, and instructor

#### Majors Collection
- Unique index on major name

#### Enrollments Collection
- Combined unique index on department abbreviation, course number, and student

## Technical Implementation

### Core Components

1. **Menu System**
   - Implemented using `Menu` and `Option` classes
   - Provides hierarchical menu structure for user interaction
   - Supports various operation types through menu options

2. **Data Validation**
   - Enforces unique constraints through MongoDB indexes
   - Implements input validation for all data entry operations
   - Handles duplicate entry attempts gracefully

3. **Error Handling**
   - Comprehensive exception handling for database operations
   - User-friendly error messages
   - Recursive retry functionality for failed operations

### Special Features

1. **Enrollment Types**
   - Supports both pass/fail and letter grade enrollment options
   - Allows specification of minimum satisfactory grade for letter grade enrollments

2. **Section Scheduling**
   - Supports various schedule patterns (MW, MWF, TuTh, F, S)
   - Prevents scheduling conflicts through unique indexes

3. **Relationship Management**
   - Maintains relationships between departments and courses
   - Tracks student majors and enrollments
   - Supports multiple majors per student

## Setup and Configuration

1. **MongoDB Connection**
   ```python
   cluster = "mongodb+srv://[username]:[password]@[cluster-url]/?retryWrites=true&w=majority"
   client = MongoClient(cluster)
   db = client["Demonstration"]
   ```

2. **Required Python Packages**
   - pymongo
   - datetime
   - pprint

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. Use the menu system to:
   - Add new records
   - Delete existing records
   - List various types of information
   - Manage student enrollments

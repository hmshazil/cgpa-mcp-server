from typing import Optional
from server import mcp

GRADE_BANDS = [
    (85, 100, 4.0),
    (80, 84, 3.7),
    (75, 79, 3.3),
    (70, 74, 3.0),
    (65, 69, 2.7),
    (61, 64, 2.3),
    (58, 60, 2.0),
    (55, 57, 1.7),
    (50, 54, 1.0),
    (0, 49, 0.0),
]

COURSES = {
    1: [("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5),
        ("GE-190", "Functional English", 3.0)],
    2: [("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5)],
    3: [("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5)],
    4: [("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5)],
    5: [("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5)],
    6: [("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5)],
    7: [("CC-411", "Final Year Project - I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5)],
    8: [("CC-412", "Final Year Project - II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5)],
}

TOTAL_PROGRAM_CREDIT_HOURS = 134.0


@mcp.tool
def marks_to_grade_points(marks: int) -> float | str:
    """Convert obtained marks (0-100) in one course to a grade point using the
    PUCIT grade band table. Use this before calculating any GPA whenever the
    student gives you marks instead of a grade point directly."""
    if not isinstance(marks, (int, float)):
        return "Error: marks must be a number"
    if marks < 0 or marks > 100:
        return "Error: marks must be between 0 and 100"
    for low, high, gp in GRADE_BANDS:
        if low <= marks <= high:
            return gp
    return "Error: could not map marks to a grade point"


@mcp.tool
def calculate_semester_gpa(grade_points: list[float], credit_hours: list[float]) -> float | str:
    """Calculate one semester's credit-hour-weighted GPA from a list of grade
    points and the matching list of credit hours (same order, same length).
    Use this once you have grade points and credit hours for every course the
    student took in a semester."""
    if not grade_points or not credit_hours:
        return "Error: grade_points and credit_hours cannot be empty"
    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must be the same length"
    total_ch = sum(credit_hours)
    if total_ch <= 0:
        return "Error: total credit hours must be greater than 0"
    weighted_sum = sum(gp * ch for gp, ch in zip(grade_points, credit_hours))
    return round(weighted_sum / total_ch, 3)


@mcp.tool
def calculate_new_cgpa(
    current_cgpa: Optional[float] = None,
    completed_credit_hours: Optional[float] = None,
    semester_gpa: Optional[float] = None,
    semester_credit_hours: Optional[float] = None,
) -> float | str:
    """Project a student's new CGPA after adding one semester's GPA to their
    existing CGPA. Use this when the student already has a CGPA and completed
    credit hours, and wants to know where a given (or hypothetical) semester
    GPA would leave them. Only call this once you actually have all four
    values - do not call it with values missing."""
    missing = [
        name
        for name, val in [
            ("current_cgpa", current_cgpa),
            ("completed_credit_hours", completed_credit_hours),
            ("semester_gpa", semester_gpa),
            ("semester_credit_hours", semester_credit_hours),
        ]
        if val is None
    ]
    if missing:
        return f"Error: missing required value(s): {', '.join(missing)}. Ask the student for these before calling this tool."
    if completed_credit_hours < 0 or semester_credit_hours <= 0:
        return "Error: credit hours must be positive"
    if not (0.0 <= current_cgpa <= 4.0):
        return "Error: current_cgpa must be between 0.0 and 4.0"
    if not (0.0 <= semester_gpa <= 4.0):
        return "Error: semester_gpa must be between 0.0 and 4.0"
    numerator = (current_cgpa * completed_credit_hours) + (semester_gpa * semester_credit_hours)
    denominator = completed_credit_hours + semester_credit_hours
    return round(numerator / denominator, 3)


@mcp.tool
def required_gpa_for_target(
    target_cgpa: Optional[float] = None,
    current_cgpa: Optional[float] = None,
    completed_credit_hours: Optional[float] = None,
    remaining_credit_hours: Optional[float] = None,
) -> float | str:
    """Calculate the GPA a student needs to earn over some remaining credit
    hours to reach a target CGPA by the end of the program. The result can
    come out above 4.0, which means the target is not reachable in that many
    remaining credit hours - it is still the correct number, just report it
    honestly rather than pretending it is achievable. Only call this once you
    actually have all four values - do not call it with values missing."""
    missing = [
        name
        for name, val in [
            ("target_cgpa", target_cgpa),
            ("current_cgpa", current_cgpa),
            ("completed_credit_hours", completed_credit_hours),
            ("remaining_credit_hours", remaining_credit_hours),
        ]
        if val is None
    ]
    if missing:
        return f"Error: missing required value(s): {', '.join(missing)}. Ask the student for these before calling this tool."
    if remaining_credit_hours <= 0:
        return "Error: remaining_credit_hours must be greater than 0"
    if completed_credit_hours < 0:
        return "Error: completed_credit_hours cannot be negative"
    if not (0.0 <= target_cgpa <= 4.0):
        return "Error: target_cgpa must be between 0.0 and 4.0"
    if not (0.0 <= current_cgpa <= 4.0):
        return "Error: current_cgpa must be between 0.0 and 4.0"
    numerator = (target_cgpa * (completed_credit_hours + remaining_credit_hours)) - (
        current_cgpa * completed_credit_hours
    )
    return round(numerator / remaining_credit_hours, 3)


@mcp.tool
def get_semester_courses(semester: int) -> str:
    """Return the list of courses and their credit hours for a given semester
    (1-8) of the PUCIT BS(CS) scheme of studies. Use this whenever you need to
    know what courses a semester contains, or their credit hours, instead of
    guessing."""
    if semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    lines = [f"Semester {semester} courses:"]
    for code, name, ch in COURSES[semester]:
        lines.append(f"- {code}: {name} ({ch} credit hours)")
    return "\n".join(lines)


@mcp.tool
def get_remaining_credit_hours(current_semester: int) -> float | str:
    """Total the graded credit hours remaining from the semester AFTER
    current_semester through semester 8 (inclusive). Use this to find out how
    many credit hours a student still has left in the degree, e.g. to work
    out required_gpa_for_target. current_semester is the semester the student
    just finished or is currently in (1-8)."""
    if current_semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    remaining = 0.0
    for sem in range(current_semester + 1, 9):
        remaining += sum(ch for _, _, ch in COURSES[sem])
    return round(remaining, 1)


@mcp.tool
def save_report(filename: str, content: str) -> str:
    """Save a text report (e.g. a semester GPA result, a projected CGPA, or a
    plan for reaching a target CGPA) to a file. Only call this after you have
    produced something worth keeping, and only when the student has asked you
    to save it."""
    if not filename.strip():
        return "Error: filename cannot be empty"
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        return f"Error: could not save file ({e})"
    return f"Saved report to {filename}"
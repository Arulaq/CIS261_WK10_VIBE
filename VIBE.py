"""Student Grade Calculator.

This program uses Option B: a Student class for each student record.
"""

from dataclasses import dataclass
from pathlib import Path


DATA_FILE = Path("student_grades.txt")


@dataclass
class Student:
	"""Store a student's scores and calculated results."""

	name: str
	student_id: str
	test1: float
	test2: float
	test3: float

	@property
	def average(self) -> float:
		return (self.test1 + self.test2 + self.test3) / 3

	@property
	def grade(self) -> str:
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self) -> str:
		return (
			f"{self.name}|{self.student_id}|{self.test1:.2f}|"
			f"{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"
		)


def load_students(filename: Path = DATA_FILE) -> list[Student]:
	"""Load student records, skipping malformed lines with a clear message."""
	students = []
	if not filename.exists():
		return students

	try:
		with filename.open("r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				values = line.rstrip("\n").split("|")
				if len(values) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					students.append(
						Student(
							values[0],
							values[1],
							float(values[2]),
							float(values[3]),
							float(values[4]),
						)
					)
				except ValueError:
					print(f"Skipping invalid scores on line {line_number}.")
	except OSError as error:
		print(f"Could not load {filename}: {error}")
	return students


def save_students(students: list[Student], filename: Path = DATA_FILE) -> bool:
	"""Save all records in the required pipe-delimited format."""
	try:
		with filename.open("w", encoding="utf-8") as file:
			file.writelines(student.to_file_line() for student in students)
		return True
	except OSError as error:
		print(f"Could not save {filename}: {error}")
		return False


def prompt_score(test_number: int) -> float:
	"""Prompt until a score from 0 through 100 is entered."""
	while True:
		try:
			score = float(input(f"Test {test_number} score (0-100): ").strip())
			if 0 <= score <= 100:
				return score
			print("Please enter a score from 0 through 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students: list[Student]) -> None:
	"""Prompt for and add one student record."""
	print("\nAdd Student")
	name = input("Student name: ").strip()
	while not name or "|" in name:
		print("Name is required and cannot contain '|'.")
		name = input("Student name: ").strip()

	student_id = input("Student ID: ").strip()
	while not student_id or "|" in student_id:
		print("Student ID is required and cannot contain '|'.")
		student_id = input("Student ID: ").strip()

	student = Student(
		name,
		student_id,
		prompt_score(1),
		prompt_score(2),
		prompt_score(3),
	)
	students.append(student)
	print(f"Added {student.name}: average {student.average:.2f}, grade {student.grade}.")


def display_students(students: list[Student]) -> None:
	"""Display all student records in a formatted table."""
	if not students:
		print("\nNo student records found.")
		return

	print("\nStudent Records")
	print("-" * 86)
	print(f"{'Name':<22} {'ID':<14} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>9} {'Grade':>6}")
	print("-" * 86)
	for student in students:
		print(
			f"{student.name:<22.22} {student.student_id:<14.14} "
			f"{student.test1:>8.2f} {student.test2:>8.2f} {student.test3:>8.2f} "
			f"{student.average:>9.2f} {student.grade:>6}"
		)
	print("-" * 86)


def display_statistics(students: list[Student]) -> None:
	"""Display highest, lowest, and overall class averages."""
	if not students:
		print("\nNo student records available for statistics.")
		return

	averages = [student.average for student in students]
	print("\nClass Statistics")
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average:  {min(averages):.2f}")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_students(students: list[Student]) -> None:
	"""Find and display students whose names contain the search text."""
	search_text = input("\nEnter a student name to search: ").strip().lower()
	matches = [student for student in students if search_text in student.name.lower()]
	if matches:
		display_students(matches)
	else:
		print(f"No students found matching '{search_text}'.")


def main() -> None:
	"""Run the Student Grade Calculator menu."""
	students = load_students()
	print("Student Grade Calculator")
	print("Data structure: Option B (Student class)")
	print(f"Loaded {len(students)} student record(s) from {DATA_FILE}.")

	while True:
		print("\nMenu")
		print("1. Add student")
		print("2. Display all students")
		print("3. Display class statistics")
		print("4. Search by name")
		print("5. Save records")
		print("ESC. Save and exit")
		choice = input("Choose an option: ").strip()

		if choice == "1":
			add_student(students)
			save_students(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_students(students)
		elif choice == "5":
			if save_students(students):
				print(f"Saved {len(students)} student record(s).")
		elif choice.upper() == "ESC" or choice == "\x1b":
			if save_students(students):
				print("Records saved. Goodbye!")
			break
		else:
			print("Invalid option. Choose 1-5 or press ESC to exit.")


if __name__ == "__main__":
	main()
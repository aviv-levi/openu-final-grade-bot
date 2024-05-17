from src.base.calculators.openu_calculator import OpenUCalculator
from src.base.models.openu_task_details import OpenUTaskDetails


def test_final_grade_simple_case():
    # arrange
    tasks_details = [
        OpenUTaskDetails(3, 94),
        OpenUTaskDetails(1, 100),
        OpenUTaskDetails(3, 100),
        OpenUTaskDetails(4, 100),
        OpenUTaskDetails(1, 100),
        OpenUTaskDetails(4, 100),
        OpenUTaskDetails(3, 100),
        OpenUTaskDetails(1, 100),
    ]
    exam_grade = 60
    expected_final_grade = 68
    # act
    actual_final_grade = OpenUCalculator.calculate_final_grade(tasks_details, exam_grade)
    # assert
    assert actual_final_grade == expected_final_grade


def test_final_grade_empty_case():
    # arrange
    tasks_details = []
    exam_grade = 60
    expected_final_grade = 60
    # act
    actual_final_grade = OpenUCalculator.calculate_final_grade(tasks_details, exam_grade)
    # assert
    assert actual_final_grade == expected_final_grade

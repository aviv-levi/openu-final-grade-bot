from typing import List

from src.base.models.openu_task_details import OpenUTaskDetails

TOTAL_WEIGHT = 14


class OpenUCalculator:

    @staticmethod
    def calculate_final_grade(tasks_details: List[OpenUTaskDetails], exam_grade):
        sorted_tasks = sorted(
            tasks_details,
            key=lambda item: item.task_grade,
            reverse=True
        )

        tasks_total_weight = 0
        calculation_tasks = []
        for task_details in sorted_tasks:
            if tasks_total_weight < TOTAL_WEIGHT or task_details.task_grade > exam_grade:
                tasks_total_weight += task_details.task_weight
                calculation_tasks.append(task_details)

        exam_weight = 100 - tasks_total_weight
        exam_details = OpenUTaskDetails(exam_weight, exam_grade)
        calculation_tasks.append(exam_details)
        return sum(calculation_task.task_grade * calculation_task.task_weight
                   for calculation_task in calculation_tasks) / 100

    @staticmethod
    def _find_closest_exam_grade(exam_to_final_map, desired_final_grade):
        return min(exam_to_final_map, key=lambda exam_grade: abs(exam_to_final_map[exam_grade] - desired_final_grade))

    @staticmethod
    def calculate_desired_exam_grade(tasks_details: List[OpenUTaskDetails], desire_grade):
        exam_to_final_map = {exam_grade: OpenUCalculator.calculate_final_grade(tasks_details, exam_grade)
                             for exam_grade in range(60, 101)}
        return OpenUCalculator._find_closest_exam_grade(exam_to_final_map, desire_grade)

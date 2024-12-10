import os

from openpyxl import Workbook

from interface.widgets.message import message
from managers.DAO_classes import customer_DAO, project_DAO, tasks_DAO


class report_manager:
    @staticmethod
    def make_report():
        """Створює звіт"""
        report = report_manager.get_info()
        report_manager.create_report(report, "report.xlsx")

    @staticmethod
    def get_info():
        """Повертає дані у вигляді однієї структури"""
        report = []

        projects = project_DAO.get_all_projects()

        for project in projects:

            customer = customer_DAO.get_customer_by_id(project.customer_id)
            tasks = tasks_DAO.get_tasks_by_project_id(project.id)

            report.append(
                {
                    "Project_name": project.name,
                    "Customer": {
                        "Name": customer.name,
                        "Surname": customer.surname,
                        "Phone": customer.phone,
                        "Address": customer.address,
                        "Mail": customer.mail,
                    },
                    "Paid": project.cost,
                    "Cost": project.paid,
                    "Tasks": [
                        {
                            "deadline": task.deadline,
                            "is_done": task.is_done,
                            "is_checked": task.is_checked,
                            "Comment": task.comment,
                        }
                        for task in tasks
                    ],
                }
            )

        return report

    @staticmethod
    def create_report(report, filename):
        """Створює EXCEL файл"""
        wb = Workbook()

        for project in report:
            project_name = project["Project_name"]
            ws = wb.create_sheet(title=project_name)

            customer = project["Customer"]
            ws.append(
                [
                    f"Customer Name: {customer['Name']} {customer['Surname']}",
                    f"Phone: {customer['Phone']}",
                    f"Address: {customer['Address']}",
                    f"Email: {customer['Mail']}",
                ]
            )

            ws.append(
                [
                    f"Paid: {project['Paid']}",
                    f"Cost: {project['Cost']}",
                ]
            )

            ws.append([])

            ws.append(["deadline", "is_done", "is_checked", "Comment"])

            for task in project["Tasks"]:
                task_row = [
                    task["deadline"],
                    task["is_done"],
                    task["is_checked"],
                    task["Comment"],
                ]
                ws.append(task_row)

            column_widths = {
                "A": 36,
                "B": 22,
                "C": 30,
                "D": 46,
            }

            for col, width in column_widths.items():
                ws.column_dimensions[col].width = width

        del wb["Sheet"]

        if not os.path.exists("reports"):
            os.makedirs("reports")
        wb.save("reports/" + filename)

        message.show_message("Звіт сформовано", "Перевірте папку reports")

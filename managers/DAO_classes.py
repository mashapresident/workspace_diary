from datetime import datetime

from database.db import Session as session_factory
from database.tables import (
    customer,
    groups_list,
    project,
    roles_list,
    stuff,
    stuff_group,
    tag,
    task,
    task_stage,
    zoom,
)


class customer_DAO:
    @staticmethod
    def add_customer(
        name: str, surname: str, phone: str, address: str, mail: str, date_of_birth: str
    ):
        try:
            new_customer = customer(
                name,
                surname,
                phone,
                address,
                mail,
                datetime.strptime(date_of_birth, "%Y-%m-%d").date(),
            )
            with session_factory() as session:
                session.add(new_customer)
                session.commit()
        except Exception as e:
            print(f"Failed to add customer: {e}")

    @staticmethod
    def get_customer_by_id(customer_id):
        try:
            with session_factory() as session:
                return session.query(customer).filter_by(id=customer_id).first()
        except Exception as e:
            print(f"Failed to fetch customer by id: {e}")
            return None

    @staticmethod
    def get_all_customers():
        try:
            with session_factory() as session:
                return session.query(customer).all()
        except Exception as e:
            print(f"Failed {e}")
            return None

    @staticmethod
    def get_customer_id_by_fullname(fulname: str):
        ns = fulname.split(" ")
        name = ns[0]
        surname = ns[1]
        try:
            with session_factory() as session:
                return (
                    session.query(customer)
                    .filter_by(name=name, surname=surname)
                    .first()
                    .id
                )
        except Exception as e:
            print(f"Failed to fetch customer by id: {e}")
            return None

    @staticmethod
    def get_customer_by_phone(entered_phone: str):
        try:
            with session_factory() as session:
                return session.query(customer).filter_by(phone=entered_phone).first()
        except Exception:
            return None

    @staticmethod
    def get_customer_by_email(entered_email: str):
        try:
            with session_factory() as session:
                return session.query(customer).filter_by(mail=entered_email).first()
        except Exception:
            return None

    @staticmethod
    def delete_customer(customer_id):
        try:
            with session_factory() as session:
                customer_record = (
                    session.query(customer).filter_by(id=customer_id).first()
                )
                if customer_record:
                    session.delete(customer_record)
                    session.commit()
        except Exception as e:
            print(f"Failed to delete customer: {e}")


class stuff_DAO:
    @staticmethod
    def add_stuff(
        name: str,
        surname: str,
        role: str,
        phone: str,
        address: str,
        mail: str,
        date_of_birth: str,
    ):
        try:
            print(type(date_of_birth))
            new_stuff = stuff(
                name=name,
                surname=surname,
                role=role,
                phone=phone,
                address=address,
                mail=mail,
                date_of_birth=date_of_birth,
            )
            with session_factory() as session:
                session.add(new_stuff)
                session.commit()
        except Exception as e:
            print(f"Failed to add stuff: {e}")

    @staticmethod
    def get_stuff_by_phone(entered_phone: str):
        try:
            with session_factory() as session:
                return session.query(stuff).filter_by(phone=entered_phone).first()
        except Exception:
            return None

    @staticmethod
    def get_stuff_by_email(entered_email: str):
        try:
            with session_factory() as session:
                return session.query(stuff).filter_by(mail=entered_email).first()
        except Exception:
            return None

    @staticmethod
    def get_password_by_mail(stuff_mail: str):
        try:
            with session_factory() as session:
                return session.query(stuff).filter_by(mail=stuff_mail).first().password
        except Exception as e:
            print("1234")
            return None

    @staticmethod
    def get_staff_id_by_fullname(fullname: str):
        list = fullname.split(" ")
        name = list[1]
        surname = list[0]
        """Возвращает идентификатор сотрудника по имени и фамилии."""
        try:
            with session_factory() as session:
                staff = (
                    session.query(stuff).filter_by(name=name, surname=surname).first()
                )
                return staff.id if staff else None
        except Exception as e:
            print(f"Failed to fetch staff ID: {e}")

            return None

    @staticmethod
    def get_stuff_by_id(stuff_id: int):
        try:
            with session_factory() as session:
                return session.query(stuff).filter_by(id=stuff_id).first()
        except Exception as e:
            print(f"Failed to fetch stuff by id: {e}")
            return None

    @staticmethod
    def get_all_stuff():
        try:
            with session_factory() as session:
                return session.query(stuff).all()
        except Exception as e:
            print(f"Failed to fetch all stuff: {e}")
            return []

    @staticmethod
    def get_all_stuff_without_manager():
        try:
            with session_factory() as session:
                return session.query(stuff).filter(stuff.role != "manager").all()
        except:
            return []

    @staticmethod
    def get_stuff_by_mail(mail: str):
        """Retrieve stuff record by email."""
        try:
            with session_factory() as session:
                stuff_record = session.query(stuff).filter_by(mail=mail).first()
                return stuff_record if stuff_record else None
        except Exception as e:
            print(f"Failed to fetch stuff by email: {e}")
            return None

    @staticmethod
    def delete_stuff(stuff_id: int):
        try:
            with session_factory() as session:
                stuff_record = session.query(stuff).filter_by(id=stuff_id).first()
                if stuff_record:
                    session.delete(stuff_record)
                    session.commit()
                else:
                    print("Stuff not found.")
        except Exception as e:
            print(f"Failed to delete stuff: {e}")


class project_DAO:
    @staticmethod
    def get_id_by_name(name: str):
        try:
            with session_factory() as session:
                return session.query(project).filter_by(name=name).first().id
        except Exception as e:
            print(f"Failed to fetch project by customer id: {e}")
            return None


    # @staticmethod
    # def get_projects_by_stuff_id(id: int):
    #     groups_DAO.
    #     try:
    #         with session_factory() as session:
    #             return session.query(project).filter_by(group_id = ).first().id
    #     except Exception as e:
    #         print(f"Failed to fetch project by customer id: {e}")
    #         return None
    
    
    @staticmethod
    def get_name_by_id(project_id: int):
        print(project_id)
        try:
            with session_factory() as session:
                project_instance = (
                    session.query(project).filter_by(id=int(project_id)).first()
                )
                if project_instance:
                    return project_instance.name
                else:
                    print(f"No project found with id: {project_id}")
                    return None
        except Exception as e:
            print(f"Failed to fetch project by id: {e}")
            return None

    @staticmethod
    def add_project(name: str, group_id: int, customer_id: int, cost: int, paid: int):
        try:
            new_project = project(
                name,
                group_id,
                customer_id,
                cost,
                paid,
            )
            with session_factory() as session:
                session.add(new_project)
                session.commit()
        except Exception as e:
            print(f"Failed to add project: {e}")

    @staticmethod
    def get_project_by_customerid(customer_id):
        try:
            with session_factory() as session:
                return session.query(project).filter_by(customer_id=customer_id).all()
        except Exception as e:
            print(f"Failed to fetch project by customer id: {e}")
            return None

    @staticmethod
    def get_all_projects():
        try:
            with session_factory() as session:
                return session.query(project).all()
        except Exception as e:
            return None

    @staticmethod
    def get_all_projects_with_stuff_id(stuff_id: int):
        try:
            with session_factory() as session:
                return session.query(project).filter().all()
        except Exception as e:
            return None


    @staticmethod
    def get_first_project():
        try:
            with session_factory() as session:
                return session.query(project).first()
        except Exception as e:
            return None

    @staticmethod
    def delete_project(project_id):
        try:
            with session_factory() as session:
                customer_record = (
                    session.query(project).filter_by(id=project_id).first()
                )
                if customer_record:
                    session.delete(customer_record)
                    session.commit()
        except Exception as e:
            print(f"Failed to delete project: {e}")


class stuff_group_DAO:
    @staticmethod
    @staticmethod
    def add_stuff_to_group(staff_id: int, group_id: int):
        try:
            st_gr = stuff_group(stuff_id=staff_id, group_id=group_id)
            with session_factory() as session:
                session.add(st_gr)
                session.commit()
        except Exception as e:
            session.rollback()


class groups_DAO:
    @staticmethod
    def add_group(group_name: str):
        """Добавить новую группу в базу данных."""
        try:
            new_group = groups_list(group_name)
            with session_factory() as session:
                session.add(new_group)
                session.commit()
            print(f"Group '{group_name}' added successfully.")
        except Exception as e:
            print(f"Error adding group: {e}")

    @staticmethod
    def get_groups():
        """Получить список всех групп из базы данных."""
        try:
            with session_factory() as session:
                groups = session.query(groups_list).all()
                return groups  # Вернуть список объектов групп
        except Exception as e:
            print(f"Error fetching groups: {e}")
            return []

    @staticmethod
    def get_groups_names():
        """Получить список всех групп из базы данных."""
        try:
            with session_factory() as session:
                groups = session.query(groups_list).all()
                # Возвращаем только имена групп
                return [group.name for group in groups]
        except Exception as e:
            print(f"Error fetching groups: {e}")
            return []

    @staticmethod
    def get_group_id_by_name(name: str):
        try:
            with session_factory() as session:
                group = session.query(groups_list).filter_by(name=name).first()
                if group:
                    return group.id
                else:
                    print(f"Group with name '{name}' not found.")
                    return None
        except Exception as e:
            print(f"Error fetching group ID by name: {e}")
            return None


class tasks_DAO:
    @staticmethod
    def get_tasks_by_project_id(project_id):
        try:
            with session_factory() as session:
                tasks = (
                    session.query(task)
                    .filter_by(project_id=project_id)
                    .order_by(task.deadline)
                    .all()
                )
                return tasks
        except Exception as e:
            print(f"Failed to fetch tasks for project_id {project_id}: {e}")
            return None

    @staticmethod
    def add_task(target_role, project_id, deadline, comment):
        """Додає нове завдання до бази даних."""
        try:
            with session_factory() as session:
                new_task = task(
                    target_role=target_role,
                    project_id=project_id,
                    deadline=deadline,
                    comment=comment,
                )
                session.add(new_task)
                session.commit()
        except Exception as e:
            raise Exception(f"Database error: {e}")

    @staticmethod
    def delete_task(task_id):
        """Видаляє завдання з бази даних за його ID."""
        try:
            with session_factory() as session:
                task_to_delete = session.query(task).filter_by(id=task_id).first()
                if task_to_delete:
                    session.delete(task_to_delete)
                    session.commit()
                else:
                    raise Exception(f"Task with ID {task_id} not found.")
        except Exception as e:
            raise Exception(f"Database error: {e}")

    @staticmethod
    def edit_task(task_id, target_role, project_id, deadline, comment):
        """Оновлює завдання у базі даних."""
        try:
            with session_factory() as session:
                task_to_edit = session.query(task).filter_by(id=task_id).first()
                if task_to_edit:
                    task_to_edit.target_role = target_role
                    task_to_edit.project_id = project_id
                    task_to_edit.deadline = deadline
                    task_to_edit.comment = comment
                    session.commit()
                else:
                    raise Exception(f"Task with ID {task_id} not found.")
        except Exception as e:
            raise Exception(f"Database error: {e}")

    @staticmethod
    def get_all_tasks():
        """Повертає всі завдання з бази даних."""
        try:
            with session_factory() as session:
                return session.query(task).all()
        except Exception as e:
            raise Exception(f"Database error: {e}")

    @staticmethod
    def get_tasks(stage: str, proj: project, target_role: roles_list):
        """
        Повертає завдання для відповідного проекту залежно від ролі.
        """
        if not proj:
            return []
        try:
            print(
                f"Fetching tasks for project_id={proj.id}, stage={stage}, target_role={target_role}"
            )
            with session_factory() as session:
                # Базовий фільтр за проектом
                query = session.query(task).filter_by(project_id=proj.id, stage=stage)
                if target_role.lower() != "manager":
                    query = query.filter_by(role=target_role)
                tasks = query.order_by(task.deadline).all()
                print(f"Found {len(tasks)} tasks")
                return tasks
        except Exception as e:
            print(f"Failed to fetch tasks: {e}")
            return []

    @staticmethod
    def get_all_tasks():
        """Повертає всі завдання з бази даних."""
        try:
            with session_factory() as session:
                return session.query(task).all()
        except Exception as e:
            raise Exception(f"Database error: {e}")

    @staticmethod
    def get_tasks_by_staff_id(staff_id):
        """
        Повертає завдання, пов'язані зі співробітником за його ID.
        """
        try:
            with session_factory() as session:
                # Отримуємо завдання, де Is Done або Is Checked дорівнює staff_id
                tasks = (
                    session.query(task)
                    .filter((task.is_done == staff_id) | (task.is_checked == staff_id))
                    .order_by(task.deadline)
                    .all()
                )
                return tasks
        except Exception as e:
            print(f"Failed to fetch tasks for staff_id {staff_id}: {e}")
            return None

    @staticmethod
    def get_tasks_by_staff_id_with_names(staff_id):
        """
        Повертає завдання, пов'язані зі співробітником за його ID, з іменами в полях 'Is Done' та 'Is Checked'.
        """
        try:
            with session_factory() as session:
                # Отримуємо всі завдання, де Is Done або Is Checked дорівнює staff_id
                tasks = (
                    session.query(task)
                    .filter((task.is_done == staff_id) | (task.is_checked == staff_id))
                    .order_by(task.deadline)
                    .all()
                )

                # Замінюємо staff_id на імена та прізвища
                task_list_with_names = []
                for t in tasks:
                    is_done_name = session.query(stuff).filter_by(id=t.is_done).first()
                    is_checked_name = (
                        session.query(stuff).filter_by(id=t.is_checked).first()
                    )

                    task_list_with_names.append(
                        {
                            "deadline": t.deadline,
                            "is_done": (
                                f"{is_done_name.name} {is_done_name.surname}"
                                if is_done_name
                                else "N/A"
                            ),
                            "is_checked": (
                                f"{is_checked_name.name} {is_checked_name.surname}"
                                if is_checked_name
                                else "N/A"
                            ),
                            "Comment": t.comment,
                        }
                    )
                return task_list_with_names
        except Exception as e:
            print(f"Failed to fetch tasks for staff_id {staff_id}: {e}")
            return None


class roles_DAO:
    @staticmethod
    def get_all_roles():
        """
        Повертає всі ролі з таблиці roles_list.
        """
        try:
            with session_factory() as session:
                roles = session.query(roles_list).all()
                return roles
        except Exception as e:
            print(f"Failed to fetch roles: {e}")
            return None

    @staticmethod
    def get_stuff_roles():
        """
        Повертає всі ролі з таблиці roles_list, за винятком ролі 'manager'.
        """
        try:
            with session_factory() as session:
                roles = (
                    session.query(roles_list).filter(roles_list.role != "manager").all()
                )
                return roles
        except Exception as e:
            print(f"Failed to fetch roles excluding manager: {e}")
            return None


class task_stage_DAO:
    @staticmethod
    def get_stages():
        """Повертає всі доступні стадії завдання."""
        try:
            with session_factory() as session:
                return session.query(task_stage).all()
        except Exception as e:
            raise Exception(f"Database error: {e}")

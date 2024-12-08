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
                datetime.strptime(date_of_birth, "%d-%m-%Y").date(),
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
    def get_customer_by_fullname(entered_name: str, entered_surname: str):
        try:
            with session_factory() as session:
                return (
                    session.query(customer)
                    .filter_by(name=entered_name, surname=entered_surname)
                    .all()
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
                return session.query(customer).filter_by(email=entered_email).first()
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
        password: str,
    ):
        try:
            new_stuff = stuff(
                name=name,
                surname=surname,
                role=role,
                phone=phone,
                address=address,
                mail=mail,
                date_of_birth=datetime.strptime(date_of_birth, "%d-%m-%Y").date(),
                password=password,
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
                return session.query(stuff).filter_by(email=entered_email).first()
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
        name = list[0]
        surname = list[1]
        """Возвращает идентификатор сотрудника по имени и фамилии."""
        try:
            with session_factory() as session:
                staff = session.query(stuff).filter_by(name=name, surname=surname).first()
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
                return session.query(stuff).filter(stuff.role != 'manager').all()
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
            print(f"Failed to fetch project by customer id: {e}")
            return None

        
    @staticmethod
    def get_all_projects():
        try:
            with session_factory() as session:
                return session.query(project).all()
        except Exception as e:
            print(f"Failed to fetch project by customer id: {e}")
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

            

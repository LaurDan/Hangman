import time
class Employer:
    employee_list = list()

    def __init__(self, user, first_name, last_name, age, job, salary, bonus):
        self.__user = user
        self.__first_name = first_name
        self.__last_name = last_name
        self.__age = age
        self.__job = job
        self.__salary = salary
        self.__bonus = bonus

    def add_new_employee(self):
        Employer.employee_list.append(self)

    @staticmethod
    def get_employee_list():
        return Employer.employee_list

    @staticmethod
    def get_employee_by_user(user):
        for employee in Employer.employee_list:
            if employee.get_user() == user:
                return employee
        return False

    @staticmethod
    def update_employee_by_user(user, first_name, last_name, age, job, salary, bonus):
        for employee in Employer.employee_list:
            if employee.get_user() == user:
                employee.__user = user
                employee.__first_name = first_name
                employee.__last_name = last_name
                employee.__age = age
                employee.__job = job
                employee.__salary = salary
                employee.__bonus = bonus
                return True
        return False

    @staticmethod
    def remove_employee_by_user(user):
        for employee in Employer.employee_list:
            if employee.get_user() == user:
                Employer.employee_list.remove(employee)
                return True
        return False

    def total_salary(self):
        total_salary = self.__bonus + self.__salary
        return total_salary

    def get_user(self):
        return self.__user

    def set_user(self, user):
        self.__user = user

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_last_name(self):
        return self.__first_name

    def set_last_name(self, last_name):
        self.__first_name = last_name

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

    def get_job(self):
        return self.__job

    def set_job(self, job):
        self.__age = job

    def get_salary(self):
        return self.__salary

    def set_salary(self, salary):
        self.__salary = salary

    def get_bonus(self):
        return self.__bonus

    def set_bonus(self, bonus):
        self.__bonus = bonus

    def __str__(self):
        time.sleep(1)
        return f"User ID: {self.__user}\n" \
               f"First Name: {self.__first_name}\n" \
               f"Last Name: {self.__last_name}\n" \
               f"Age : {self.__age}\n" \
               f"Job: {self.__job}\n" \
               f"Salary: {self.__salary}\n" \
               f"Bonus : {self.__bonus}\n" \
               f"Total Salary: {self.total_salary()}"

def conditions():

    choice = 1
    employee = Employer("", "", 0, "", 0, 0, 0)

    while 1 <= choice <= 5:
        time.sleep(1)
        print("\n1.Add New Employee\n"
              "2.Get Employee list\n"
              "3.Get Employee By Id\n"
              "4.Update Employee by ID\n"
              "5.Remove Employee by ID\n")
        choice = int(input("Please enter your choice: "))
        print("\n")

        if choice == 1:
            user = int(input("Enter Employee user: "))
            first_name = input("Enter Employee first name: ")
            last_name = input("Enter Employee last name: ")
            age = int(input("Enter Employee age: "))
            job = input("Enter Employee department job: ")
            salary = float(input("Enter Employee salary: "))
            bonus = int(input("Enter Employee bonus: "))
            emp = Employer(user, first_name, last_name, age, job, salary, bonus)
            emp.add_new_employee()

        elif choice == 2:
            for emp in employee.get_employee_list():
                print(emp)

        elif choice == 3:
            user = int(input("Enter Employee user: "))
            emp = employee.get_employee_by_user(user)
            if not emp:
                print(f"\n Sorry but the employee cannot be found by this user: {user}")
            else:
                print(emp)

        elif choice == 4:
            user = int(input("Enter Employee user: "))
            first_name = input("Enter Employee first name: ")
            last_name = input("Enter Employee last name: ")
            age = int(input("Enter Employee age: "))
            job = input("Enter Employee department job: ")
            salary = float(input("Enter Employee salary: "))
            bonus = int(input("Enter Employee bonus: "))
            emp = employee.update_employee_by_user(user, first_name, last_name, age, job, salary, bonus)

            if not emp:
                print("\n Sorry, Update Failed, Employee cant be found by this user: ", user)
            else:
                print("\nSuccessfully Update Employee!")

        elif choice == 5:
            user = int(input("Enter Employee user you want to delete:"))
            emp = employee.remove_employee_by_user(user)
            if not emp:
                print("\n Sorry, Delete Failed, Employee cant be found by this user: ", user)
            else:
                print("\nSuccessfully Deleted Employee!")

def main():
    conditions()

if __name__ == '__main__':
    main()

import time

class Person:
    def __init__(self, first_name, last_name, age):

        self.first_name = first_name
        self.last_name = last_name
        self.age = age

class Employer(Person):
    def __init__(self, user: int, first_name: str, last_name: str, age: int, job: str, salary: int, bonus: int):
        Person.__init__(self, first_name, last_name, age)
        self.user = user
        self.job = job
        self.salary = salary
        self.bonus = bonus

    employee_list = list()

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
                employee.user = user
                employee.first_name = first_name
                employee.last_name = last_name
                employee.age = age
                employee.job = job
                employee.salary = salary
                employee.bonus = bonus
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
        total_salary = self.bonus + self.salary
        return total_salary

    def email_address(self):
        email_address = self.last_name + self.first_name + "@capgemini.com"
        return email_address

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.first_name

    def set_last_name(self, last_name):
        self.first_name = last_name

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    def get_job(self):
        return self.job

    def set_job(self, job):
        self.age = job

    def get_salary(self):
        return self.salary

    def set_salary(self, salary):
        self.salary = salary

    def get_bonus(self):
        return self.bonus

    def set_bonus(self, bonus):
        self.bonus = bonus

    def __str__(self):
        time.sleep(1)
        return f"User ID: {self.user}\n" \
               f"First Name: {self.first_name}\n" \
               f"Last Name: {self.last_name}\n" \
               f"Age : {self.age}\n" \
               f"Job: {self.job}\n" \
               f"Salary: {self.salary}\n" \
               f"Bonus : {self.bonus}\n" \
               f"Total Salary: {self.total_salary()}\n" \
               f"Email address: {self.email_address()}"

def conditions():
    choice = 1
    employee = Employer(0, "", "", 0, "", 0, 0)

    while 1 <= choice <= 6:
        time.sleep(1)

        print("\n1.Add New Employee\n"
              "2.Get Employee list\n"
              "3.Get Employee By Id\n"
              "4.Update Employee by ID\n"
              "5.Remove Employee by ID\n"
              "6.Exit Program\n")
        try:
            choice = int(float(input("Please enter your choice: ")))
            print("\n")
        except ValueError:
            print("Please use the numbers displayed. Try again!")
            conditions()

        try:
            if choice == 1:
                    user = int(input("Enter Employee user number: "))
                    first_name = str(input("Enter Employee first name: "))
                    last_name = str(input("Enter Employee last name: "))
                    age = int(input("Enter Employee age: "))
                    job = str(input("Enter Employee department job: "))
                    salary = int(input("Enter Employee salary: "))
                    bonus = int(input("Enter Employee bonus: "))
                    emp = Employer(user, first_name, last_name, age, job, salary, bonus)
                    emp.add_new_employee()
                    print("Successfully created employee in out data base!")

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
                user = int(input("Enter Employee user number you want to update: "))
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
                    print("\n Sorry, Delete Failed, Employee cant be found by this user number: ", user)
                else:
                    print("\nSuccessfully Deleted Employee!")
            elif choice == 6:
                print("Ok! Good bye!")
                exit()
            else:
                if 1 >= choice <= 6:
                    break
                else:
                    print("Wrong number(s). Try again!")
                    conditions()
        except(NameError, ValueError, TypeError):
            print('Invalid Input(s), try again')

def main():
    conditions()

if __name__ == '__main__':
    main()

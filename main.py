"""
    RAHAT v1.0
Author: Suraj Singh
Contributors: Suraj Singh, Vagish Baweja
Date: 18-10-2021
Version Number: v1.0
Current Phase: Implementation
"""

from Database import Database
from SysAdmin import SysAdmin
from CampAdmin import CampAdmin
import os

''' -------- Driver function -------- '''


def main():
    which_portal = input("Select a portal (Camp-Admin (c)/System-Admin (s)): ")

    if which_portal.lower() == 's':
        pswd = input("Enter password to access System-Admin portal: ")
        admin = SysAdmin(pswd)

        # if admin != None:     # this was ineffective, and we don't even need such a check 
        # because if password is wrong, the creation of object named `admin` fails and program terminates instantly
        choice = -1
        os.system("cls")

        while choice != 0:
            print("\n----------Welcome to Admin portal-----------")
            print("1. Register a camp")
            print("2. De-register an accidentally registered camp")
            print("3. Read the relations of a camp")
            print("4. List all camps and their details")
            print("0. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                admin.registerCamp()
            elif choice == 2:
                admin.deRegister()
            elif choice == 3:
                admin.readCamp()
            elif choice == 4:
                admin.listAllRegCampsInfo()
            elif choice == 0:
                print("Exiting ...")
                exit(0)
            else:
                print("Error!! wrong choice")

            print()
            input("Enter a key to continue...")
            os.system("cls")

    elif which_portal.lower() == 'c':
        dbase = Database()
        campId = input("Enter your camp ID: ")
        campName = "camp" + campId

        if not dbase.isPresentCamp(campName):
            print("Error!! There's no camp with id " + campId)
            del dbase
            exit(-1)
        else:
            del dbase
            pswd = input("Enter password of camp" + campId + ": ")
            admin = CampAdmin(campName, pswd)
            os.system("cls")

            # if admin != None:     # this was ineffective, and we don't even need such a check 
            # because if password is wrong, the creation of object named `admin` fails and program terminates instantly

            # NOTE: we will maintain whether a person is present in camp or left, 
            # so that even if person leaves, we have his/her information
            # new column char(1) Present? (y/n)

            # one more column containing Flood codename will be present
            # will be same for all people 
            # but when database used in another flood later
            # flood codename will be updated and will be same for all people coming then
            # so on

            # contains consolidated information of camp, location, id, authorities list
            # maintainers etc (in a file or a new relation)

            choice = -1
            while choice != 0:
                print("\n----------Welcome to CampAdmin portal-----------")
                print("Connected to your camp camp" + campId + "\n")
                print("1. Read Record(s)")
                print("2. Enter a new Person's Record")

                print("3. Update details of a person")
                # also a col containing LeftDate needs to be updated
                print("4. Find vacancies in nearby camps")
                print("5. Read resource availability in other camp")
                print("6. Get Contact of camps having certain supply items available")
                print("7. Request supply from government")
                print("8. Update Supply data")
                print("9. Read new entries of the day in other camps")
                # also allows search in today's new entries of other camps
                # contains UniteProgram inside, so can unite the people who are found to their families

                # from general feedback to all types, including education of students, requirements, etc
                print("10. Send Feedback to SysAdmin (to NDRF authorities)")
                print("0. Exit")
                choice = int(input("Enter a choice: "))

                if choice == 1:
                    admin.readThis(campName)
                elif choice == 2:
                    admin.writeInto(campName)
                elif choice == 3:
                    admin.updateDetails(campName)
                elif choice == 4:
                    admin.findVacancies()
                elif choice == 5:
                    admin.readItemAvailability()
                elif choice == 6:
                    admin.contactSupplyFromCamps()
                elif choice == 7:
                    admin.requestSupplyFromMain(campName)
                elif choice == 8:
                    admin.updateSupplyData(campName)
                elif choice == 9:
                    admin.readTodayAll()
                elif choice == 10:
                    admin.feedback(campName)
                elif choice == 0:
                    print("Exiting...")
                    exit(0)
                else:
                    print("Error! Invalid choice.")

                print()
                input("Enter a key to continue...")
                os.system("cls")


if __name__ == '__main__':
    main()

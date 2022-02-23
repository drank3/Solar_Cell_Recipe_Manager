new_version_path = "no"
old_version_path = "no"



from PySide2 import QtSql, QtWidgets
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import pandas as pd
from PySide2.QtCore import Qt
import os



class Update_Manager():

    def __init__(self, default_version):
        self.connection_status = False
        #This is the version specified in the code, but is not updated with every patch
        self.default_version = default_version
        self.dir_path = os.path.dirname(__file__)
        self.version = self.Return_Current_Version()
        self.Create_Server_Connection()




    def Return_Current_Version(self):
        version_path = self.dir_path + r"\System Settings\Version.txt"
        try:
            with open(version_path, 'r') as file:
                version = file.read()
            return version
        except:
            self.Create_Version_File()
            return self.default_version


    def Create_Server_Connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host='170.187.158.29',
                #user='remote_user',
                #passwd='eml-lab293461',
                user='dranke',
                passwd='Ryl.14.Buin.547',
                database = 'Updates'
            )
            self.connection_status = True

            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
            self.connection_status = False

        self.connection = connection

        return connection


    def Check_For_Updates(self):
        try:
            all_updates = self.Retrieve_Update_Actions()

            [build_major, build_minor, build_patch] = [int(num) for num in self.version.split('.')]
            [latest_major, latest_minor, latest_patch] = [int(num) for num in self.latest_version.split('.')]

            if (self.version == self.latest_version):
                print("All up to date, moving on.")
            else:
                reply = QtWidgets.QMessageBox.question(None, 'Message',
                        f"A new update to Version {self.latest_version} is available. Update now?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

                if reply == QtWidgets.QMessageBox.Yes:
                    required_update_ids = []
                    #When this turns true, the updates are added to the queue (sort of)
                    new_condition= False
                    for update in all_updates:
                        u_version = update[1]
                        u_id = update[0]
                        if new_condition == False:
                            if self.version == u_version:
                                new_condition = True
                        elif new_condition == True:
                            if not self.version == u_version:
                                required_update_ids.append(u_id)

                    print(f"An update to version {self.latest_version} is available with {len(required_update_ids)} file alterations")

                    if (build_major==latest_major):
                        self.Run_Update_Actions(required_update_ids)
                    else:
                        #TODO: Make a GUI for large updates
                        print("Too much updating hassle")
                else:
                    print("Update was aborted by user")

        except Exception as e:
            print(f"Failed to check for updates with error code {e}")


    #This function takes a list of action ids as an input, and pulls the instructions for updates from the database
    # and enacts them
    def Run_Update_Actions(self, action_ids):
        try:
            for id in action_ids:
                print(id)

                cursor = self.connection.cursor()
                query = f"SELECT Version, Action, File, Old_Path, New_Path  FROM Update_Actions WHERE ID = {id}"
                cursor.execute(query)

                [update_version, update_action, update_file, old_path, new_path] = cursor.fetchall()[0]

                update_file = update_file.decode('utf-8')
                update_file = "".join([chr(int(binary, 2)) for binary in update_file.split(" ")])


                if update_action == "Replace":
                    os.remove(self.dir_path + old_path)
                    with open(self.dir_path + new_path, 'w') as file:
                        file.write(update_file)
                if update_action == "Remove":
                    os.remove(self.dir_path + old_path)
                if update_action == "Rename":
                    os.rename(self.dir_path + old_path, self.dir_path + new_path)
                if update_action == "Create":
                    with open(self.dir_path + new_path, 'w') as file:

                        file.write(update_file)

            #Setting the current version of the app to the version of the last update action after successful completion
            self.version = update_version
            self.Set_New_Version(self.version)


        except Exception as e:
            print(f"Update actions failed with error {e}")



    #Will find all of update actions in the databse above the current version
    def Retrieve_Update_Actions(self):
        cursor = self.connection.cursor()
        versions_query = "SELECT ID, Version FROM Update_Actions ORDER BY Version ASC"
        cursor.execute(versions_query)

        try:
            all_updates = cursor.fetchall()
            self.latest_version = all_updates[-1][1]
            return all_updates

        except Exception as e:
            self.latest_version = self.version
            return []


    def Create_Version_File(self):
        if os.path.isfile(self.dir_path + r"\System Settings\Version.txt"):
            pass
        elif os.path.isdir(self.dir_path + r"\System Settings"):
            with open(self.dir_path + r"\System Settings\Version.txt", 'w') as file:
                file.write(self.default_version)
        else:
            os.mkdir(self.dir_path + r"\System Settings")
            with open(self.dir_path + r"\System Settings\Version.txt", 'w') as file:
                file.write(self.default_version)

    def Set_New_Version(self, version):
        version_path = self.dir_path + r"\System Settings\Version.txt"
        try:
            with open(version_path, 'w') as file:
                version = file.write(version)
            return version
        except Exception as e:
            print(f"Setting the new version number failed with error {e}")




if __name__ == "__main__":
    um = Update_Manager("1.0.00")



    cursor = um.connection.cursor()

    #SQL doesn't like apostrophes in data, so  need to double them up wherever they are
    path = r"/Trial_Update_Text.txt"
    file= "Should be some text here"
    file = ' '.join(format(ord(i), '08b') for i in file)
    query_add = f"INSERT INTO Update_Actions(ID, Version, Action, File, Old_Path, New_Path) VALUES(16, '1.0.01','Create' ,'{file}', '{path}', '{path}');"

    cursor.execute(query_add)
    um.connection.commit()
    cursor.close()

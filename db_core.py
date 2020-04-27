from collections import defaultdict
import os.path
import pickle
import shutil
import csv

HANDLER_EDIT = 0
HANDLER_ADD = 1


class DataBase:
    def __init__(self):
        self.fields = ["nickname",
                       "battles_amount",
                       "wins_amount",
                       "tanks_amount",
                       "is_banned",
                       "is_tester",
                       "motto",
                       "clan_name"]

        self.init_dicts()
        self.create_or_read_file()

    def init_dicts(self):
        """
        Inits records and fields dictionaries in database
        """

        self.records_dict = dict()
        self.fields_dict = {field: defaultdict(set) for field in self.fields}

    def get_records_dict(self) -> dict:
        """
        Gets records dictionary (for displaying records) from database
        :returns: Records dictionary
        """

        return self.records_dict

    def get_fields_dict(self) -> dict:
        """
        Gets fields dictionary (for search by fields) from database
        :returns: Fields dictionary
        """

        return self.fields_dict

    def get_record(self, nickname: str) -> dict:
        """
        Gets record from database
        :param nickname: nickname of needed record
        :type nickname: str
        :returns: Record from database
        """

        return self.records_dict[nickname]

    def add_record(self, record: dict) -> (bool, str):
        """
        Adds record to database
        :param record: new record
        :type record: dict
        :returns: False (in error case) or True and Error/Done message
        """

        handler_answer = self.nickname_handler(record, HANDLER_ADD)

        if handler_answer[0]:
            nickname: str = record['nickname']
            self.records_dict[nickname] = {}

            for key in self.fields:
                if key not in record:
                    record[key] = "-"
                self.records_dict[nickname][key] = record[key]
                self.fields_dict[key][record[key]].add(nickname)
        return handler_answer

    def delete_record(self, nickname: str):
        """
        Deletes record from database
        :param nickname:
        :type nickname: str
        """

        deleted_record = self.get_record(nickname)

        del self.records_dict[nickname]

        for key, value in deleted_record.items():
            self.fields_dict[key][value].remove(nickname)
            if not self.fields_dict[key][value]:
                del self.fields_dict[key][value]

    def edit_record(self, old_nickname: str, new_record: dict) -> (bool, str):
        """
        Edits record from database
        :param old_nickname: nickname before editing
        :param new_record: record with new nickname
        :type old_nickname: str
        :type new_record: dict
        :returns: False (in error case) or True and Error/Done message
        """

        new_nickname = new_record['nickname']
        if old_nickname != new_nickname:
            handler_answer = self.nickname_handler(new_record, HANDLER_EDIT)
        else:
            handler_answer = True, "Record was successfully edited!"

        if handler_answer[0]:
            for key in new_record:
                if not new_record[key]:
                    new_record[key] = "-"
            self.delete_record(old_nickname)
            self.add_record(new_record)
            return True, "Record was successfully edited!"
        else:
            return handler_answer

    def nickname_handler(self, record: dict, command: int) -> (bool, str):
        """
        Handles nickname entered by user
        :param record: record with entered nickname
        :param command: type of operation for record (add or edit)
        :type record: dict
        :type command: int
        :returns: False (in error case) or True and Error/Done message
        """

        if record.get('nickname') is None:
            return False, "Invalid (or empty) nickname!"

        nickname: str = record['nickname']

        if nickname in self.records_dict:
            return False, "Nickname is already in DB!"

        if command == 0:
            return True, "Record was successfully edited!"
        elif command == 1:
            return True, "Record was successfully added!"
        else:
            return False, "Oops. Something went wrong. Try again!"

    def search_record(self, search_dict: dict) -> (bool, str or set):
        """
        Searches usernames of players by fields in search dictionary
        :param search_dict: dictionary with search queries
        :type search_dict: dict
        :returns: False and Error string if search was failed or True and set of search result
        """

        if not search_dict:
            return False, "All search fields are empty!"

        search_fields = list(search_dict.keys())
        result_set = self.fields_dict[search_fields[0]][search_dict[search_fields[0]]].copy()
        for field in search_fields:
            temp_field = self.fields_dict[field][search_dict[field]].copy()
            result_set.intersection_update(temp_field)

        if not result_set:
            return False, "Records not found!"

        return True, result_set

    def create_or_read_file(self):
        """
        Creates database (.bd) file or read if it exists
        """

        if self.check_for_database():
            with open("base.bd", "rb") as pickle_in:
                database_dict = pickle.load(pickle_in)
            self.records_dict = database_dict['records_dict']
            self.fields_dict = database_dict['fields_dict']
        else:
            self.write_database_to_file()

    def write_database_to_file(self):
        """
        Dumps dictionary with database to .bd file
        """

        pickle_dict = {"records_dict": self.records_dict, "fields_dict": self.fields_dict}
        with open("base.bd", "wb") as pickle_out:
            pickle.dump(pickle_dict, pickle_out)

    @staticmethod
    def check_for_database():
        """
        Checks for database (.bd) file in / directory
        """

        return os.path.isfile("base.bd")

    @staticmethod
    def check_for_backup():
        """
        Checks for backup (.bak) file in / directory
        """

        return os.path.isfile("base.bak")

    def delete_database_file(self):
        """
        Deletes database file (.bd)
        """

        if self.check_for_database():
            os.remove("base.bd")
            self.init_dicts()

    def create_backup_of_database(self):
        """
        Creates backup (.bak file) of database
        """

        if self.check_for_database():
            shutil.copy2("base.bd", "base.bak")

    def recover_database_from_backup(self):
        """
        Recovers database from backup (.bak file)
        """

        if self.check_for_backup():
            shutil.copy2("base.bak", "base.bd")
            self.create_or_read_file()

    def delete_backup(self):
        """
        Deletes backup (.bak file) of database
        """

        if self.check_for_backup():
            os.remove("base.bak")

    def export_to_csv(self):
        """
        Exports database to CSV file
        """

        with open("base.csv", 'w', encoding="UTF-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writeheader()
            for row in self.records_dict:
                writer.writerow(self.records_dict[row])





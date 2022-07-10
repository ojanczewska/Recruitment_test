import re
import os
import csv
import argparse
import numpy as np


class Email:
    def __init__(self):
        self.folder_name = "emails"
        # list with all emails from emails files
        self.email_list = []
        self.read_emails_from_file()
        # list with all correct emails
        self.correct_emails = []
        # list with all incorrect emails
        self.incorrect_emails = []
        # list of emails containing a given string
        self.found_emails = []
        # dictionary with grouped emails by domain
        self.grouped_emails = {}
        # list of sorted key names (domains names) from grouped_emails dictionary
        self.sorted_names = []
        # list of emails in logs file
        self.in_logs_emails = []
        # list of emails no in logs file
        self.not_in_logs_emails = []

        self.divide_emails()

    # extracting emails from files
    def read_emails_from_file(self):
        for file in os.listdir(self.folder_name):
            if file[-3:] == "txt":
                with open("emails/" + file) as f:
                    lines = f.readlines()
                for e in lines:
                    self.email_list.append(e.replace('\n', ""))
            else:
                file_name = open("emails/" + file)
                csvreader = csv.reader(file_name)
                email_row = 1
                for row in csvreader:
                    row = row[0].split(';')
                    if row[email_row] == 'email':
                        continue
                    self.email_list.append(row[email_row])

    # division of emails into correct and incorrect
    def divide_emails(self):
        valid_email = re.compile(r'(([\w\.]+)@([\w]+\.[a-zA-Z\d]{1,4}))')

        for e in self.email_list:
            if valid_email.match(e):
                self.correct_emails.append(e)
            else:
                self.incorrect_emails.append(e)

        # rejecting duplicates
        self.correct_emails = np.unique(self.correct_emails)
        self.correct_emails = sorted(self.correct_emails)

    # print the number of invalid emails, then one invalid email per line
    def show_incorrect_emails(self):
        print(f"Invalid emails ({len(self.incorrect_emails)})")
        for e in self.incorrect_emails:
            print("\t" + e)

    # search emails by text
    def search_emails_by_text(self, string_argument):
        pattern = re.compile(string_argument)

        for e in self.correct_emails:
            if pattern.search(e):
                self.found_emails.append(e)

        #  print the number of found emails, then one found email per line
        print(f"Found emails with '{string_argument}' in email ({len(self.found_emails)}):")
        for e in self.found_emails:
            print("\t" + e)

    # group emails by domain
    def group_emails_by_domain(self):
        for e in self.correct_emails:
            # extracting domain name from emails
            domain_name = e.split('@')
            domain_name = domain_name[1]

            # creating dictionary of domain names
            if domain_name not in self.grouped_emails:
                self.grouped_emails[domain_name] = e
            elif type(self.grouped_emails[domain_name]) == list:
                self.grouped_emails[domain_name].append(e)
            else:
                self.grouped_emails[domain_name] = [self.grouped_emails[domain_name], e]

        self.show_group_emails()

    # printing grouped emails by domains
    def show_group_emails(self):
        self.sorted_names = sorted(self.grouped_emails)

        for e in self.sorted_names:
            if type(self.grouped_emails[e]) == list:
                number_of_emails = len(self.grouped_emails[e])
            else:
                number_of_emails = 1

            print(f"Domain name: {e} ({number_of_emails}):")
            if type(self.grouped_emails[e]) == list:
                for x in self.grouped_emails[e]:
                    print('\t' + x)
            else:
                print('\t' + self.grouped_emails[e])

    # find emails that are not in the logs file
    def check_logs_file(self, path):
        # extracting emails from logs file
        with open(path) as f:
            lines = f.readlines()
        email_idx = 1
        self.in_logs_emails = [e.split("'")[email_idx] for e in lines]

        # find emails that are not in the logs file
        self.in_logs_emails = sorted(self.in_logs_emails)
        self.not_in_logs_emails = set(self.correct_emails) - set(self.in_logs_emails)
        self.not_in_logs_emails = sorted(self.not_in_logs_emails)

        # print the numbers of found emails, then one found email per line sorted alphabetically
        print(f"Emails not sent ({len(self.not_in_logs_emails)}):")
        for e in self.not_in_logs_emails:
            print('\t' + e)

    # execute chosen operations
    def execute_email_operation(self, parser_args):
        if parser_args.incorrect_emails:
            self.show_incorrect_emails()

        if parser_args.group_by_domain:
            self.group_emails_by_domain()

        if parser_args.search:
            self.search_emails_by_text(parser_args.search)

        if parser_args.find_emails_not_in_logs:
            file = parser_args.find_emails_not_in_logs
            # validation of input data
            try:
                self.check_logs_file(file)
            except OSError:
                print("Incorrect file path")


# add arguments to the parser
def add_parser_arguments():
    parser.add_argument('-ic',
                        '--incorrect-emails',
                        action='store_true',
                        help='show incorrect emails ')

    parser.add_argument('-gbd',
                        '--group-by-domain',
                        action='store_true',
                        help='group emails by domain ')

    parser.add_argument('-s',
                        '--search',
                        action='store',
                        metavar='str',
                        help='search emails by text (str)')

    parser.add_argument('-feil',
                        '--find-emails-not-in-logs',
                        action='store',
                        metavar='path_to_logs_file',
                        help='find emails that are not in the logs file')


parser = argparse.ArgumentParser(description='Perform operations on the email data')
add_parser_arguments()
args = parser.parse_args()

email_operation = Email()
email_operation.execute_email_operation(args)

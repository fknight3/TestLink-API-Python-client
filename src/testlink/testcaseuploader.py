"""
    This module is the terminal interface for the TestLink Uploader. The expected workflow is that
    once an engineer has completed creating new test cases they will use this tool to upload their
    new test cases to the TestLink Application. The only inputs the application expects from users
    are the files they would like to upload and the location of their test projects library files.
"""

import os
import sys
import getpass
import re
from pprint import pprint
from time import sleep
from pyfiglet import Figlet
import inquirer
import testlink


def update_sys_path(lib_path):
    """Adds the path for the projects libraries to the sys.path

        This is needed to avoid any errors with loading the dependencies for the test file(s).

        Args:
            lib_path (str): The path to the test projects library files

    """
    sys.path.append(os.path.abspath(lib_path))


def call_test_link_api(file_path):
    """Handles the API calls to TestLink

        Args:
            file_path (str): The path to a file containing test cases to upload

        Returns:
            tl_api_response (dict): Metadata about the API response

    """
    sys.path.append(os.path.split(file_path)[0])
    test_file_path = os.path.split(file_path)[1].split('.py')[0]
    imported_test_file = __import__(test_file_path)
    test_class_name = test_file_path.replace('test', 'Tc').replace('_', ' ').title().replace(
        ' ', '')
    tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
    count_cases_uploaded = tls.bulkTestCaseUpload(getpass.getuser(), file_path,
                                                  getattr(imported_test_file, test_class_name))
    tl_api_response = {'test_file': test_file_path, 'uploaded_cases': count_cases_uploaded}
    return tl_api_response


def upload_test_cases(files_list):
    """Uploads a group of test files to TestLink.

        Args:
            files_list (list): A list of full paths for each file to be uploaded to TestLink

    """
    for file_path in files_list:
        tl_output = call_test_link_api(file_path)
        if tl_output['uploaded_cases'] is not 0:
            print(tl_output['test_file'] + ': Uploaded ' + str(tl_output['uploaded_cases']) +
                  ' new test cases.')
        else:
            print(tl_output['test_file'] + ': There were no test cases to import.')


def get_tests_to_upload(test_prefix='test_'):
    """Get information from the user regarding the files they are uploading via the API.

    Uses the inquirer command line user interface to query the user. The inquirer cli will validate
    all data submitted. A user may choose to upload a single file or upload an entire folder.
    Note - that when uploading a folder, all of the root folders' subdirectories will be searched
    for test files to upload. The default prefix for a test files is "test_".

        Args:
            test_prefix (str): The naming convention used for files containing test cases
            that should be uploaded to TestLink.

        Returns:
            A dict containing the data that will be uploaded. Either the the test_file key or
            test_folder will be returned depending on what type of upload the user has selected.
            Example:
                {'libs_dir': '/home/johndoe/test_project',
                 'test_file': 'home/johndoe/test_project/test_item.py'}

    """
    if inquirer.list_input('How many test files do you need to upload?',
                           choices=['Single', 'Multiple']) == 'Single':
        questions = [
            inquirer.Path('test_file', message="Which test file are you uploading?",
                          path_type=inquirer.Path.FILE),
            inquirer.Path('libs_dir', message="Whats the path to your projects library files?",
                          path_type=inquirer.Path.DIRECTORY)
        ]
    else:
        questions = [
            inquirer.Path('test_folder', message="Which test folder are you uploading?",
                          path_type=inquirer.Path.DIRECTORY),
            inquirer.Path('libs_dir', message="Whats the path to your projects library files?",
                          path_type=inquirer.Path.DIRECTORY)
        ]
    answers = inquirer.prompt(questions)
    files_to_upload = []

    if 'test_folder' in answers:
        for root, dirs, files in os.walk(answers['test_folder']):
            for file in files:
                if re.search(test_prefix + '.*.py$', file) is not None:
                    files_to_upload.append(root + '/' + file)
    else:
        files_to_upload.append(answers['test_file'])

    upload_data = {'tests': files_to_upload, 'libs_dir': answers['libs_dir']}
    upload_data['confirmed'] = confirm_upload(upload_data['tests'])
    return upload_data


def confirm_upload(test_file_list):
    """Confirm if the user would like to proceed with uploading test data.

    For folder uploads, the arg value will be presented to the user in a list. The intention is
    that they will be able to review the list of files the program found and confirm if they would
    like to proceed.

    For single file uploads, the arg value will be presented to the user for confirmation that the
    path they previously submitted was correct.

        Args:
            test_file_list (list): A list of test files that were identified as upload candidates

        Returns:
            A string value of 'Yes' or 'No'

    """
    if len(test_file_list) > 1:
        print('\nFound ' + str(len(test_file_list)) + ' test(s) to upload.\n')
        print('Test(s):')
        pprint(test_file_list)
        print('\n')
        message_content = 'Are you sure you would like to upload these files?'
    else:
        message_content = 'Are you sure you would like to upload: ' + \
                          os.path.split(test_file_list[0])[1] + '?'
    confirmed = inquirer.list_input(message_content, choices=['Yes', 'No'])
    return confirmed


def display_splash_screen():
    """Print out an ASCII Text Banner."""
    print(Figlet(font='slant').renderText('TestLink\nUploader'))


def restart_application():
    """Restart the application.

    This process includes clearing the screen and displaying the splash screen again. The sleep was
    added to give the terminal time to catch up with the code.

    """
    os.system('clear')
    sleep(0.5)
    display_splash_screen()


def exit_application():
    """Exit the application.

    This process gives the user notification that we are stopping the application. Clear the
    terminal for them and then exit the python application.

    """
    print('Exiting the TestLink Uploader...')
    sleep(1)
    os.system('clear')
    sys.exit()


def main():
    os.system('clear')
    display_splash_screen()

    # Get Test Case Data
    info = get_tests_to_upload()
    while info['confirmed'] == 'No':
        if inquirer.list_input('Would you like to exit the application?',
                               choices=['Yes', 'No']) == 'Yes':
            exit_application()
        restart_application()
        info = get_tests_to_upload()
    update_sys_path(info['libs_dir'])
    upload_test_cases(info['tests'])

    # Upload Data

    # Verify the user is finished
    if inquirer.list_input('Do you have more tests to upload?', choices=['Yes', 'No']) == 'Yes':
        main()
    else:
        exit_application()


main()

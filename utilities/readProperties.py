"""
This class is to read the properties required for test execution
"""
import configparser
import fnmatch
import os

config = configparser.RawConfigParser()
config.read(os.getcwd() + "\\Configurations\\config.ini")


class ReadConfig:

    # static method helps you read the function in another file without instantiating the class
    @staticmethod
    def getApplicationURL(env):
        if env == 'non-prod':
            return f"https://indianexpress.com/"

    @staticmethod
    def get_news_name():
        news_link = config.get('commonInfo', 'news_link')
        return news_link

    @staticmethod
    def getEpsilonTeamName():
        team_name = config.get('commonInfo', 'team_name')
        return team_name

    @staticmethod
    def getBrowserName():
        browsername = config.get('commonInfo', 'browser')
        return browsername

    @staticmethod
    def get_no_of_carousel():
        no_of_carousel = config.get('commonInfo', 'no_of_carousel')
        return no_of_carousel

    @staticmethod
    def getORFilePath(env):
        if env == 'non-prod':
            OR = config.get('commonInfo', 'OR_Testenv')
        return OR

    @staticmethod
    def get_headless_mode():
        headless = config.get('commonInfo', 'headless')
        return headless

    # @staticmethod
    # def getS2TPath():
    #     s2tpath = config.get('commonInfo', 's2t')
    #     return s2tpath

    # To get the path of the given filename in the specific directory
    @staticmethod
    def get_file_path(filename, dirpath):
        result = []
        for root, dirs, files in os.walk(dirpath):
            if filename in files:
                result.append(os.path.join(root, filename))
        return result[0]

    # To search the file with the given pattern in the specific directory and return the filepath
    @staticmethod
    def search_file_pattern(dirpath, pattern):
        result = []
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    result.append(os.path.join(file))
        return result

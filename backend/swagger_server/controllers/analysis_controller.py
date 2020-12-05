"""This module handles the logic for performing concordance analysis on a given body of text."""
import operator
import re

#import boto3
#import botocore.exceptions
import connexion
import nltk
from nltk.tokenize import RegexpTokenizer
from time import perf_counter_ns
#from swagger_server.database_methods import (
#    ConcordanceTableOperations,
#    LocationsTableOperations,
#)
from swagger_server.models.location_result import LocationResult
from swagger_server.models.location_result_concordance import LocationResultConcordance
from swagger_server.models.result import Result
from swagger_server.models.result_concordance import ResultConcordance


def get_concordance(body=None):  # noqa: E501
    """Calculate

    Post text to generate concordance # noqa: E501

    :param body: Text to be analyzed
    :type body: dict | bytes

    :rtype: Result
    """
    code = 200

    #connected_to_database = False

    #try:
    #    ConcordanceTableOperations.create_concordance_table()
    #except botocore.exceptions.ClientError:
    #    print("Failed to communicate with DynamoDB, so it will not be used.\n")
    #    connected_to_database = False

    try:
        if connexion.request.is_json:
            body = str.from_dict(connexion.request.get_json())  # noqa: E501

        input_text = body.decode("utf-8")
        concordance = []

        #if connected_to_database:
        #    dynamodb_resource = boto3.resource("dynamodb", region_name="us-east-2")
        #    table = dynamodb_resource.Table("concordance")
        #    response = table.get_item(Key={"input": input_text})
        #
        #    if "Input" in response:
        #        concordance = response["input"]["concordance"]

        #else:

        # start timer
        timer_start = perf_counter_ns()

        # initialize regular expression that excludes all punctuation and
        # other special characters except for apostrophes and hyphens
        regex = "[^a-zA-Z'\- ]+"

        # parse only alpha characters using the initialized regular expression
        input_split = re.sub(regex, "", input_text.lower())

        #stop timer
        timer_stop = perf_counter_ns()

        print("Time to run Analyze: ", timer_stop - timer_start, "ns")

        input_split = input_split.split()

        used_words = []
        for word in input_split:
            if used_words.count(word) == 0:
                concordance.append(ResultConcordance(word, input_split.count(word)))
                used_words.append(word)

        concordance.sort(key=operator.attrgetter("token"))

    # general exception is used here as a 'catch-all'
    # concordance should return an empty result if it failed regardless of the error
    except Exception as e:
        print(e)
        concordance = []
        code = 400

    result = Result(concordance, input_text)

    #f connected_to_database:
    #    ConcordanceTableOperations.upload_concordance_data(result)

    return result, code


def get_concordance_with_location(body=None):  # noqa: E501
    """Calculate Location

    Post text to generate concordance that includes the location of each word # noqa: E501

    :param body: Text to be analyzed
    :type body: dict | bytes

    :rtype: LocationResult
    """
    code = 200

    #connected_to_database = True

    #try:
    #    LocationsTableOperations.create_location_table()
    #except botocore.exceptions.ClientError:
    #    print("Failed to communicate with DynamoDB, so it will not be used.\n")
    #    connected_to_database = False

    try:
        if connexion.request.is_json:
            body = str.from_dict(connexion.request.get_json())  # noqa: E501

        # initialize regular expression that excludes all punctuation and
        # other special characters except for apostrophes and hyphens
        regex = "[^a-zA-Z'\- ]+"

        input_text = body.decode("utf-8")
        concordance = []

        #if connected_to_database:
        #    dynamodb_resource = boto3.resource("dynamodb", region_name="us-east-2")
        #    table = dynamodb_resource.Table("locations")
        #    response = table.get_item(Key={"input": input_text})
        #
        #    if "Input" in response:
        #        concordance = response["input"]["concordance"]

        #else:
           
        # parse only alpha characters using the initialized regular expression
        input_split = re.sub(regex, "", input_text.lower())
        input_split = input_split.split()

        used_words = []
        for word in input_split:
            if used_words.count(word) == 0:
                locations = [
                    i for i in range(len(input_split)) if input_split[i] == word
                ]
                concordance.append(LocationResultConcordance(word, locations))
                used_words.append(word)

        concordance.sort(key=operator.attrgetter("token"))

    # general exception is used here as a 'catch-all'
    # concordance should return an empty result if it failed regardless of the error
    except Exception:
        concordance = []
        code = 400

    result = LocationResult(concordance, input_text)

    #if connected_to_database:
    #    LocationsTableOperations.upload_location_data(result)

    return result, code

def get_concordance_nltk(body=None):  # noqa: E501
    """Calculate

    Post text to generate concordance # noqa: E501

    :param body: Text to be analyzed
    :type body: dict | bytes

    :rtype: Result
    """
    code = 200

    try:
        if connexion.request.is_json:
            body = str.from_dict(connexion.request.get_json())  # noqa: E501

        input_text = body.decode("utf-8")
        concordance = []

        # start timer
        timer_start = perf_counter_ns()

        # initialize regular expression that excludes all punctuation and
        # other special characters except for apostrophes and hyphens
        tokenizer = RegexpTokenizer("[a-zA-Z'\-]+")

        input_split = tokenizer.tokenize(input_text.lower())

        #stop timer
        timer_stop = perf_counter_ns()

        print("Time to run NLTK: ", timer_stop - timer_start, "ns")

        used_words = []
        for word in input_split:
            if used_words.count(word) == 0:
                concordance.append(ResultConcordance(word, input_split.count(word)))
                used_words.append(word)

        concordance.sort(key=operator.attrgetter("token"))

    # general exception is used here as a 'catch-all'
    # concordance should return an empty result if it failed regardless of the error
    except Exception as e:
        print(e)
        concordance = []
        code = 400

    result = Result(concordance, input_text)

    return result, code    

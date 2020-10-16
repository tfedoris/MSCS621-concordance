import decimal
import json
import operator
import re
from collections import Counter

import boto3
import connexion
import six
from boto3.dynamodb.conditions import Key
from swagger_server import util
from swagger_server.database_methods import (ConcordanceTableOperations,
                                             LocationsTableOperations)
from swagger_server.models.location_result import LocationResult
from swagger_server.models.location_result_concordance import \
    LocationResultConcordance
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
    
    ConcordanceTableOperations.create_concordance_table()

    try:
        if connexion.request.is_json:
            body = str.from_dict(connexion.request.get_json())  # noqa: E501
        
        #initialize regular expression that excludes all punctuation and
        #other special characters except for apostrophes and hyphens
        regex = "[^a-zA-Z'\- ]+"
        
        input = body.decode('utf-8')
        concordance = []

        dynamodb_resource = boto3.resource('dynamodb')
        table = dynamodb_resource.Table('concordance')
        response = table.get_item(
            Key={
                'input': input
            }
        )

        if 'Input' in response:
            concordance = response['input']['concordance']

        else:  
            #parse only alpha characters using the initialized regular expression
            input_split = re.sub(regex, '', input.lower())
            input_split = input_split.split()
            
            used_words = []
            for word in input_split:
                if (used_words.count(word) == 0):
                    concordance.append(ResultConcordance(word, input_split.count(word)))
                    used_words.append(word)
        
        concordance.sort(key=operator.attrgetter('token'))
        
    except Exception as error:
        concordance = []
        code = 400

    result = Result(concordance, input)

    ConcordanceTableOperations.upload_concordance_data(result)

    return result, code


def get_concordance_with_location(body=None):  # noqa: E501
    """Calculate Location

    Post text to generate concordance that includes the location of each word # noqa: E501

    :param body: Text to be analyzed
    :type body: dict | bytes

    :rtype: LocationResult
    """
    code = 200

    LocationsTableOperations.create_location_table()
    
    try:
        if connexion.request.is_json:
            body = str.from_dict(connexion.request.get_json())  # noqa: E501
            
        #initialize regular expression that excludes all punctuation and
        #other special characters except for apostrophes and hyphens
        regex = "[^a-zA-Z'\- ]+"
        
        input = body.decode('utf-8')
        concordance = []

        dynamodb_resource = boto3.resource('dynamodb')
        table = dynamodb_resource.Table('locations')
        response = table.get_item(
            Key={
                'input': input
            }
        )

        if 'Input' in response:
            concordance = response['input']['concordance']
        
        else:
            #parse only alpha characters using the initialized regular expression
            input_split = re.sub(regex, '', input.lower())
            input_split = input_split.split()
            
            used_words = []
            for word in input_split:
                if (used_words.count(word) == 0):
                    locations = [i for i in range(len(input_split)) if input_split[i] == word]
                    concordance.append(LocationResultConcordance(word, locations))
                    used_words.append(word)
        
        concordance.sort(key=operator.attrgetter('token'))
    
    except Exception as error:
        concordance = []
        code = 400

    result = LocationResult(concordance, input)

    LocationsTableOperations.upload_location_data(result)
    
    return result, code

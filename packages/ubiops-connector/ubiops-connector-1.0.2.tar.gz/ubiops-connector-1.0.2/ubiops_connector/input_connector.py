import logging

from .utilities import map_data


logger = logging.getLogger('Connector')


class InputConnector:

    def __init__(self, base_directory, context):
        """
        Initialisation method for the connector

        :param str base_directory: absolute path to the directory where the model file is located
        :param dict context: a dictionary containing details of the model deployment that might be useful in your code
        """

        self.base_directory = base_directory
        self.context = context

    def request(self, data):
        """
        Method for requests, called separately for each individual request. Map the input fields, if necessary, and
        insert the given input data into the database.

        :param dict data: input data for the connector. Not used as this is an input connector
        """

        data = self.retrieve()
        return map_data(data)

    def retrieve(self):
        """
        Insert given data into the database. This method must be implemented in each connector class.

        :return dict|list: dictionary with the values expected as output of the deployment, or a list of those
            dictionaries
        """

        raise NotImplementedError

    def stop(self):
        """
        Stop the connector by closing the connection to the data source
        """

        pass

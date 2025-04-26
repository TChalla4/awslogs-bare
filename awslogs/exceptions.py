class BaseAWSLogsException(Exception):

    code = 1

    def hint(self):
        return "Unknown Error."


class UnknownDateError(BaseAWSLogsException):

    code = 3

    def hint(self):
        return "awslogs doesn't understand '{}' as a date.".format(self.args[0])


class TooManyStreamsFilteredError(BaseAWSLogsException):

    code = 6

    def hint(self):
        return (
            "The number of streams that match your pattern '{}' is '{}'. "
            "AWS API limits the number of streams you can filter by to {}."
            "It might be helpful to you to not filter streams by any "
            "pattern and filter the output of awslogs."
        ).format(self.args[0], self.args[1], self.args[2])


class NoStreamsFilteredError(BaseAWSLogsException):

    code = 7

    def hint(self):
        return (
            "No streams match your pattern '{}' for the given time period."
        ).format(self.args[0])

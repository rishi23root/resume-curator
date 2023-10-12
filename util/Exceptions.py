# place to put all the custorm exceptions

# class InvalidAttrException(Exception,etype):
#     "error with the arrgument attributes"
#     print(etype)
#     pass


class InvalidAttrException(Exception):
    def __init__(self, message, error_code):
        self.message = "Template data Error: " + message
        self.error_code = error_code
        self.attr = message

# class InvalidAttrException(Exception):
#     def __init__(self, message, cause=None):
#         self.message = message
#         self.cause = cause

#     def __str__(self):
#         if self.cause:
#             return f'CustomException: {self.message} caused by {self.cause}'
#         else:
#             return f'CustomException: {self.message}'

#     def __cause__(self):
#         return self.cause
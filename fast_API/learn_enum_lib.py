#!/usr/bin/python3
from enum import IntEnum

"""
enum library: provides support for enumeration. In this case 
IntEnum allows to define enumerations where the members are also
integers and can be used in context where an integer is expected
"""

class Status(IntEnum):
    SUCCESS=200
    FAILURE=404

my_status=Status.SUCCESS
print(f"Status Code: {my_status}>>{my_status==200}")



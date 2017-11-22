"""
@author: grimrhapsody
"""

from enum import Enum


""" CONDITION REGISTERS """


class condition(Enum):
    continue_execution = 0
    and1 = 1
    and2 = 2
    and3 = 3
    and4 = 4
    and5 = 5
    and6 = 6
    and7 = 7
    or1 = -1
    or2 = -2
    or3 = -3
    or4 = -4
    or5 = -5
    or6 = -6
    or7 = -7


""" HELPER CONSTANTS """

CONT = condition.continue_execution
AND1 = condition.and1
AND2 = condition.and2
AND3 = condition.and3
AND4 = condition.and4
AND5 = condition.and5
AND6 = condition.and6
AND7 = condition.and7
OR1 = condition.or1
OR2 = condition.or2
OR3 = condition.or3
OR4 = condition.or4
OR5 = condition.or5
OR6 = condition.or6
OR7 = condition.or7


""" EVENT ENUM DEFINITIONS """

class ai_status_type(Enum):
    normal = 0
    recognition = 1
    alert = 2
    battle = 3





class flag_type(Enum):
    event_flag = 0
    event = 1
    event_with_slot = 2
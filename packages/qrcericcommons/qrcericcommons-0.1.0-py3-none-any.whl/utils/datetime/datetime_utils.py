# -*- coding: utf-8 -*-
# @Time    : 2019/11/19 20:19
# @Author  : Dong Qirui
# @Software: PyCharm

from datetime import datetime, timedelta


def getTomorrowDateStrftimeFull () -> str :
    '''
    
    :return: '2019-5-8'
    '''
    return (datetime.today() + timedelta( days=+1 )).strftime( "%Y-%-m-%-d" )


def getTodayDateStrftimeFull () -> str :
    '''

    :return: '2019-5-8'
    '''
    return datetime.today().strftime( "%Y-%-m-%-d" )


def getTodayDateStrftime ( delta: int = 0 ) :
    '''
    
    :return: '2019-05-08'
    '''
    return (datetime.today() + timedelta( days=+delta )).strftime( "%Y-%m-%d" )


def getTodayDateStrftimeShort ( delta: int = 0 ) -> str :
    '''
    
    :return: '20190508'
    '''
    return (datetime.today() + timedelta( days=+delta )).strftime( "%Y%m%d" )


def getTodayMonthStrftime () -> str :
    '''
    
    :return: '2019-5'
    '''
    return datetime.today().strftime( "%Y-%-m" )


def getTodayTimeStrftime () -> str :
    '''
    
    :return: '2019-05-08 16:43:18'
    '''
    return datetime.now().strftime( '%Y-%m-%d %H:%M:%S' )


def getDateTimeStrftime ( format: str = '%Y-%m-%d %H:%M:%S' ) -> str :
    '''
    based on format
    :return: '2019-05-08 16:43:18'
    '''
    return datetime.now().strftime( format )


def getNow () :
    return datetime.now()

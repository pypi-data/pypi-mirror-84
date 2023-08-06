
from numpy import array, diff, where, split
import itertools

def grouper(l):
    resultList = split(l, where(diff(l)!=0)[0]+1)
    groupListNum = [[i for x in range(len(tempGroup))] for i,tempGroup in enumerate(resultList)]
    groupListNumMerged = list(itertools.chain.from_iterable(groupListNum))
    return groupListNumMerged


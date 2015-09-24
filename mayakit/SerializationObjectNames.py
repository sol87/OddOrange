#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
#=============================================
import re, string
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def SerializationObjectNames(objectList, nameFormat='Temp*', start=0, padding=3):
    '''
    objectList must is a list or a tuple
    nameFormat mutst have one " * "
    Exp:
            [pCulbe,  pCulbe1, pCulbe2, pCulbe3, pCulbe4] -> temp*
        ->  [temp000, temp001, temp002, temp003, temp004] 
    
            [pCulbe,  pCulbe1, pCulbe2, pCulbe3, pCulbe4] -> C_temp*_geo_0
        ->  [C_temp000_geo_0, C_temp001_geo_0, C_temp002_geo_0, C_temp003_geo_0, C_temp004_geo_0] 
    '''
    if not isinstance(objectList, (list, tuple)):
        return
    
    if nameFormat.count('*') != 1:
        return
    
    newNameList = []
    for i, obj in enumerate(objectList):
        newName = compileMayaObjectName(nameFormat.replace('*', string.zfill(i + start, padding)))
        newNameList.append(newName)
    return newNameList

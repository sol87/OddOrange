#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
#=============================================
import re, string
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def compileMayaObjectName(objectName):
    '''
    build a not exists maya object name...
    Exp: 
        pCube  -> pCube1  -> pCube2  -> pCube3  -> pCube4 ...  pCuben+1
        pSphere -> pSphere1 -> pSphere2 -> pSphere3 -> pSphere4 ... pSpheren+1
    '''
    if not mc.objExists(objectName):
        return objectName
    
    res = re.search('\d+$', objectName)
    if res:
        index = string.zfill(int(res.group()) + 1, len(res.group()))
        result   = re.sub('\d+$', index, objectName)    
    else:
        result   = '%s1'%(objectName)
    
    return compileMayaObjectName(result)





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
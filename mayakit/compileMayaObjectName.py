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

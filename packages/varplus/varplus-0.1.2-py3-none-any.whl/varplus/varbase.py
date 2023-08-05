import varplus.varrules as vrule
var = list() #List to save data of variables
idx = list() #List to save index of variables in var list

#Give error message when error is catched
def giveError(msg):
    raise Exception(msg)
    pass


def checkRule(name):
    finded_data = var[idx.index(name)]
    return vrule.checkRules(finded_data)

def checkKill(name):
    finded_data = var[idx.index(name)]
    return vrule.checkKill(finded_data)

#Set(declaere) new variable
def setVariable(name=None, value=None, rule={}):
    if(name == None):
        raise Exception("'Name' value can't be None")
    else:
        var.append({'name' : name , 'value' : value, 'rule' : rule})
        idx.append(name)
        checkKill(name)
        return 0
    pass

#Get selected variable's value
def getValue(name):
    checkKill(name)
    try:
        finded_data = var[idx.index(name)]
        return finded_data['value']
    except:
        giveError("Not declared var " + name)

#Clear selected variable
def clearVariable(name):
    try:
        findex_idx = idx.index(name)
        del idx[findex_idx]
        del var[findex_idx]
    except:
        giveError("Not declared var " + name)
    return 0

#Modify selected variable's value
def modifyValue(name, value):
    var_rule = var[idx.index(name)]['rule']
    if(var_rule.get('isConst') == True):
        raise Exception(name + " is const can't modify value - varplus_dev")
    try:
        var[idx.index(name)]['value'] = value
    except:
        giveError("Not declared var " + name)
    checkKill(name)
    return 0

#Check if selected variable is declared
def isDeclared(name):
    try:
        finded_data = var[idx.index(name)]
        checkKill(name)
        return True
    except:
        return False
    pass




#This varrules.py is the file which has a rules for variables


def rule_noNone(variable):
    var_rule = variable['rule']
    if(var_rule.get('noNone') == True and variable['value'] == None):
        return False
    else:
        return True
    pass

def rule_varibaleType(variable):
    var_rule = variable['rule']
    if(str(type(variable['value'])) == "<class '" + var_rule.get('variableType') + "'>"):
        return True
    else:
        return False
    pass

def checkRules(variable):
    var_rule = variable['rule']
    if(var_rule.get('noNone') != None):
        return rule_noNone(variable)
        pass
    if (var_rule.get('variableType') != None):
        return rule_varibaleType(variable)
        pass
    else:
        return True
    pass

def checkKill(variable):
    var_rule = variable['rule']
    if(var_rule.get('noNone') != None):
        if(rule_noNone(variable) == False):
            raise Exception(variable['name'] + "'s value can't be None - varplus_dev")
        pass
    if (var_rule.get('variableType') != None):
        if (rule_varibaleType(variable) == False):
            raise Exception(variable['name'] + "'s value is not correct type - varplus_dev ")
        pass
    else:
        return True
    pass


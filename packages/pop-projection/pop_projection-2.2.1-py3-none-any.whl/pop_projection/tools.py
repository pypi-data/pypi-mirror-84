"""
Created on 2019

@author: a.teffal

"""

def init_employees_proj(employees, MAX_YEARS):
    
    #projected employees are stored in a dic with keys:
    # - data : all columns of dataframe employees passed to simulerEffectif except column id
    # - exist (0 or 1) : first initialized to 1, becomes 0 when employee deleted from population
    # - entrance (int) : year in which employee was added to population
    # - lives (list of numbers) : the element i represents the probability of living until year i
    # - deaths (list of numbers) : the element i represents the probability of dying between year i and year i+1
    # - res (list of numbers) : the element i represents the probability of resignation between year i and year i+1
    # - type (list of string) : if employee is still active at year i, then element i is 'active' otherwise 'retired'
    employees_proj = {}
    n_e = len(employees)

    
    for i in range(n_e):
        if employees["type"][i] == "active":
            employees_proj[employees["id"][i]] = {'data':dict(zip(employees.columns[1:],list(employees.iloc[i])[1:])), 'exist':1, 
                'entrance':0, 'lives':[1] + [0]*(MAX_YEARS-1), 'deaths' : [0]*MAX_YEARS, 'res':[0]*MAX_YEARS, 
                'type':['active'] + ['']*(MAX_YEARS-1), 'numbers':[employees["number"][i]] + [0]*(MAX_YEARS-1), 'spouses_number':[0]*MAX_YEARS, 'children_number':[0]*MAX_YEARS}  
        else:
            employees_proj[employees["id"][i]] = {'data':dict(zip(employees.columns[1:],list(employees.iloc[i])[1:])), 'exist':1, 
                'entrance':0, 'lives':[1] + [0]*(MAX_YEARS-1), 'deaths' : [0]*MAX_YEARS, 'res':[0]*MAX_YEARS, 
                'type':['retired']*MAX_YEARS, 'numbers':[employees["number"][i]] + [0]*(MAX_YEARS-1), 'spouses_number':[0]*MAX_YEARS, 'children_number':[0]*MAX_YEARS}
        employees_proj[employees["id"][i]]['data']['age0'] = employees["age"][i]

        # if 'number' in list(employees.columns[1:]):
        #     employees_proj[employees["id"][i]]['numbers'][0] = employees["number"][i]
        # else:
        #     employees_proj[employees["id"][i]]['numbers'][0] = 1

    

    return employees_proj

def init_spouses_proj(spouses, MAX_YEARS, employees_proj_ = None):
    
    #projected spouses are stored in a dic with keys:
    # - data : all columns of dataframe employees passed to simulerEffectif except column id
    # - exist (0 or 1) : first initialized to 1, becomes 0 when employee deleted from population
    # - entrance (int) : year in which employee was added to population
    # - lives (list of numbers) : the element i represents the probability of living until year i
    # - deaths (list of numbers) : the element i represents the probability of dying between year i and year i+1
    # - type (list of string) : if employee is still active at year i, then element i is 'active' otherwise 'retired'
    spouses_proj = {}
    n_s = len(spouses)

    for i in range(n_s):
        spouses_proj[(spouses["id"][i], spouses["rang"][i])] = {'data':dict(zip(spouses.columns[2:],list(spouses.iloc[i])[2:])), 'exist':1, 
            'entrance':0, 'lives':[1] + [0]*(MAX_YEARS-1), 'deaths' : [0]*MAX_YEARS, 'res' : [0]*MAX_YEARS,'rev' : [0]*MAX_YEARS,
            'type':[spouses["type"][i]] + ['']*(MAX_YEARS-1), 'numbers':[spouses["number"][i]] + [0]*(MAX_YEARS-1)}
        spouses_proj[(spouses["id"][i], spouses["rang"][i])]['data']['age0'] = spouses["age"][i]

        # if 'number' in list(spouses.columns[1:]):
        #     spouses_proj[(spouses["id"][i], spouses["rang"][i])]['numbers'][0] = spouses["number"][i]
        # else:
        #     spouses_proj[(spouses["id"][i], spouses["rang"][i])][0] = 1

        # set the number of spouses of the employee attached to this spouse
        if not (employees_proj_ is None):
            if spouses["type"][i] !='widow':
                employees_proj_[spouses["id"][i]]['spouses_number'][0] +=spouses["number"][i]

    return spouses_proj

def init_children_proj(children, MAX_YEARS, employees_proj_ = None):
    
    #projected spouses are stored in a dic with keys:
    # - data : all columns of dataframe employees passed to simulerEffectif except column id
    # - exist (0 or 1) : first initialized to 1, becomes 0 when employee deleted from population
    # - entrance (int) : year in which employee was added to population
    # - lives (list of numbers) : the element i represents the probability of living until year i
    # - deaths (list of numbers) : the element i represents the probability of dying between year i and year i+1
    # - type (list of string) : if employee is still active at year i, then element i is 'active' otherwise 'retired'
    children_proj = {}
    n_c = len(children)

    for i in range(n_c):
        children_proj[(children["id"][i], children["rang"][i])] = {'data':dict(zip(children.columns[2:],list(children.iloc[i])[2:])), 'exist':1, 
            'entrance':0, 'lives':[1] + [0]*(MAX_YEARS-1), 'deaths' : [0]*MAX_YEARS, 'res' : [0]*MAX_YEARS,
            'type':[children["type"][i]] + ['']*(MAX_YEARS-1), 'numbers':[children["number"][i]] + [0]*(MAX_YEARS-1)}
        children_proj[(children["id"][i], children["rang"][i])]['data']['age0'] = children["age"][i]

        # if 'number' in list(children.columns[1:]):
        #     children_proj[(children["id"][i], children["rang"][i])]['numbers'][0] = children["number"][i]
        # else:
        #     children_proj[(children["id"][i], children["rang"][i])]['numbers'][0] = 1

        # set the number of children of the employee attached to this spouse
        if not (employees_proj_ is None):
            if children["type"][i]!='widow':
                employees_proj_[children["id"][i]]['children_number'][0] +=children["number"][i]

    return children_proj
    
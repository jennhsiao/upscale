# functions for file 'opt_param'

def tup_convert(tup):
    str = ''.join(tup)
    return str

def unfold(val, min, max):
    """
    transform values normalized between 0-1 back to their regular range
    """
    unfold_list = []
    for i in val: 
        unfold_i = i*(max - min) + min
        unfold_list.append(unfold_i)        
    return unfold_list


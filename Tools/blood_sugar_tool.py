from schemas.blood_sugar_schema import BloodSugarSchema 
from langchain_core.tools import tool 
@tool('blood_sugar_level',args_schema = BloodSugarSchema)
def blood_suagr_level(blood_sugar_level,test_type) ->dict :
    ''' categorise the patient into three types Normal ,Pre-Diabetic ,Diabetic using the 
    test_type and blood_sugar_level'''
    if test_type == 'fasting' : 
        if blood_sugar_level < 100 :
            diagnosis = 'Normal'
        elif 100 <= blood_sugar_level < 125 :
            diagnosis = 'Pre-Diabetic'
        else : diagnosis = 'Diabetic'
    elif test_type == 'post_meal' :
        if blood_sugar_level < 140 :
            disgnosis = 'Normal'
        elif 140 <= blood_suagr_level < 199 :
            diagnosis = 'Pre-Diabetic'
        else : diagnosis = 'Diabetic'
    return {
        'blood_sugar_level':blood_sugar_level ,
        'test_type':test_type , 
        'diagnosis' : diagnosis
    }
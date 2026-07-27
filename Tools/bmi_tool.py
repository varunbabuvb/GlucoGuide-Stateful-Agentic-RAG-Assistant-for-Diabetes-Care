from schemas.bmi_schema import BMISchema 
from langchain_core.tools import tool 
@tool('calculate_bmi',args_schema = BMISchema)
def calculate_bmi(weight : float , height : float) ->dict :
    ''' Calculates the body mass index (BMI) and return the structured
    output containing the valur of bmi and the Category the patient belongs to'''
    height_m = height 
    bmi = weight / (height_m ** 2)
    bmi = round(bmi,2)

    if bmi < 18.5 :
        category = 'Underweight'
    elif 18.5 <= bmi < 25:
        category = 'NormalWeight'
    elif 25 <= bmi < 30 :
        category = 'OverWeight'
    else :
        category = 'Obesity'
    return {
        'bmi' : bmi ,
        'category' : category
    }

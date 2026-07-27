from pydantic import BaseModel,Field
from typing import Annotated,Literal 
class BloodSugarSchema(BaseModel):
    blood_sugar_level : Annotated[float,Field(gt = 0,description = 'blood sugar level of patient in mg/dL'),]
    test_type : Annotated[Literal['fasting','post_meal'],Field(description = '''Based on the test timings and history of food intake
    categorise the patients test_type into fasting ,post_meal 
    if the patient has not taken any calories in the past 8 hrs categorise him into fasting 
    else if he/she  has taken taken any calories in the past 2 hrs then he goes to post_meal 
    ''')]

from pydantic import BaseModel,Field
from typing import Annotated 
class BMISchema(BaseModel):
    weight : Annotated[float,Field(gt = 0,title = 'weight of the patient',description = 'weight of the patient in kg ',examples = [25,40])]
    height : Annotated[float,Field(gt = 0,title = 'height of the patient',description = 'heigt of the patient in m ',strict = True)]
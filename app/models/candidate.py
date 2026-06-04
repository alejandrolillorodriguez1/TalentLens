from pydantic import BaseModel;

# Pydantic establece la estructura que deben cumplir los datos en nuestra aplicación, de esta forma hace la validación de forma automatica en vez de tener que crear nosotros las validaciones mediante código
# https://www.datacamp.com/tutorial/pydantic?utm_cid=23781701478&utm_aid=196565213035&utm_campaign=260417_1-ps-dscia~amx-tofu~python_2-b2c_3-emea_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na&utm_loc=1005493-&utm_mtd=p-c&utm_kw=modules%20python&utm_source=google&utm_medium=paid_search&utm_content=ps-dscia~emea-en~amx~tofu~tutorial~python&gad_source=1&gad_campaignid=23781701478&gbraid=0AAAAADQ9WsHpX62Nvgq2Mu00QQCXVcY0H&gclid=CjwKCAjwxITRBhBYEiwA6mZm7Sw5chi6dkm4X9gzL-r3mES6Y5eH-7JCLVsUnEYVViPeFmfNsbHJ9xoCt6kQAvD_BwE

class Candidate(BaseModel) : 

    name : str
    skills : list[str]

import requests

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55IjoiZXhwZXJ0Y2VudHJlIiwiZmlyc3RuYW1lIjoidmFkaW0iLCJsYXN0bmFtZSI6ImtoYXJpY2hrb3YifQ.gGKZ9mBvBpAownYJg9pfzvFjM2L1PaTotnSyGTYUCkU"
base_inn_url = "https://crm-new.featureddata.com/api/v1/companies?filter.taxPayerNumber={}"


def new_CRM_check(inn):
    auth_code = f"Bearer {access_token}"
    response = requests.get(
        base_inn_url.format(inn),
        headers={
            'Authorization': auth_code
        }
    )
    result = response.json()
    if result['Data']['Total'] == 0:
        # print('Такой организации ещё нет в CRM')
        lead_exist = False
    elif result['Data']['Total'] > 0:
        # print('Такая организация уже есть в CRM')
        lead_exist = True
    else:
        # Не удалось получить данные, может наебнулось API
        lead_exist = False
    return lead_exist


print(new_CRM_check("0278128540"))

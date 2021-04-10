#from openapi_client import openapi
#from config import TINKOFF_TOKEN


#def portfolio_balance() -> int:
    #client = openapi.api_client(TINKOFF_TOKEN)
    #pf = client.portfolio.portfolio_get()

    #balance = 0
    #for i in range(len(pf.payload.positions)):
    #    balance += pf.payload.positions[i].average_position_price.value * pf.payload.positions[i].balance
    #return balance

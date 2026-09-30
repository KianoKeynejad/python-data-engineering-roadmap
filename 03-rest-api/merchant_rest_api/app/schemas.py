
from pydantic import BaseModel

# Define the structure and data types of a merchant API response
class MerchantResponse(BaseModel):
    merchant_id: str
    company_name: str
    mcc_code: int
    business_industry: str
    price_model: str
    msf_cc_percent: float
    msf_dc_dollar: float
    state: str
    postcode: str


# Test the MerchantResponse model
merchant = MerchantResponse(
    merchant_id="SP7020000018176",
    company_name="Example Business",
    mcc_code=5812,
    business_industry="Eating Places & Restaurants",
    price_model="SmartCharge",
    msf_cc_percent=0.70,
    msf_dc_dollar=0.20,
    state="NSW",
    postcode="2000"
)

print(merchant)
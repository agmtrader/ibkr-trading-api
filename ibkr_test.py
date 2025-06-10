import requests

base_url = "http://localhost:5056"
url = f"{base_url}/contracts/search"
payload = {
    "symbol": "AAPL",
    "secType": "STK",
}
response = requests.post(url, json=payload, verify=False)
contracts = response.json()
for contract in contracts:
    print("conid: ", contract.get("conid", ""))
    print("companyHeader: ", contract.get("companyHeader", ""))
    print("companyName: ", contract.get("companyName", ""))
    print("symbol: ", contract.get("symbol", ""))
    print("description: ", contract.get("description", ""))
    print("restricted: ", contract.get("restricted", ""))
    print("sections: ", contract.get("sections", ""))
    print("issuers: ", contract.get("issuers", ""))
    print("fop: ", contract.get("fop", ""))
    print("opt: ", contract.get("opt", ""))
    print("war: ", contract.get("war", ""))
    print("bondid: ", contract.get("bondid", ""))
    print("\n")

conid = "265598"
sectype = "STK"
month = "202506"
url2 = f"{base_url}/contracts/info"
payload = {
    "conid": conid,
    "sectype": sectype,
    "month": month,
}
response = requests.post(url2, json=payload, verify=False)
details = response.json()
print(details)
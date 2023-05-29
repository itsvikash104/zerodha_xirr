# Zerodha Equity XIRR calculator (Unofficial)

## Description
The script downloads the trade information and uses current value input to calculate the XIRR of the 
zerodha equity trades

## Disclamier
Do not share your zerodha `cookie` and `x-csrftoken` header values with anyone. It can allow other to make transactions on your behalf

## Usage
```bash
# please do python new environment setup before
git clone https://github.com/itsvikash104/zerodha_xirr
cd zerodha_xirr
vim console.cookie
# put the cookie value from logged in console session on browser and save
vim console.x-csrftoken
# put the x-csrftoken from logged in console session on browser and save
pip install -r requirements.txt
python xirr.py {potfolio-current-value}
```
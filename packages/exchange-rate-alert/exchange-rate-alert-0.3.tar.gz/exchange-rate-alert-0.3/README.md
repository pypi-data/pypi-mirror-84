# Exchange Rate Alert
---

Creates desktop alerts when the Transferwise exchange rates hit a target rate. Tries every five minutes.

Currently running on Windows, Linux support incoming.

---

#### Before Using

Before the module can be used the user has to create a Transferwise API token. The detailed instructions can be found here - https://api-docs.transferwise.com/#payouts-guide-api-access  

The program will try and find the access token in the following manner
 
 1. System Variable named TCR - create a system variable named TCR
 
 2. Configuration file - located at `%HOMEDRIVE%%HOMEPATH%/.tcr` on windows or `~/.tcr` on linux
                      
---

#### Usage 

Install package from pip 
- `pip install exchange-rate-alert`


Import into python script
- `from ratealert import ConversionAlert`

Call the constructor, wait for alert, profit!
- `ConversionAlert(source, target, alert_rate)`

--- 

#### Example

`from ratealert.conversionalert import ConversionAlert`

`ConversionAlert('SEK', 'INR', 8.5)`

This will create an alert when the Transferwise exchange rate crosses the alert rate. 

The rates will be checked every five minutes.

Exit the script by Ctrl+C

---

#### Change notes

0.3 - Alert on a target conversion rate
 
0.1 - Alert at specified intervals


---

#### Next steps

- Linux support
- OAuth login for Transferwise
- Quotation request on target conversion rate


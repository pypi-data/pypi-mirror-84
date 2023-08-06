Exchange Rate Alert
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

#### Installation 

Install package from pip 
- `pip install exchange-rate-alert`


#### Usage

**From Command Prompt** 

- `era --source=SEK --target=INR --alert-rate=8.5`
- `era` and respond to prompts


**As a python module** 

Import into python script
- `from ratealert import ConversionAlert`
    
Call the constructor, wait for alert, profit!
- `ConversionAlert(source, target, alert_rate)`

--- 

#### Example

    from ratealert import ConversionAlert
    ConversionAlert('SEK', 'INR', 8.5)

This will create a notification when the Transferwise exchange rate crosses the alert rate. 

The rates will be checked every five minutes.

Exit the script by Ctrl+C

---

#### Change notes

0.4 - Command line execution, input prompts

0.3 - Alert on a target conversion rate
 
0.1 - Alert at specified intervals


---

#### Next steps

- OAuth login for Transferwise
- Quotation request and transfer lock on target conversion rate
- Linux support


# Thermal-printer-V1
This is a POS app built with Django(Python) and Electron(Javascript) 

Disclaimer
Using this app on your device, means you have an intermediate level of python skill

Get Started
After cloning the repository, you install the required modules to make it work.
I recomend you create a virtual enviroment for ease of work follow

Tested on Python --version 3.6

Django/Python 
This is the server side of the application, it runs on localhost and port 8000
Feature
. Five Database Table
. Sign
. Sign Out
. Create account
. Print Reiept on the Thermal Printer (Currently unavailable due to lack of hardware)
. Generate Report to xml

Electron/Javascript
The electron app basically open the django app via ip address. This will make running
the app on a broswer irrelevant.

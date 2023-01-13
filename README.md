# sunrise-sunset-quality-via-text
Small python program that pulls data from sunsetwx.com given a location by user input and texts the user the sunrise/sunset forecast.

To use this, run the SunsetWxText.py file. 

You will need to sign up for an account with SunsetWx: https://subscriptions.sunsetwx.com/register

As of this writing, the API is free to use for personal use. 

Input the location you would like in the 'loc' variable. This will convert your location into coordinates automatically using 
geopy.geocoders and Nominatim


Finally, you will need to sign up for a Twilio account to text you. Twilio gives new users free trial credits, so this app can run free for a while until your credits run out. 
You will need to paste your Twilio SID, auth code, the Twilio provided phone number, and add your personal phone number as the authorzed number to text. 

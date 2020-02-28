# Burnham-BurnhamX

BurnhamX is a chrome extension that is built using the IndboxSDK, Gmail API, and a Django API app.

# Components

## Gadget
This holds the chrome extension that is uploaded to the Google Store. It's very empty as the app is loaded remotely from a static file

## Django
Djagno is used (but mostly just the Django Rest Framework). It connects to a sql database and interacts with CloudSQL

## Static
The actual inbox sdk code lives here. It is loaded remotely. It could be hosted on GCS, but that was not chosen at the time of development

## Deploying the Django App
In the current incarnation of the application (2/28/2020), everything is contained in the app. It was written before we knew how to use a `lib` folder and `appengine_config.py`.
Therefore, all that is needed to deploy is to run `gcloud app deploy --project burnham-x`
As of 2/28/2020, there is a SOW to perform a django upgrade and python upgrade. 

## Deploying InboxSDK code
Just like the section above, copy and paste the code into the `static` directory. The gadget will then pull from that directly.

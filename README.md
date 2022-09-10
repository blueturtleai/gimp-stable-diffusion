# gimp-stablediffusion

This repository includes a GIMP plugin for communication with a stablediffusion server and a Google colab for the server.

## Overview

The server exposes a REST API, which is used by the GIMP plugin to communicate with the server. Currently the plugin offers the possibility to use img2img. img2img means, that you create an image in GIMP, which is then used as the base for the image creation in stablediffusion.

## Installation
### GIMP

The plugin is tested in GIMP 2.10 and runs most likely in all 2.* releases.

1. Start GIMP and open the preferences dialog via edit/preferences and scroll down to "folders". Expand "folders" and click on "plug-ins". Select the folder which includes your username and copy the path. 

2. Open the file explorer, navigate to this directory and copy the file "stable.py" from the repository into this directory.

3. Restart GIMP. You should now see the new menu "AI". If you don't see this, something went wrong. The menu has one item "Stable img2img". This item can't currently be selected. This only works, when you opened an image before. More about this, when the server is running.

### Stablediffusion server
#### Prerequisits
You need a Google account, an account on ngrok.com and on huggingface.co. Google is needed for running a colab server, ngrok for exposing an external IP and huggingface for downloading the model file. Details follow below.

#### Model file
The model file includes all the data which is needed for stablediffusion to generate the images.
1. Create an account on https://huggingface.co. 
2. Nagivate here https://huggingface.co/CompVis/stable-diffusion-v-1-4-original and agree to the shown agreement. 
3. Download the model file from here: https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt. 
4. Login into your Google account and upload the file to your Google drive.

#### Ngrok Authtoken
Ngrok offers a free service to access an server via a public IP.
1. Create an account on https://ngrok.com
2. Click on the left side menu "Your Authtoken" and copy the token.

#### Colab server
1. Click on ??? to open the notebook.
2. Click on "connect" and wait until the status changes to "connected".
3. Click on the arrow left to "Check CPU" and wait until you see a checkmark on the left.
4. Click on the arrow left to "Mount Google drive". Confirm the mount in the dialog which pops up. When the checkmark is shown proceed.
5. Click on the arrow left to "Installation" and wait until finished.
6. Click on the folder symbol on the left. Open the "gdrive/MyDrive" folder and navigate to the model file from huggingface, which you uploaded before. Select the model file, click on the three dots and select "copy path". Close the file explorer via the cross.
7. Copy the copied path into the input field "checkpoint_model_file" in the "Load Model" section and click on the arrow on the left. Wait until finished.
8. Click on the arrow left to "Enter ngrok Authtoken". Copy the authtoken into the input field where the cursor blinks and press enter. Wait until finished.
9. Click on the arrow left to "Waiting for GIMP requests". The arrow on the left won't stop spinning in this case. If everything is okay, you should something like this:
```
 * Serving Flask app "__main__" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off

INFO:werkzeug: * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

 * Running on http://***.ngrok.io
 * Traffic stats available on http://127.0.0.1:4040
 ```

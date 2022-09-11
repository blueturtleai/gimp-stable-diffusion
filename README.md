# gimp-stable-diffusion

This repository includes a GIMP plugin for communication with a stablediffusion server and a Google colab notebook for running the server.

## Overview

The server exposes a REST API, which is used by the GIMP plugin to communicate with the server. Currently the plugin offers the possibility to use img2img. img2img means, that you create an image in GIMP, which is then used as the base for the image creation in stablediffusion.

## Installation
### GIMP

The plugin is tested in GIMP 2.10 and runs most likely in all 2.* releases.

1. Start GIMP and open the preferences dialog via edit/preferences and scroll down to "folders". Expand "folders" and click on "plug-ins". Select the folder which includes your username and copy the path. 

2. Open the file explorer, navigate to this directory and copy the file "gimp-stable-diffusion.py" from the repository into this directory.

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
1. Open the link using the "new tab" option. [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blueturtleai/gimp-stable-diffusion/blob/main/gimp-stable-diffusion.ipynb)

2. Click on "connect" and wait until the status changes to "connected".

3. Click on the arrow left to "Check CPU" and wait until you see a checkmark on the left.

4. Click on the arrow left to "Mount Google drive". Confirm the mount in the dialog which pops up. When the checkmark is shown proceed.

5. Click on the arrow left to "Installation" and wait until finished.

6. Click on the folder symbol on the left. Open the "gdrive/MyDrive" folder and navigate to the model file from huggingface, which you uploaded before. Select the model file, click on the three dots and select "copy path". Close the file explorer via the cross.

7. Copy the copied path into the input field "checkpoint_model_file" in the "Load Model" section and click on the arrow on the left. Wait until finished.

8. Click on the arrow left to "Enter ngrok Authtoken". Copy the authtoken into the input field where the cursor blinks and press enter. Wait until finished.

9. Click on the arrow left to "Waiting for GIMP requests". The arrow on the left won't stop spinning in this case. If everything is okay, you should see something like this:
```
 * Serving Flask app "__main__" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off

INFO:werkzeug: * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

 * Running on http://*.ngrok.io <- copy this URL
 * Traffic stats available on http://127.0.0.1:4040
 ```
 
 10. Copy the URL from above, which reads like ```http://*.ngrok.io```. This is the URL, which is used for the communication between the GIMP plugin and the server. 

## Generate images
Now we are ready for generationg images.

1. Start GIMP and open an image or create a new one. The image should have the dimensions 512x512. This is a limitation, which will be removed soon.

2. Select the new AI/Stable im2img menu item. A dialog will open, where you can enter the details for the image generation.
   - **Init Strength:** How much the AI should take the init image into account. The higher the value, the more will the generated image look like the init image. 0.3 is a good value to use.

   - **Prompt Strength:** How much the AI should follow the prompt. The higher the value, the more the AI will generate an image which looks like your prompt. 7.5 is a good value to use.

   - **Steps:** How many steps the AI should use to generate the image. The higher the value, the more the AI will work on details. But it also means, the longer the generation takes and the more the GPU is used. 50 is a good value to use.

   - **Prompt:** How the generated image should look like.

   - **Backend root URL:** Insert the ngrok.io URL you copied from the server. It has to end by an "/". The URL should look like this ```http://*.ngrok.io/```

3. Click on the OK button. The values you inserted into the dialog and the init image will be transmitted to the server, which starts now generating the image. On the colab browser tab you can see what's going on. When the image has been generated successfully, it will be shown as a new image in GIMP.

## Hints
### Colab server
The ressources on the colab server are limited. So, it's a good idea to stop it when you don't use it. 
   - If you only don't use it for a short time, just stop the last step (Waiting for GIMP requests). To do so, click on the spinning circle on the left. If you want to use it again, just execute the last step again. The URL for accessing the server will be different, so copy it again.

   - If you don't use if for a longer time, the best is to release all ressources. To do so, select "Runtime/Disconnect and delete runtime". If you want to use it again, you have to start again at step 1.

If you generated several images, the ressources of the colab server will be exhausted at some point. This happens pretty quickly, if you use the free plan. It takes longer for the pro plans. If this happens, an error will occur and you have to wait for some time until you can generate images again.

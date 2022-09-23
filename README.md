# gimp-stable-diffusion

This repository includes a GIMP plugin for communication with a stable-diffusion server and a Google colab notebook for running the server.

Please check HISTORY.md for the latest changes. 

Click here [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opencoca/gimp-stable-diffusion/blob/main/gimp-stable-diffusion.ipynb) to open the notebook, if you already read the setup instructions below.

## Overview

The server exposes a REST API, which is used by the GIMP plugin to communicate with the server. Currently the plugin offers the possibility to use img2img. img2img means, that you create an image in GIMP, which is then used as the base for the image creation in stable-diffusion.



https://user-images.githubusercontent.com/113246030/190710535-9fb23f88-954f-4f73-afea-1475c8690754.MOV

## Manual
It doesn't exist a separate manual. Please check the following sections for installation and image generation for a detailled explanation.

## Installation
### Download files

To download the files of this repository click on "Code" and select "Download ZIP". In the ZIP you will find the file "gimp-stable-diffusion.py". This is the code for the GIMP plugin. You don't need the other files in the ZIP.

### GIMP

The plugin is tested in GIMP 2.10 and runs most likely in all 2.* releases. Excluded is 2.99, because it's already Python 3 based.

1. Start GIMP and open the preferences dialog via edit/preferences and scroll down to "folders". Expand "folders" and click on "plug-ins". Select the folder which includes your username and copy the path. 

2. Open the file explorer, navigate to this directory and copy the file "gimp-stable-diffusion.py" from the repository into this directory. If you are on MacOS or Linux, chahge the file permissions to 755.

3. Restart GIMP. You should now see the new menu "AI". If you don't see this, something went wrong. The menu has one item "Stable img2img". This item can't currently be selected. This only works, when you opened an image before. More about this, when the server is running.

### Stable-Diffusion server
#### Prerequisites
You need a Google account, an account on ngrok.com and on huggingface.co. Google is needed for running a colab server, ngrok for exposing an external IP and huggingface for downloading the model file. Details follow below.

#### Model file
The model file includes all the data which is needed for stable-diffusion to generate the images.
1. Create an account on https://huggingface.co. 

2. Nagivate here https://huggingface.co/CompVis/stable-diffusion-v-1-4-original and agree to the shown agreement. 

3. Download the model file from here: https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt (4 GB). 

4. Login into your Google account and upload the file to your Google drive.

#### Ngrok Authtoken
Ngrok offers a free service to access an server via a public IP.
1. Create an account on https://ngrok.com

2. Click on the left side menu "Your Authtoken" and copy the token.

#### Colab server
1. Open this link in a new tab [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blueturtleai/gimp-stable-diffusion/blob/main/gimp-stable-diffusion.ipynb)

2. Click on "connect" and wait until the status changes to "connected".

3. Click on the arrow left to "NVIDIA GPU" and wait until you see a checkmark on the left.

4. Click on the arrow left to "Mount Google Drive" and confirm the mount. Wait until you see a checkmark on the left.

5. Click on the folder symbol on the left. Open the "gdrive/MyDrive" folder and navigate to the model file from huggingface, which you uploaded before. Select the model file, click on the three dots and select "copy path". Close the file explorer via the cross.

5. Insert the copied path into the field "models_path_gdrive" at the step "Set Model Path". Remove the filename and the last "/" at the end. The path should now look for example like this ```/content/drive/MyDrive/SD/models```. Click on the arrow at the left and wait until finished.

6. Execute the step "Setup Environment".

7. Execute the step "Python Definitions".

8. Execute the step "Select and Load Model". In the selector for the model files there is currently only one entry. When v1.5 has been released, this model will be added to the selector.

9. Click on the arrow left to "Enter ngrok Authtoken". Copy the authtoken into the input field where the cursor blinks and press enter. Wait until finished.

10. Click on the arrow left to "Waiting for GIMP requests". The arrow on the left won't stop spinning in this case. If everything is okay, you should see something like this:
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
 Sometimes an error message is displayed instead. Please check "Hints/Colab Server/No external IP" below for a solution.
 
 10. Copy the URL from above, which reads like ```http://*.ngrok.io```. This is the URL, which is used for the communication between the GIMP plugin and the server. 

## Generate images
Now we are ready for generating images.

1. Start GIMP and open an image or create a new one. It is recommended, that the image size is not larger than 512x512 as the model has been trained on this size. If you want to have larger images, use an external upscaler instead. The generated image will have the dimensions of the init image. But it may be resized to make sure, that the dimensions are a multiple of 64. The larger the image, the longer it takes to generate it and the more GPU ressources and RAM is used. If it is too larger, you will run out of memory.

2. Select the new AI/Stable im2img menu item. A dialog will open, where you can enter the details for the image generation.

   - **Inpainting:** If you want to inpaint. Please read the section "Inpainting" below for an explanation how inpainting works.
   
   - **Inpainting/Mask Brightness:** For future use. For now leave the value just unchanged.
   
   - **Inpainting/Mask Contrast:** For future use. For now leave the value just unchanged.
    
   - **Init Strength:** How much the AI should take the init image into account. The higher the value, the more will the generated image look like the init image. 0.3 is a good value to use.

   - **Prompt Strength:** How much the AI should follow the prompt. The higher the value, the more the AI will generate an image which looks like your prompt. 7.5 is a good value to use.

   - **Steps:** How many steps the AI should use to generate the image. The higher the value, the more the AI will work on details. But it also means, the longer the generation takes and the more the GPU is used. 50 is a good value to use.

   - **Seed:** This parameter is optional. If it is empty, a random seed will be generated om the server. If you use a seed, the same image is generated again in the case the same parameters for init strength, steps, etc. are used. A slightly different image will be generated, if the parameters are modified. You find the seed in an additional layer at the top left. 

   - **Number of images:** Number of images, which are created in one run. The more images you create, the more server ressources will be used and the longer you have to wait until the generated images are diaplayed in GIMP.
   
   - **Prompt:** How the generated image should look like.

   - **Backend root URL:** Insert the ngrok.io URL you copied from the server. It has to end by an "/". The URL should look like this ```http://*.ngrok.io/```

3. Click on the OK button. The values you inserted into the dialog and the init image will be transmitted to the server, which starts now generating the image. On the colab browser tab you can see what's going on. When the image has been generated successfully, it will be shown as a new image in GIMP. The used seed is shown at the top lift in an additional layer.

### Inpainting
Inpainting is replacing a part of an existing image. For example you don't like the face on an image, you can replace it. Inpainting is currently still in experimental stage. So, please don't expect perfect results. The experimental stage is caused by the server side and not by GIMP.

For inpainting it's necessary to prepare the input image because the AI needs to know which part you want to replace. For this purpose you replace this image part by transparency. To do so, open the init image in GIMP and select "Layer/Transparency/Add alpha channel". Select now the part of the image which should be replaced and delete it. You can also use the eraser tool. 

For the prompt you use now a description of the new image. For example the image shows currently "a little girl running over a meadow with a balloon" and you want to replace the balloon by a parachute. You just write now "a little girl running over a meadow with a parachute".

## Hints
### Colab server
#### Ressource limits
The ressources on the colab server are limited. So, it's a good idea to stop it when you don't use it. 
   - If you only don't use it for a short time, just stop the last step (Waiting for GIMP requests). To do so, click on the spinning circle on the left. If you want to use it again, just execute the last step again. The URL for accessing the server will be different, so copy it again.

   - If you don't use if for a longer time, the best is to release all ressources. To do so, select "Runtime/Disconnect and delete runtime". If you want to use it again, you have to start again at step 1.

If you generated several images, the ressources of the colab server will be exhausted at some point. This happens pretty quickly, if you use the free plan. It takes longer for the pro plans. If this happens, an error will occur and you have to wait for some time until you can generate images again.

#### No external IP
When you start the last step "Waiting for GIMP requests", sometimes an error message is displayed instead of the URL:

 ```
 INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000/
INFO:werkzeug:Press CTRL+C to quit
Exception in thread Thread-12:
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 926, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 1177, in run
    self.function(*self.args, **self.kwargs)
  File "/usr/local/lib/python3.7/dist-packages/flask_ngrok.py", line 70, in start_ngrok
    ngrok_address = _run_ngrok()
  File "/usr/local/lib/python3.7/dist-packages/flask_ngrok.py", line 38, in _run_ngrok
    tunnel_url = j['tunnels'][0]['public_url']  # Do the parsing of the get
IndexError: list index out of range
```

If this is the case, stop and restart the step again.

## FAQ

**Will GIMP 3 be supported?** 
Yes, the plugin will be ported to GIMP 3.

**Does it run locally?** The honest answer is: I don't know. I don't have a local GPU, so I can't try it. But I'm pretty sure, there are experts out there who will try it and make a local version available, if it's possible to run it locally.

**Will In-/Out-Painting be supported?** I first need to check the details and see what's possible. So, unfortunately I can't promise it currently.

**Can the official stable-diffusion API be used?** Unfortunately, this is currently not possible. The reason is, that this API currently can only be accessed via gRPC and it's not possible to use this protocol in a GIMP plugin. As soon as the API is available as a REST API, it will be possible to port the plugin.

**How do I report an error or request a new feature?** Please open a new issue in this repository.



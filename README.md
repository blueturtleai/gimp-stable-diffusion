# gimp-stable-diffusion

This repository includes a GIMP plugin for communication with a stable-diffusion server and a Google colab notebook for running the server.

Please check HISTORY.md for the latest changes. 

Click here [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blueturtleai/gimp-stable-diffusion/blob/main/gimp-stable-diffusion.ipynb) to open the notebook, if you already read the setup instructions below.

## Overview

The server exposes a REST API, which is used by the GIMP plugin to communicate with the server. Currently the plugin offers the possibility to use img2img. img2img means, that you create an image in GIMP, which is then used as the base for the image creation in stable-diffusion. It also supports inpainting for the case you want to change parts of an existing image.



https://user-images.githubusercontent.com/113246030/190710535-9fb23f88-954f-4f73-afea-1475c8690754.MOV

## Manual
It doesn't exist a separate manual. Please check the following sections for installation and image generation for a detailed explanation.

## Installation
### Download files

To download the files of this repository click on "Code" and select "Download ZIP". In the ZIP you will find the file "gimp-stable-diffusion.py". This is the code for the GIMP plugin. You don't need the other files in the ZIP.

### GIMP

The plugin is tested in GIMP 2.10 and runs most likely in all 2.* releases. Excluded is 2.99, because it's already Python 3 based.

1. Start GIMP and open the preferences dialog via edit/preferences and scroll down to "folders". Expand "folders" and click on "plug-ins". Select the folder which includes your username and copy the path. 

2. Open the file explorer, navigate to this directory and copy the file "gimp-stable-diffusion.py" from the repository into this directory. If you are on MacOS or Linux, change the file permissions to 755.

3. Restart GIMP. You should now see the new menu "AI". If you don't see this, something went wrong. Please check in this case "Troubleshooting/GIMP" for possible solutions. The menu has one item "Stable img2img". This item can't currently be selected. This only works, when you opened an image before. More about this, when the server is running.

### Stable-Diffusion server
#### Prerequisites
You need a Google account and on huggingface.co. Google is needed for running a colab server and huggingface for downloading the model file. Details follow below.

#### Model file
The model file includes all the data which is needed for stable-diffusion to generate the images.
1. Create an account on https://huggingface.co. 

2. Nagivate here https://huggingface.co/CompVis/stable-diffusion-v-1-4-original and agree to the shown agreement. 

3. Download the model file from here: https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt (4 GB). 

4. Login into your Google account and upload the file to your Google drive. Please use the original filename.

#### Colab server
1. Open this link in a new tab [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blueturtleai/gimp-stable-diffusion/blob/main/gimp-stable-diffusion.ipynb)

2. Click on "connect" and wait until the status changes to "connected".

3. Click on the arrow left to "NVIDIA GPU" and wait until you see a checkmark on the left.

4. Click on the arrow left to "Mount Google Drive" and confirm the mount. Wait until you see a checkmark on the left.

5. Click on the folder symbol on the left. Open the "drive/MyDrive" folder and navigate to the model file from huggingface, which you uploaded before. Select the model file, click on the three dots and select "copy path". Close the file explorer via the cross.

6. Insert the copied path into the field "models_path_gdrive" at the step "Set Model Path". Remove the filename and the last "/" at the end. The path should now look for example like this ```/content/drive/MyDrive/SD/models```. Click on the arrow at the left and wait until finished.

7. Execute the step "Setup Environment".

8. Execute the step "Python Definitions".

9. Execute the step "Select and Load Model". In the selector for the model files there is currently only one entry. When v1.5 has been released, this model will be added to the selector.

10. Click on the arrow left to "Waiting for GIMP requests". The arrow on the left won't stop spinning in this case. If everything is okay, you should see something like this:
```
 * Serving Flask app "__main__" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off

INFO:werkzeug: * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

 * Running on https://*.trycloudflare.com <- copy this URL
 * Traffic stats available on http://127.0.0.1:4040
 ```
 
12. Copy the URL from above, which reads like ```https://*.trycloudflare.com```. This is the URL, which is used for the communication between the GIMP plugin and the server. 

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

   - **Seed:** This parameter is optional. If it is empty, a random seed will be generated on the server. If you use a seed, the same image is generated again in the case the same parameters for init strength, steps, etc. are used. A slightly different image will be generated, if the parameters are modified. You find the seed in an additional layer at the top left. 

   - **Number of images:** Number of images, which are created in one run. The more images you create, the more server ressources will be used and the longer you have to wait until the generated images are displayed in GIMP.
   
   - **Prompt:** How the generated image should look like.

   - **Backend root URL:** Insert the trycloudflare.com URL you copied from the server. The URL should look like this ```https://*.trycloudflare.com```.

3. Click on the OK button. The values you inserted into the dialog and the init image will be transmitted to the server, which starts now generating the image. On the colab browser tab you can see what's going on. When the image has been generated successfully, it will be shown as a new image in GIMP. The used seed is shown at the top left in an additional layer.

### Inpainting
Inpainting means replacing a part of an existing image. For example if you don't like the face on an image, you can replace it. **Inpainting is currently still in experimental stage. So, please don't expect perfect results.** The experimental stage is caused by the server side and not by GIMP.

For inpainting it's necessary to prepare the input image because the AI needs to know which part you want to replace. For this purpose you replace this image part by transparency. To do so, open the init image in GIMP and select "Layer/Transparency/Add alpha channel". Select now the part of the image which should be replaced and delete it. You can also use the eraser tool. 

For the prompt you use now a description of the new image. For example the image shows currently "a little girl running over a meadow with a balloon" and you want to replace the balloon by a parachute. You just write now "a little girl running over a meadow with a parachute".

## Troubleshooting
### GIMP
#### AI menu is not shown
##### Linux
   - If you get this error ```gimp: LibGimpBase-WARNING: gimp: gimp_wire_read(): error```, it's very likely, that you have a GIMP version installed, which doesn't include Python. Check, if you have got the menu "Filters > Python-Fu > Console". If it is missing, please install GIMP from here: https://flathub.org/apps/details/org.gimp.GIMP.

##### macOS
   - Please double check, if the permissions of the plugin py file are set to 755. It seems, that changing permissions doesn't work via the file manager. Please open a terminal, cd to the plugins directory and run "chmod ugo+x *py".
   
##### macOS/Linux
   - Open a terminal an try to run the plugin py file manually via ```python <path-to-plugin-folder>/gimp-stable-diffusion.py```. You should see the error message, that "gimpfu" is unknown. Make sure, that you are running Python 2, as this version is used by GIMP. If other errors occur, please reinstall GIMP.

### Colab server
#### Ressource limits
The ressources on the colab server are limited. So, it's a good idea to stop it when you don't use it. 
   - If you only don't use it for a short time, just stop the last step (Waiting for GIMP requests). To do so, click on the spinning circle on the left. If you want to use it again, just execute the last step again. The URL for accessing the server will be different, so copy it again.

   - If you don't use if for a longer time, the best is to release all ressources. To do so, select "Runtime/Disconnect and delete runtime". If you want to use it again, you have to start again at step 1.

If you generated several images, the ressources of the colab server will be exhausted at some point. This happens pretty quickly, if you use the free plan. It takes longer for the pro plans. If this happens, an error will occur and you have to wait for some time until you can generate images again.

## FAQ

**Will GIMP 3 be supported?** 
Yes, the plugin will be ported to GIMP 3.

**Does it run locally?** According to Google it should be possible to run the notebook locally. As I don't have a local GPU, I can't try it myself. If you give it a try, I would be happy to know, if it really works.

**Will Out-Painting be supported?** I first need to check the details and see what's possible. So, unfortunately I can't promise it currently.

**Can the official stable-diffusion API be used?** Unfortunately, this is currently not possible. The reason is, that this API currently can only be accessed via gRPC and it's not possible to use this protocol in a GIMP plugin. As soon as the API is available as a REST API, it will be possible to port the plugin.

**How do I report an error or request a new feature?** Please open a new issue in this repository.



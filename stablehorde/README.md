# gimp-stable-diffusion-horde

This repository includes a GIMP plugin for communication with [stablehorde](https://stablehorde.net). Stablehorde is a cluster of stable-diffusion servers run by volunteers. You can create stable-diffusion images for free without running a colab notebook or a local server. Please check the section "Limitations" to better understand where the limits are.

Please check HISTORY.md for the latest changes. 

## Installation
### Download files

To download the files of this repository click on "Code" and select "Download ZIP". In the ZIP you will find the file "gimp-stable-diffusion-horde.py" in the subfolder "stablehorde". This is the code for the GIMP plugin. You don't need the other files in the ZIP.

### GIMP

The plugin is tested in GIMP 2.10 and runs most likely in all 2.* releases. Excluded is 2.99, because it's already Python 3 based.

1. Start GIMP and open the preferences dialog via "edit/preferences" and scroll down to "folders". Expand "folders" and click on "plug-ins". Select the folder which includes your username and copy the path. 

2. Open the file explorer, navigate to this directory and copy the file "gimp-stable-diffusion.py" from the repository into this directory. If you are on MacOS or Linux, change the file permissions to 755.

3. Restart GIMP. You should now see the new menu "AI". If you don't see this, something went wrong. Please check in this case "Troubleshooting/GIMP" for possible solutions. The menu has one item "Stablehorde text2img". This item can't currently be selected. This only works, when you opened an image before. More about this below.

## Generate images
Now we are ready for generating images.

1. Start GIMP and open any image or create a new one. The only purpose of the image is, that the menuitem for generating the images will be enabled.

2. Select the new AI/Stablehorde text2img menu item. A dialog will open, where you can enter the details for the image generation.

   - **Prompt Strength:** How much the AI should follow the prompt. The higher the value, the more the AI will generate an image which looks like your prompt. 7.5 is a good value to use.

   - **Steps:** How many steps the AI should use to generate the image. The higher the value, the more the AI will work on details. But it also means, the longer the generation takes and the more the GPU is used. 50 is a good value to use.

   - **Seed:** This parameter is optional. If it is empty, a random seed will be generated on the server. If you use a seed, the same image is generated again in the case the same parameters for init strength, steps, etc. are used. A slightly different image will be generated, if the parameters are modified. You find the seed in an additional layer at the top left. 

   - **Prompt:** How the generated image should look like.

   - **API key:** This parameter is optional. If you don't enter an API key, you run the image generation as anonymous. The downside is, that you will have then the lowest priority in the generation queue. For that reason it is recommended registering for free on [stablehorde](https://stablehorde.net) and getting an API key.

   - **Max Wait:** The maximum time in minutes you want to wait until image generation is finished. When the max time is reached, a timeout happens and the generation request is stopped.

3. Click on the OK button. The values you inserted into the dialog will be transmitted to the server, which dispatches the request now to one of the stable-diffusion servers in the cluster. Your generation request is added to queue. You can see the queue position and the remaining wait time in the status bar of the dialog. When the image has been generated successfully, it will be shown as a new image in GIMP. The used seed is shown at the top left in an additional layer.

## Limitations
   - **Stability:** Stablehorde is still pretty new and under heavy development. So, it's not unlikely, that the servers are not available for some time or unexpected errors occur.

   - **Image size:** Currently only 512x512 is possible. In general stablehorde can also generate larger images, but not all servers in the cluster are able to do this. To make sure, that your images are generated as fast as possible, the plugin currently generates only 512x512. As soon as there are more servers in the cluster, which support larger images, it will be possible to generate larger sizes.

   - **Generation speed:** Stablehorde is a cluster of stable-diffusion servers run by volunteers. The generation speed depends on how many servers are in the cluster, which hardware they use and how many others want to generate with stablehorde. The upside is, that stablehorde is free to use, the downside that the generation speed is unpredictable.

   - **Privacy:** The privacy stablehorde offers is similar to generating in a public discord channel. So, please assume, that neither your prompts nor your generated images are private.
   
   - **Features:** Currently only text2img is available. As soon as stablehorde supports img2img and in-/out-painting, this will be available in the plugin too.

## Troubleshooting
### GIMP
#### AI menu is not shown
##### Linux
   - If you get this error ```gimp: LibGimpBase-WARNING: gimp: gimp_wire_read(): error```, it's very likely, that you have a GIMP version installed, which doesn't include Python. Check, if you have got the menu "Filters > Python-Fu > Console". If it is missing, please install GIMP from here: https://flathub.org/apps/details/org.gimp.GIMP.
  
  - Please try https://flathub.org/apps/details/org.gimp.GIMP if you have got any other problems.

##### macOS
   - Please double check, if the permissions of the plugin py file are set to 755. It seems, that changing permissions doesn't work via the file manager. Please open a terminal, cd to the plugins directory and run "chmod ugo+x *py".
   
##### macOS/Linux
   - Open a terminal an try to run the plugin py file manually via ```python <path-to-plugin-folder>/gimp-stable-diffusion.py```. You should see the error message, that "gimpfu" is unknown. Make sure, that you are running Python 2, as this version is used by GIMP. If other errors occur, please reinstall GIMP.

## FAQ

**Will GIMP 3 be supported?** Yes, the plugin will be ported to GIMP 3.

**Will Img2img, In- and Out-Painting be supported?** Very likely everyhing will be supported. This depends on which features the stablehorde cluster supports.

**How do I report an error or request a new feature?** Please open a new issue in this repository.



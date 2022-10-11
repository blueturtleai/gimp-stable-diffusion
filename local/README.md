# gimp-stable-diffusion-local

This repository includes a GIMP plugin for communication with a locally installed stable-diffusion server. Linux, macOS and Windows 11 (WSL2) are supported. Please check the section "Limitations" to better understand where the limits are.

Please check HISTORY.md for the latest changes. 

## Installation
### Download files

To download the files of this repository click on "Code" and select "Download ZIP". In the ZIP you will find the file "gimp-stable-diffusion-local.py" in the subfolder "local". This is the code for the GIMP plugin. You don't need the other files in the ZIP.

### GIMP

The plugin is tested in GIMP 2.10 and runs most likely in all 2.* releases. Excluded is 2.99, because it's already Python 3 based.

1. Start GIMP and open the preferences dialog via "edit/preferences" and scroll down to "folders". Expand "folders" and click on "plug-ins". Select the folder which includes your username and copy the path. 

2. Open the file explorer, navigate to this directory and copy the file "gimp-stable-diffusion.py" from the repository into this directory. If you are on MacOS or Linux, change the file permissions to 755.

3. Restart GIMP. You should now see the new menu "AI". If you don't see this, something went wrong. Please check in this case "Troubleshooting/GIMP" for possible solutions. The menu has one item "Stablehorde text2img". This item can't currently be selected. This only works, when you opened an image before. More about this below.

### Stable-Diffusion server
#### Prerequisites
You need an account on huggingface.co for downloading the model file. If you want to run on Windows 11, WSL2 needs to be prepared before. Details follow below. 

#### Model file
The model file includes all the data which is needed for stable-diffusion to generate the images.
1. Create an account on https://huggingface.co. 

2. Nagivate here https://huggingface.co/CompVis/stable-diffusion-v-1-4-original and agree to the shown agreement. 

3. Go to "Settings/Access Tokens" on the left side.

4. Click on "New Token", enter a name, select "Read" as role, click on create and copy the token.

#### Local server
If you want to run the server on Windows 11, WSL2 needs to be prepared before. Please follow [these instructions](https://github.com/blueturtleai/cog/blob/main/docs/wsl2/wsl2.md) until after you reach executing "wsl.exe" in 7. Afterwards please start with 2. from the instructions below, as Docker is already installed.

**1. Install and start docker**

Please don't execute these commands, if you are running on Windows 11. Jump directly to 2.

```
sudo yum update -y
sudo yum -y install docker
sudo service docker start
sudo usermod -aG docker ${USER}
```
  Log off and log in again.

**2. Install cog and cog-stable-diffusion**
```
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/download/v0.4.4/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog
sudo yum install git -y
git clone https://github.com/blueturtleai/cog-stable-diffusion
cd cog-stable-diffusion
```

**3. Install stable-diffusion server**
```
cog run script/download-weights <your huggingface token>
sudo chown -R $USER .
```

**4. Create docker image and start stable-diffusion server**
```
cog build -t stable-diffusion
docker run -d -p 5000:5000 --gpus all stable-diffusion
```

**5. Test stable-diffusion server**

Wait a minute after server start.
```
curl http://localhost:5000/predictions -X POST \
-H 'Content-Type: application/json' \
-d '{"input": {"prompt": "A beautiful day, digital painting"}}'
```
If the test was successful, the generated image will be shown as a base64 encoded very long string.

**Stop stable-diffusion server**

If you are done generating images, you can stop the server that way.

Get the container name.
```
docker ps -q
```
Stop the container.
```
docker stop <container name>
```

## Generate images
Now we are ready for generating images.

1. Start GIMP and open any image or create a new one. If you want to use img2img, open the init image.

2. Select the new "AI/Stable Local" menu item. A dialog will open, where you can enter the details for the image generation.

   - **Init Image:** If you want to use an init image.

   - **Init Strength:** How much the AI should take the init image into account. The higher the value, the more will the generated image look like the init image. 0.3 is a good value to use.
   
   - **Prompt Strength:** How much the AI should follow the prompt. The higher the value, the more the AI will generate an image which looks like your prompt. 7.5 is a good value to use.

   - **Steps:** How many steps the AI should use to generate the image. The higher the value, the more the AI will work on details. But it also means, the longer the generation takes and the more the GPU is used. 50 is a good value to use.

   - **Seed:** This parameter is optional. If it is empty, a random seed will be generated on the server. If you use a seed, the same image is generated again in the case the same parameters for init strength, steps, etc. are used. A slightly different image will be generated, if the parameters are modified. You find the seed in an additional layer at the top left. 

   - **Prompt:** How the generated image should look like.

   - **Backend root URL:** Insert the URL of your local server. If you used the instructions from above, the URL should look like this ```http://localhost:5000```.

3. Click on the OK button. The values you inserted into the dialog will be transmitted to the server. When the image has been generated successfully, it will be shown as a new image in GIMP. The used seed is shown at the top left in an additional layer.

## Limitations
   - **Testing:** The local server runs on Linux, macOS and Windows 11. Due to limited availability, it has only been tested on Linux. If you run in any problems on macOS or Windows 11, please open an issue.

   - **Inpainting:** Currently inpainting isn't available, as this needs some further testing. If the test was successful, it will be made available.

   - **NSFW:** The server doesn't support NSFW (Not Safe For Work) images. If the server generates a NSFW image, an error is displayed in GIMP.

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

**Will Out-Painting be supported?** This depends on which features the cog stable-diffusion server will support in the future.

**How do I report an error or request a new feature?** Please open a new issue in this repository.



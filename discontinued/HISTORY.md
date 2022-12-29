# History
## GIMP Plugin
### 1.2.0
#### Changes
- Now text2img is supported.
- The dialog has been optimized.

### 1.1.2
#### Changes
- Exception handling further improved

### 1.1.1
#### Changes
- Data is now transferred to the server using https

### 1.1.0
#### Changes
- Inpainting is now supported

### 1.0.2
#### Changes
- **Image count**: It is now possible to create up to 4 images in one run

- **Seed**: Can now be blank if not used (before -1)

- **Backend URL**: Needs no longer to end with "/"

- **Exception handling**: Has been improved

### 1.0.1
#### CHANGES
- **API**: Data is now transferred as JSON. It is checked, if the API version of the client and the server matches. If mismatch, user is requested to update plugin and/or server. 

- **Seed**: The seed of the generated image is now displayed in an additional layer. It can be passed to the server to generate the same image again. This only works, if the same parameters (init strength, number of steps, etc) are used.

### 1.0.0
Initial version

## Stable-Diffusion server
### 1.3.0
Changes
- Now text2img is supported.

### 1.2.1
#### Changes
- Stable-Diffusion Model v1.5 is now supported.

### 1.2.0
#### Changes
- It's no longer necessary to upload model files yourself to your Google drive. If a model file is missing, it is automatically downloaded from Huggingface. A Huggingface account and acceptance of the terms of service is still needed.

### 1.1.2
#### Changes
- Instead of ngrok now cloudflare is used as the tunnel provider. The switch is done because several users reported problems. Additional benefit is, that it's no longer necessary to register on ngrok and enter the authkey. Thanks for suggesting this @opencoca.

### 1.1.1
#### Changes
- Mounting Google drive and setting model path are now two separated steps

### 1.1.0
#### Changes
- The notebook is now based on the deforum notebook (before pharmapsychotic)
- Inpainting is now supported

### 1.0.3
#### Changes
- **Image count**: It is now possible to create up to 4 images in one run

### 1.0.2
#### Changes
- **API**: Data is now transferred in JSON. It is checked, if API version of the client and server matches. If mismatch, code 405 is returned.

- **Seed**: If a seed != -1 is transferred to the server, this seed is used for image generation.

### 1.0.1
#### Changes
- **Image dimensions**: The image dimensions are now no longer fixed to 512x512. The dimensions of the init image are now used instead. The dimensions are adjusted to a multiple of 64.

### 1.0.0
Initial version

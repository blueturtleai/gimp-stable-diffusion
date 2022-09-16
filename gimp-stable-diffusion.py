#!/usr/bin/python

# v1.0.1

import urllib2
import tempfile
import os
import base64
import json

from gimpfu import *

INIT_FILE = "init.png"
GENERATED_FILE = "generated.png"
API_ENDPOINT = "api/img2img"
API_VERSION = 2

initFile = r"{}".format(os.path.join(tempfile.gettempdir(), INIT_FILE))
generatedFile = r"{}".format(os.path.join(tempfile.gettempdir(), GENERATED_FILE))

def getImageData(image, drawable):
   pdb.file_png_save_defaults(image, drawable, initFile, initFile)
   initImage = open(initFile, "rb")
   encoded = base64.b64encode(initImage.read())
   return encoded

def displayGenerated(seed):
   image = pdb.file_png_load(generatedFile, generatedFile)
   pdb.gimp_display_new(image)
   # image, drawable, x, y, text, border, antialias, size, size_type, fontname
   pdb.gimp_text_fontname(image, None, 2, 2, str(seed), -1, TRUE, 12, 1, "Sans")
   pdb.gimp_image_set_active_layer(image, image.layers[1])
   return

def img2img(image, drawable, initStrength, promptStrength, steps, prompt, seed, url):
   data = {
      "init_strength": float(initStrength),
      "prompt_strength": float(promptStrength),
      "steps": int(steps),
      "width": image.width,
      "height": image.height,
      "prompt": prompt,
      "seed": seed,
      "api_version": API_VERSION
   }

   imageData = getImageData(image, drawable)
   data.update({"init_img": imageData})
   data = json.dumps(data)

   headers = {"Content-Type": "application/json"}

   pdb.gimp_progress_set_text("starting dreaming now...")
   url = url + API_ENDPOINT
   request = urllib2.Request(url=url, data=data, headers=headers)

   try:
      response = urllib2.urlopen(request)

      data = response.read()
      data = json.loads(data)

      images = data["images"]
      imageData = base64.b64decode(images[0]["image"])

      imageFile = open(generatedFile, "wb+")
      imageFile.write(imageData)
      imageFile.close()

      displayGenerated(images[0]["seed"])

      if os.path.exists(initFile):
         os.remove(initFile)

      if os.path.exists(generatedFile):
         os.remove(generatedFile)

   except Exception as ex:
      if hasattr(ex, "code") and ex.code == 405:
         raise Exception("GIMP plugin and stable-diffusion server don't match. Please update the GIMP plugin. If the error still occurs, please reopen the colab notebook.")
      else:
         raise ex

   return

register(
   "img2img",
   "img2img",
   "img2img",
   "BlueTurtleAI",
   "BlueTurtleAI",
   "2022",
   "<Image>/AI/Stable img2img",
   "*",
   [
      (PF_SLIDER, "initStrength", "Init Strength", 0.3, (0.1, 0.9, 0.1)),
      (PF_SLIDER, "promptStrength", "Prompt Strength", 7.5, (0, 20, 0.5)),
      (PF_SLIDER, "steps", "Steps", 50, (10, 150, 1)),
      (PF_STRING, "prompt", "Prompt", ""),
      (PF_INT, "seed", "Seed", -1),
      (PF_STRING, "url", "Backend root URL", "")
   ],
   [],
   img2img
)

main()

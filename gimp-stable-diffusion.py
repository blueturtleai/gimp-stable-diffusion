#!/usr/bin/python

# v1.1.0

import urllib2
import tempfile
import os
import base64
import json
import re

from gimpfu import *

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

INIT_FILE = "init.png"
GENERATED_FILE = "generated.png"
API_ENDPOINT = "api/img2img"
API_VERSION = 4

initFile = r"{}".format(os.path.join(tempfile.gettempdir(), INIT_FILE))
generatedFile = r"{}".format(os.path.join(tempfile.gettempdir(), GENERATED_FILE))

def getImageData(image, drawable):
   pdb.file_png_save_defaults(image, drawable, initFile, initFile)
   initImage = open(initFile, "rb")
   encoded = base64.b64encode(initImage.read())
   return encoded

def displayGenerated(images):
   color = pdb.gimp_context_get_foreground()
   pdb.gimp_context_set_foreground((0, 0, 0))

   for image in images:
      imageFile = open(generatedFile, "wb+")
      imageFile.write(base64.b64decode(image["image"]))
      imageFile.close()

      imageLoaded = pdb.file_png_load(generatedFile, generatedFile)
      pdb.gimp_display_new(imageLoaded)
      # image, drawable, x, y, text, border, antialias, size, size_type, fontname
      pdb.gimp_text_fontname(imageLoaded, None, 2, 2, str(image["seed"]), -1, TRUE, 12, 1, "Sans")
      pdb.gimp_image_set_active_layer(imageLoaded, imageLoaded.layers[1])

   pdb.gimp_context_set_foreground(color)
   return

def img2img(image, drawable, isInpainting, maskBrightness, maskContrast, initStrength, promptStrength, steps, seed, imageCount, prompt, url):
   data = {
      "inpainting": bool(isInpainting),
      "mask_brightness": float(maskBrightness),
      "mask_contrast": float(maskContrast),
      "init_strength": float(initStrength),
      "prompt_strength": float(promptStrength),
      "steps": int(steps),
      "width": int(image.width),
      "height": int(image.height),
      "prompt": prompt,
      "image_count": int(imageCount),
      "api_version": API_VERSION
   }

   seed = -1 if not seed else int(seed)
   data.update({"seed": seed})

   imageData = getImageData(image, drawable)
   data.update({"init_img": imageData})
   data = json.dumps(data)

   accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
   user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

   headers = {'User-Agent': user_agent, 'Accept': accept, 'Content-Type': 'application/json'}

   url = url + "/" if not re.match(".*/$", url) else url
   url = url + API_ENDPOINT

   request = urllib2.Request(url=url, data=data, headers=headers)
   pdb.gimp_progress_set_text("starting dreaming now...")

   try:
      response = urllib2.urlopen(request)

      data = response.read()
      data = json.loads(data)

      displayGenerated(data["images"])

      if os.path.exists(initFile):
         os.remove(initFile)

      if os.path.exists(generatedFile):
         os.remove(generatedFile)

   except Exception as ex:
      if isinstance(ex, urllib2.HTTPError) and ex.code == 405:
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
      (PF_TOGGLE, "isInpainting", "Inpainting", False),
      (PF_SLIDER, "maskBrightness", "Inpainting\nMask Brightness", 1.0, (0.0, 1.0, 0.1)),
      (PF_SLIDER, "maskContrast", "Inpainting\nMask Contrast", 1.0, (0.0, 1.0, 0.1)),
      (PF_SLIDER, "initStrength", "Init Strength", 0.3, (0.0, 1.0, 0.1)),
      (PF_SLIDER, "promptStrength", "Prompt Strength", 7.5, (0, 20, 0.5)),
      (PF_SLIDER, "steps", "Steps", 50, (10, 150, 1)),
      (PF_STRING, "seed", "Seed (optional)", ""),
      (PF_SLIDER, "imageCount", "Number of images", 1, (1, 4,1)),
      (PF_STRING, "prompt", "Prompt", ""),
      (PF_STRING, "url", "Backend root URL", "")
   ],
   [],
   img2img
)

main()

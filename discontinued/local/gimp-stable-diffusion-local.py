#!/usr/bin/python

# v1.1.0

import urllib2
import tempfile
import os
import base64
import json
import re
import random
import math
import gimp
from gimpfu import *

VERSION = 110
INIT_FILE = "init.png"
GENERATED_FILE = "generated.png"
API_ENDPOINT = "predictions"

initFile = r"{}".format(os.path.join(tempfile.gettempdir(), INIT_FILE))
generatedFile = r"{}".format(os.path.join(tempfile.gettempdir(), GENERATED_FILE))

def checkUpdate():
  try:
     gimp.get_data("update_checked")
     updateChecked = True
  except Exception as ex:
     updateChecked = False

  if updateChecked is False:
     try:
        url = "https://raw.githubusercontent.com/blueturtleai/gimp-stable-diffusion/main/local/version.json"
        response = urllib2.urlopen(url)
        data = response.read()
        data = json.loads(data)
        gimp.set_data("update_checked", "1")

        if VERSION < int(data["version"]):
           pdb.gimp_message(data["message"])
     except Exception as ex:
        ex = ex

def cleanup():
   try:
      if os.path.exists(initFile):
         os.remove(initFile)

      if os.path.exists(generatedFile):
         os.remove(generatedFile)
   except Exception as ex:
      ex = ex

def getImages(data, seed):
   images = []

   for counter in range(len(data["output"])):
      image = re.match("data:image/png;base64,(.*)", data["output"][counter]).group(1)
      image = {"img": image, "seed": seed}
      images.append(image)

   return images

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
      imageFile.write(base64.b64decode(image["img"]))
      imageFile.close()

      imageLoaded = pdb.file_png_load(generatedFile, generatedFile)
      pdb.gimp_display_new(imageLoaded)
      # image, drawable, x, y, text, border, antialias, size, size_type, fontname
      pdb.gimp_text_fontname(imageLoaded, None, 2, 2, str(image["seed"]), -1, TRUE, 12, 1, "Sans")
      pdb.gimp_image_set_active_layer(imageLoaded, imageLoaded.layers[1])

   pdb.gimp_context_set_foreground(color)
   return

def generate(image, drawable, mode, initStrength, promptStrength, steps, seed, prompt, url):
   if image.width < 384 or image.width > 1024 or image.height < 384 or image.height > 1024:
      raise Exception("Invalid image size. Image needs to be between 384x384 and 1024x1024.")

   if image.width * image.height > 786432:
      raise Exception("Invalid image size. Maximum size is 1024x768 or 768x1024.")

   if prompt == "":
      raise Exception("Please enter a prompt.")

   if mode == "MODE_INPAINTING" and drawable.has_alpha == 0:
      raise Exception("Invalid image. For inpainting an alpha channel is needed.")

   pdb.gimp_progress_init("", None)

   input = {
      "prompt": prompt,
      "num_inference_steps": int(steps),
      "guidance_scale": float(promptStrength)
   }

   if image.width % 64 != 0:
      width = math.floor(image.width/64) * 64
   else:
      width = image.width

   if image.height % 64 != 0:
      height = math.floor(image.height/64) * 64
   else:
      height = image.height

   input.update({"width": int(width)})
   input.update({"height": int(height)})

   if not seed:
      seed = random.randint(0, 2**31)
   else:
      seed = int(seed)

   input.update({"seed": seed})

   if mode == "MODE_IMG2IMG" or mode == "MODE_INPAINTING":
      imageData = getImageData(image, drawable)
      input.update({"init_image": imageData})
      input.update({"prompt_strength": (1 - float(initStrength))})

   if mode == "MODE_INPAINTING":
      input.update({"mask": imageData})

   data = {"input": input}
   data = json.dumps(data)

   headers = {"Content-Type": "application/json", "Accept": "application/json"}

   url = url + "/" if not re.match(".*/$", url) else url
   url = url + API_ENDPOINT

   request = urllib2.Request(url=url, data=data, headers=headers)
   pdb.gimp_progress_set_text("starting dreaming now...")

   try:
      response = urllib2.urlopen(request)
      data = response.read()

      try:
         data = json.loads(data)
      except Exception as ex:
         raise Exception(data)

      if data["status"] == "failed":
         raise Exception("The image couldn't be generated: " + data["error"])

      images = getImages(data, seed)
      displayGenerated(images)
   except Exception as ex:
      raise ex
   finally:
      pdb.gimp_progress_end()
      cleanup()
      checkUpdate()

   return

register(
   "stable-local",
   "stable-local",
   "stable-local",
   "BlueTurtleAI",
   "BlueTurtleAI",
   "2022",
   "<Image>/AI/Stable Local",
   "*",
   [
      (PF_RADIO, "mode", "Generation Mode", "MODE_TEXT2IMG", (
         ("Text -> Image", "MODE_TEXT2IMG"),
         ("Image -> Image", "MODE_IMG2IMG"),
         ("Inpainting", "MODE_INPAINTING")
      )),
      (PF_SLIDER, "initStrength", "Init Strength", 0.3, (0.0, 1.0, 0.1)),
      (PF_SLIDER, "promptStrength", "Prompt Strength", 7.5, (0, 20, 0.5)),
      (PF_SLIDER, "steps", "Steps", 50, (10, 150, 1)),
      (PF_STRING, "seed", "Seed (optional)", ""),
      (PF_STRING, "prompt", "Prompt", ""),
      (PF_STRING, "url", "Backend root URL", "")
   ],
   [],
   generate
)

main()

#!/usr/bin/python

# v1.3.5

import urllib2
import tempfile
import os
import base64
import json
import ssl
import sched, time
import math
import gimp
import re

from gimpfu import *

VERSION = 135
INIT_FILE = "init.png"
GENERATED_FILE = "generated.png"
API_ROOT = "https://stablehorde.net/api/v2/"

# check every 5 seconds
CHECK_WAIT = 5
checkMax = None

ssl._create_default_https_context = ssl._create_unverified_context

initFile = r"{}".format(os.path.join(tempfile.gettempdir(), INIT_FILE))
generatedFile = r"{}".format(os.path.join(tempfile.gettempdir(), GENERATED_FILE))
s = sched.scheduler(time.time, time.sleep)

checkCounter = 0
id = None

def checkUpdate():
  try:
     gimp.get_data("update_checked")
     updateChecked = True
  except Exception as ex:
     updateChecked = False

  if updateChecked is False:
     try:
        url = "https://raw.githubusercontent.com/blueturtleai/gimp-stable-diffusion/main/stablehorde/version.json"
        response = urllib2.urlopen(url)
        data = response.read()
        data = json.loads(data)
        gimp.set_data("update_checked", "1")

        if VERSION < int(data["version"]):
           pdb.gimp_message(data["message"])
     except Exception as ex:
        ex = ex

def getImageData(image, drawable):
   pdb.file_png_save_defaults(image, drawable, initFile, initFile)
   initImage = open(initFile, "rb")
   encoded = base64.b64encode(initImage.read())
   return encoded

def displayGenerated(images):
   color = pdb.gimp_context_get_foreground()
   pdb.gimp_context_set_foreground((0, 0, 0))

   for image in images:
      if re.match("^https.*", image["img"]):
          response = urllib2.urlopen(image["img"])
          bytes = response.read()
      else:
          bytes = base64.b64decode(image["img"])

      imageFile = open(generatedFile, "wb+")
      imageFile.write(bytes)
      imageFile.close()

      imageLoaded = pdb.file_webp_load(generatedFile, generatedFile)
      pdb.gimp_display_new(imageLoaded)
      # image, drawable, x, y, text, border, antialias, size, size_type, fontname
      pdb.gimp_text_fontname(imageLoaded, None, 2, 2, str(image["seed"]), -1, TRUE, 12, 1, "Sans")
      pdb.gimp_image_set_active_layer(imageLoaded, imageLoaded.layers[1])

   pdb.gimp_context_set_foreground(color)
   return

def getImages():
   url = API_ROOT + "generate/status/" + id
   response = urllib2.urlopen(url)
   data = response.read()
   data = json.loads(data)

   return data["generations"]

def checkStatus():
   url = API_ROOT + "generate/check/" + id
   response = urllib2.urlopen(url)
   data = response.read()
   data = json.loads(data)

   global checkCounter
   checkCounter = checkCounter + 1

   if data["processing"] == 0:
      text = "Queue position: " + str(data["queue_position"]) + ", Wait time: " + str(data["wait_time"]) + "s"
   elif data["processing"] > 0:
      text = "Generating..."

   pdb.gimp_progress_set_text(text)

   if checkCounter < checkMax and data["done"] is False:
      if data["is_possible"] is True:
         s.enter(CHECK_WAIT, 1, checkStatus, ())
         s.run()
      else:
         raise Exception("Currently no worker available to generate your image. Please try again later.")
   elif checkCounter == checkMax:
      minutes = (checkMax * CHECK_WAIT)/60
      raise Exception("Image generation timed out after " + str(minutes) + " minutes. Please try it again later.")
   elif data["done"] == True:
      return

def generate(image, drawable, mode, inpControl, selModel, prompt, neg_prompt, promptStrength, initStrength, sampler, steps, seed, nsfw, apikey, maxWaitMin, GFPGAN, CodeFormers, faceFixerStrength, strip_background, upscaler):

   if image.width < 384 or image.width > 1024 or image.height < 384 or image.height > 1024:
      raise Exception("Invalid image size. Image needs to be between 384x384 and 1024x1024.")

   if prompt == "":
      raise Exception("Please enter a prompt.")
   elif neg_prompt != "":
      prompt = prompt + (" ### ") + neg_prompt

   if mode == "MODE_INPAINTING" and drawable.has_alpha == 0:
      raise Exception("Invalid image. For inpainting an alpha channel is needed.")

   pdb.gimp_progress_init("", None)

   global checkMax
   checkMax = (maxWaitMin * 60)/CHECK_WAIT

   optionList = []
   if GFPGAN:
       optionList.append("GFPGAN")
   if CodeFormers:
       optionList.append("CodeFormers")
   if strip_background:
       optionList.append("strip_background")
   if upscaler > 0:
       optionList.append(scalerList[upscaler])
       
   selectedModel = [ modelList[selModel] ]
   inpaintControl = inpControlList[inpControl]
   sampler_name = sampList[sampler]
   repl_filter = not nsfw
   
   try:
      params = {
         "cfg_scale": float(promptStrength),
         "steps": int(steps),
         "seed": seed,
         "facefixer_strength": float(faceFixerStrength),
         "post_processing": optionList
      }

      data = {
         "params": params,
         "models": selectedModel,
         "prompt": prompt,
         "nsfw": nsfw,
         "replacement_filter": repl_filter,
         "censor_nsfw": False,
         "r2": True
      }
      
      if image.width % 64 != 0:
         width = math.floor(image.width/64) * 64
      else:
         width = image.width

      if image.height % 64 != 0:
         height = math.floor(image.height/64) * 64
      else:
         height = image.height

      params.update({"width": int(width)})
      params.update({"height": int(height)})

      if mode == "MODE_IMG2IMG":
         init = getImageData(image, drawable)
         data.update({"source_image": init})
         data.update({"source_processing": "img2img"})
         params.update({"denoising_strength": (1 - float(initStrength))})
         params.update({"control_type" : inpaintControl})
         params.update({"sampler_name": sampler_name})
      elif mode == "MODE_INPAINTING":
         init = getImageData(image, drawable)
         data.update({"source_image": init})
         data.update({"source_processing": "inpainting"})
         params.update({"denoising_strength": (1 - float(initStrength))})
         params.update({"control_type" : inpaintControl})
      else:
         params.update({"sampler_name": sampler_name})
      
      data = json.dumps(data)

      apikey = "0000000000" if not apikey else apikey

      headers = {"Content-Type": "application/json", "Accept": "application/json", "apikey": apikey}
      url = API_ROOT + "generate/async"

      request = urllib2.Request(url=url, data=data, headers=headers)

      response = urllib2.urlopen(request)
      data = response.read()

      try:
         data = json.loads(data)
         global id
         id = data["id"]
      except Exception as ex:
         raise Exception(data)

      checkStatus()
      images = getImages()
      displayGenerated(images)

   except urllib2.HTTPError as ex:
      try:
         data = ex.read()
         data = json.loads(data)

         if "message" in data:
            message = data["message"]
         else:
            message = str(ex)
      except Exception:
         message = str(ex)

      raise Exception(message)
   except Exception as ex:
      raise ex
   finally:
      pdb.gimp_progress_end()
      checkUpdate()

   return

def getAvailModels():

   url = API_ROOT + "status/models?type=image"
   response = urllib2.urlopen(url)
   data = response.read()
   data = json.loads(data)

   modelList = []
   modelVerboseList = []
   SD_pos = 0
   for model in data:
       modelList.append(model["name"])
       modelVerboseList.append(model["name"] + " (" + str(model["count"]) + ") - queue: " + str(model["jobs"]))
       if model["name"] == "stable_diffusion":
           SD_pos = len(modelList) -1
   
   return modelList, modelVerboseList, SD_pos

inpControlList = [ "canny", "hed", "depth", "normal", "openpose", "seg", "scribble", "fakescribbles", "hough" ]
sampList = ["k_dpm_2_a", "k_euler_a", "lcm", "k_euler", "k_dpmpp_2s_a", "k_dpm_fast", "k_dpm_adaptive", "k_dpmpp_sde", "k_lms", "k_heun", "k_dpmpp_2m", "dpmsolver", "DDIM", "k_dpm_2" ]
scalerList = ["none", "RealESRGAN_x2plus", "RealESRGAN_x4plus_anime_6B", "NMKD_Siax", "4x_AnimeSharp"]
modelList, modelVerboseList, SD_position = getAvailModels()

register(
   "stable-horde", #function name
   "stable-horde", #menu label
   "stable-horde", #description
   "BlueTurtleAI", #author
   "BlueTurtleAI", #copyright notice
   "2022", #date created
   "<Image>/AI/Stablehorde", #menupath
   "*", #image type that the script works on
   [
      (PF_RADIO, "mode", "Generation Mode", "MODE_TEXT2IMG", (
         ("Text -> Image", "MODE_TEXT2IMG"),
         ("Image -> Image", "MODE_IMG2IMG"),
         ("Inpainting", "MODE_INPAINTING")
      )),
      (PF_OPTION, "inpControl", "Img2Img/Inpainting control", 3, inpControlList),
      (PF_OPTION, "selModel", "Model", SD_position, modelVerboseList),
      (PF_STRING, "prompt", "Prompt", ""),
      (PF_STRING, "neg_prompt", "Negative Prompt", ""),
      (PF_SLIDER, "promptStrength", "Prompt Strength", 8, (0, 30, 1)),
      (PF_SLIDER, "initStrength", "Init Strength", 0.3, (0, 1, 0.01)),
      (PF_OPTION, "sampler", "Sampler", 3, sampList),
      (PF_SLIDER, "steps", "Steps", 50, (10, 150, 1)),
      (PF_STRING, "seed", "Seed (optional)", ""),
      (PF_TOGGLE, "nsfw", "NSFW", True),
      (PF_STRING, "apiKey", "API key (optional)", ""),
      (PF_SLIDER, "maxWaitMin", "Max Wait (minutes)", 5, (1, 15, 1)),
      (PF_TOGGLE, "GFPGAN", "Post-process GFPGAN", False),
      (PF_TOGGLE, "CodeFormers", "Post-process CodeFormers", False),
      (PF_SLIDER, "faceFixerStrength", "Face Fixer Strength", 0.7, (0, 1, 0.01)),
      (PF_TOGGLE, "strip_background", "Post-process strip_background", False),
      (PF_OPTION, "upscaler", "Upscaler", 0, scalerList)
   ],
   [], #results
   generate #function
)

main()

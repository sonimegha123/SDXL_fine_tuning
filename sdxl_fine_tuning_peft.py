# -*- coding: utf-8 -*-
"""SDXL Model Fine-Tuning Aditya 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1A1UsGs1mx8YqbtMMAm5N3rJfBK3E40kG

# [Reference Link](https://github.com/huggingface/diffusers/blob/main/examples/text_to_image/README_sdxl.md)

# **Stable Diffusion XL Text-to-Image Fine-Tuning**

# ***Checking for Available GPU***
"""

!nvidia-smi

"""# ***Installing Necessary Libraries***"""

!pip install diffusers
!pip install accelerate

"""# **Connecting with Drive and changing the directory**

# ***Setting-Up HuggingFace Token***
"""

from huggingface_hub import notebook_login
notebook_login()

"""# ***Model Inferencing - Before Fine-Tunning***"""

# Loading the Text-Guided Image to Image Model

import torch
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import make_image_grid, load_image

pipeline = AutoPipelineForImage2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
)
pipeline.enable_model_cpu_offload()

"""# ***Model Inferencing - After Fine-Tunning***

#***Cloning the GitHub Repo***
"""

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/

# Commented out IPython magic to ensure Python compatibility.
# !pip install ./diffusers
# %cd /content/drive/MyDrive/diffusers

!pip install -e .
!pip install wandb
!pip install deepspeed

!pip install -U -r /content/drive/MyDrive/diffusers/examples/text_to_image/requirements_sdxl.txt

from huggingface_hub import notebook_login
notebook_login()

import wandb
wandb.login()

# compute_environment: LOCAL_MACHINE
# debug: true
# deepspeed_config:
#   gradient_accumulation_steps: 1
#   gradient_clipping: 1.0
#   offload_optimizer_device: none
#   offload_param_device: none
#   zero3_init_flag: false
#   zero_stage: 2
# distributed_type: DEEPSPEED
# downcast_bf16: 'no'
# machine_rank: 0
# main_training_function: main
# mixed_precision: fp16
# num_machines: 1
# num_processes: 1
# rdzv_backend: static
# same_network: true
# tpu_env: []
# tpu_use_cluster: false
# tpu_use_sudo: false
# use_cpu: false

"""# ***Initializing the Accelerator***"""

!accelerate config default --mixed_precision fp16

from accelerate.utils import write_basic_config
write_basic_config()

"""# ***Loading the Stable Diffusion XL Model***"""

import os
os.environ['MODEL_NAME'] = f'stabilityai/stable-diffusion-xl-base-1.0'
os.environ['DATASET_NAME'] = f"/content/drive/MyDrive/Datasets/combine_images/"
os.environ['OUTPUT_DIR'] = f'/content/drive/MyDrive/Weights_of_models/sdxl_fine_tuned_model_aditya_2'
os.environ['VAE_NAME'] = f'madebyollin/sdxl-vae-fp16-fix'
os.environ['ACCELERATE_CONFIG_FILE'] = f'/content/drive/MyDrive/Datasets/combine_images/accelerate_config.yaml'
# os.environ['TRAIN_DATA_DIR'] = f'/content/drive/MyDrive/5resize_images_abstract_2024-05-09_0519/

# export MODEL_NAME="stabilityai/stable-diffusion-xl-base-1.0"
# export VAE_NAME="madebyollin/sdxl-vae-fp16-fix"
# export DATASET_NAME="lambdalabs/naruto-blip-captions"
# export ACCELERATE_CONFIG_FILE="your accelerate_config.yaml"

"""# ***Fine-Tuning Stable Diffusion XL Model***"""

!accelerate launch  --config_file $ACCELERATE_CONFIG_FILE /content/drive/MyDrive/diffusers/examples/text_to_image/train_text_to_image_lora_sdxl.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --pretrained_vae_model_name_or_path=$VAE_NAME \
  --dataset_name=$DATASET_NAME \
  --image_column="image" \
  --caption_column="text" \
  --resolution=512  \
  --train_batch_size=8 \
  --num_train_epochs=50 \
  --checkpointing_steps=1000 \
  --learning_rate=1e-04 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --mixed_precision="fp16" \
  --validation_epochs=20 \
  --seed=1234 \
  --output_dir=$OUTPUT_DIR \
  --validation_prompt=''' This image is a bohemian-style pattern featuring a grid of overlapping paisley motifs. The grid is formed by light blue lines, while the paisley motifs are filled with a watercolor-like blue and white tie-dye pattern. The overall effect is one of movement and energy, with the paisley motifs appearing to float on the surface of the grid.''' \
  --report_to="wandb"

# paisley_239.jpg
# --train_data_dir=$TRAIN_DATA_DIR \

"""# ***Getting Inference from the Fine-Tuned Model***

### ***Text-to-Image Inference***
"""

!pip install diffusers
!pip install accelerate
!pip install -U peft

# Loading the Fine-Tuned Model
import torch
from diffusers import StableDiffusionPipeline,DiffusionPipeline

model_path = "/content/drive/MyDrive/Weights_of_models/sdxl_fine_tuned_model_aditya_2"
pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16)
pipe.to("cuda")
pipe.load_lora_weights(model_path)

prompt = "This is a seamless paisley pattern. It features a dark blue background with a multi-colored floral design. The pattern is made up of repeating paisley shapes, which are often used in Indian and Persian textile designs. The paisley shapes are filled with intricate floral details and have a curved, teardrop-shaped outline. The colors used in the pattern are purple, blue, green, yellow, and orange. The pattern has a luxurious, bohemian feel"
image = pipe(prompt,guidance_scale=5).images[0]
image

prompt = " The image is a geometric pattern composed of interlocking curved shapes in shades of blue, green, and beige. The shapes are arranged in a grid-like pattern, with each shape having a unique color and texture. The overall effect is one of movement and energy, as the shapes seem to flow into each other."
image = pipe(prompt,guidance_scale=5).images[0]
image

prompt = " The pattern is a seamless vector design featuring a lattice of interlocking organic shapes resembling stylized leaves. The shapes are formed by a series of curved lines that create a sense of movement and energy."
image = pipe(promp,guidance_scale=5).images[0]
image

prompt = "This is a seamless paisley pattern. It features a dark blue background with a multi-colored floral design. The pattern is made up of repeating paisley shapes The paisley shapes are filled with intricate floral details and have a curved, teardrop-shaped outline. The colors used in the pattern are purple, blue, green, yellow, and orange."
image = pipe(prompt).images[0]
image

"""### ***Image-to-Image Inference***"""

# import torch
# from diffusers import AutoPipelineForImage2Image
# from diffusers.utils import make_image_grid, load_image

# pipeline = AutoPipelineForImage2Image.from_pretrained(
#     model_path, torch_dtype=torch.float16, variant="fp16", use_safetensors=True
# )
# pipeline.enable_model_cpu_offload()

from PIL import Image
import io

import torch
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import make_image_grid, load_image

image_path = "/content/drive/MyDrive/Datasets/abstract_2024-05-10_1314/1030401-(3).jpg"# Update this path

init_image = Image.open(image_path)
image1 = init_image.resize(512 x 512)



prompt = '''Generate variations of an input fabric image from the fashion industry while preserving its structural elements like patterns and textures. Apply changes in color schemes, subtly modify pattern details, and introduce different fabric textures while maintaining the original design's integrity. Ensure that the new colors enhance the aesthetic appeal, pattern modifications do not distort the design, and textures match the fabric type. The output should maintain the resolution, aspect ratio, and high quality of the input image, ensuring the design is still suitable for fabric manufacturing.'''

image = pipe(prompt, image=image1,guidance_scale=5).images[0]
make_image_grid([image1, image], rows=1, cols=2)

image_path = "/content/drive/MyDrive/Datasets/abstract_2024-05-09_0519/5031017 -4.jpg"

init_image = Image.open(image_path)
init_image_resized = init_image.resize((512, 512))

# prompt = "Create a variation of the provided fabric design, retaining the overall structure, layout, and color theme. Introduce subtle variations while preserving the grid structure for geometric patterns. Modify specific shapes, abstract floral designs, or marbled patterns, maintaining the overall theme."
neg_prompt = "different image style and color"
prompt = "Generate a texture variation that retain the original structure. Modify the color schemes to include harmonious and contrasting combinations, subtly adjust the patterns to introduce fresh elements, and incorporate different texture"
num_variations = 3

image = pipe(prompt,image=init_image_resized, guidance_scale=7.5,strength=0.1).images[0]
output_image = image.resize((512, 512))
make_image_grid([init_image_resized, output_image], rows=1, cols=2)

from PIL import Image
import matplotlib.pyplot as plt

# Load and resize the initial image
image_path = "/content/drive/MyDrive/Datasets/abstract_2024-05-09_0519/5031017 -4.jpg"
init_image = Image.open(image_path)
init_image_resized = init_image.resize((512, 512))

# Define prompts
neg_prompt = "different image style and color"
prompt = "Generate a texture variation that retain the original structure. Modify the color schemes to include harmonious and contrasting combinations, subtly adjust the patterns to introduce fresh elements, and incorporate different texture."
num_variations = 3

# Generate variations
variations = pipe(prompt, negative_prompt=neg_prompt, num_images_per_prompt=num_variations, image=init_image_resized, guidance_scale=7.5,strength=0.5).images

# Resize variations to match the initial image size
variations_resized = [image.resize((512, 512)) for image in variations]

# Prepare images for display
all_images = [init_image_resized] + variations_resized

# Create a grid to display images
def make_image_grid(images, rows, cols):
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i])
        ax.axis('off')
    plt.tight_layout()
    plt.show()

# Display the original and variation images in a grid
make_image_grid(all_images, rows=1, cols=4)

image_path = "/content/drive/MyDrive/Datasets/abstract_2024-05-09_0519/10301075.jpg"

init_image = Image.open(image_path)
init_image_resized = init_image.resize((512, 512))

# prompt = "Create a variation of the provided fabric design. Retain the overall structure and layout and color theme, but replace the existing patterns with new, yet similar elements. If the pattern features specific shapes, abstract designs, marbled pattern, modify them while maintaining the overall theme."
prompt = "Produce a variation of this marble style textile pattern, keeping the flowing, organic lines intact, with subtle changes in the pattern swirls and color gradients."

image = pipe(prompt, image=init_image_resized, guidance_scale=5).images[0]
output_image = image.resize((512, 512))
make_image_grid([init_image_resized, output_image], rows=1, cols=2)

image_path = "/content/drive/MyDrive/Datasets/7resize_images_abstract_2024-05-09_0519/50310146-5.jpg"

init_image = Image.open(image_path)
init_image_resized = init_image.resize((512, 512))

# prompt = "Create a variation of the provided fabric design. Retain the overall structure and layout and color theme, but replace the existing patterns with new, yet similar elements. If the pattern features specific shapes, abstract designs or marbled pattern, modify them while maintaining the overall theme."
prompt = "Generate a texture variation that retain the original structure. Modify the color schemes to include harmonious and contrasting combinations, subtly adjust the patterns to introduce fresh elements, and incorporate different texture."


image = pipe(prompt, image=init_image_resized,strength=0.8).images[0]
output_image = image.resize((512, 512))
make_image_grid([init_image_resized, output_image], rows=1, cols=2)

from PIL import Image
import io

image_path = "/content/resize_images/abstract (22).jpg"# Update this path

init_image = Image.open(image_path)


prompt = "Create a new variation of the provided design pattern, capturing the original's artistic style and color scheme. Adapt the design to include new, yet harmonious color combinations, ensuring variant respects the initial pattern's essence and artistic flair. Aim for diversity while maintaining a cohesive link to the original concept."

image = pipeline(prompt, image=init_image).images[0]
make_image_grid([init_image, image], rows=1, cols=2)

from PIL import Image
import io

image_path = "/content/resize_images/abstract (17).jpg"# Update this path

init_image = Image.open(image_path)

prompt = "Create a new variation of the provided design pattern, capturing the original's artistic style and color scheme. Adapt the design to include new, yet harmonious color combinations, ensuring variant respects the initial pattern's essence and artistic flair. Aim for diversity while maintaining a cohesive link to the original concept."

image = pipeline(prompt, image=init_image).images[0]
make_image_grid([init_image, image], rows=1, cols=2)

from PIL import Image
import io

image_path = "//content/resize_images/abstract (25).jpg"# Update this path

init_image = Image.open(image_path)

prompt = "Create a new variation of the provided design pattern, capturing the original's artistic style and color scheme"

image = pipeline(prompt, image=init_image).images[0]
make_image_grid([init_image, image], rows=1, cols=2)

from PIL import Image
import io

image_path = "/content/resize_images/floral (1).jpg"# Update this path

init_image = Image.open(image_path)

prompt = "Create a new variation of the provided design pattern, capturing the original's artistic style and color scheme"

image = pipeline(prompt, image=init_image).images[0]
make_image_grid([init_image, image], rows=1, cols=2)

from PIL import Image
import io

image_path = "/content/resize_images/floral (21).jpg"# Update this path

init_image = Image.open(image_path)

prompt = "Create a new variation of the provided design pattern, capturing the original's artistic style and color scheme"

image = pipeline(prompt, image=init_image).images[0]
make_image_grid([init_image, image], rows=1, cols=2)

# from diffusers import DiffusionPipeline
# import torch

# model_path = "you-model-id-goes-here" # <-- change this
# pipe = DiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
# pipe.to("cuda")

# prompt = "A pokemon with green eyes and red legs."
# image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5).images[0]
# image.save("pokemon.png")
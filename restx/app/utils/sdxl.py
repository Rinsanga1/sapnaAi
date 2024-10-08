import torch
import base64
from io import BytesIO
from diffusers import LCMScheduler, AutoPipelineForText2Image


def init_pipe():
    model_id = "stabilityai/stable-diffusion-xl-base-1.0"
    adapter_id = "latent-consistency/lcm-lora-sdxl"

    pipe = AutoPipelineForText2Image.from_pretrained(
        model_id, torch_dtype=torch.float16, variant="fp16"
    )
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    pipe.to("cuda")

    # load and fuse lcm lora
    pipe.load_lora_weights(adapter_id)
    pipe.fuse_lora()
    return pipe


prompt = "Self-portrait oil painting, a beautiful cyborg with golden hair, 8k"


def generate_sapna(prompt, pipe):
    np = "blurry, bad hands, extra hands, extra fingers, fused fingers, malformed limbs, mutated hands, poorly drawn hands,missing hands,three hands,too many fingers,deformed hands,fused hands,missing fingers"

    image = pipe(
        prompt=prompt, negative_prompt=np, num_inference_steps=7, guidance_scale=1.0
    ).images[0]

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    print("inference done")
    return img_str

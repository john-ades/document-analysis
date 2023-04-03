import os

from transformers import CLIPProcessor, CLIPModel

from PIL import Image

__classifier__ = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
__processor__ = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")


def zero_shot_image_classification(images: list[Image.Image], classes: list[str]) -> list[dict[str, float]]:
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    inputs = __processor__(text=classes, images=images, return_tensors="pt", padding=True)
    outputs = __classifier__(**inputs)
    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    predictions = logits_per_image.softmax(dim=1)
    predictions = [[round(float(score), 2) for score in scores] for scores in predictions]
    return [dict(zip(classes,scores)) for scores in predictions]

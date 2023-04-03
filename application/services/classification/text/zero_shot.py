from transformers import pipeline

__classifier__ = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def zero_shot_text_classification(text: str, classes: list[str], multi_class=False) -> dict[str, float]:
    prediction = __classifier__(text, classes, multi_class=multi_class)
    return dict(zip(prediction["labels"],prediction["scores"]))

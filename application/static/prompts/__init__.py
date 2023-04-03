import os
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))

# Classification Prompts
classification_document_prompt = Path(dir_path + "/classification_document_prompt").read_text()
classification_document_w_context_prompt = Path(dir_path + "/classification_document_w_context_prompt").read_text()

# Line Item Extraction Prompt
line_item_extraction_prompt = Path(dir_path + "/line_item_extraction_prompt").read_text()
line_item_extraction_w_context_prompt = Path(dir_path + "/line_item_extraction_w_context_prompt").read_text()

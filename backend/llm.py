from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline


generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct",
    max_new_tokens=50,
    return_full_text=False
)

llm = HuggingFacePipeline(
    pipeline=generator
)
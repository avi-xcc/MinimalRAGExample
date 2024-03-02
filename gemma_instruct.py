import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import streamlit as st

# access_token="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"

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it", cache_dir="models")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it", cache_dir="models",
                                             device_map="auto", torch_dtype=torch.bfloat16)


@st.cache_resource
def llm(prompt: str) -> str:
    chat = [
        {"role": "user",
         "content": prompt}
    ]
    retargeted_prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer.encode(retargeted_prompt, add_special_tokens=True, return_tensors="pt")
    outputs = model.generate(input_ids=inputs.to(model.device), max_new_tokens=150)

    out = tokenizer.decode(outputs[0]).split("<start_of_turn>model")[-1]
    while True:
        if "<eos>" in out:
            return out.split("<eos>")[0]
        else:
            outputs = model.generate(input_ids=outputs, max_new_tokens=150)
            out = out + tokenizer.decode(outputs[0]).split("<start_of_turn>model")[-1][len(out):]

# llm = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)


# print(llm("How does transformers work?"))

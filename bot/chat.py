
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def chat_response(user_input, chat_history_ids=None):
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    bot_input_ids = torch.cat([chat_history_ids, inputs], dim=-1) if chat_history_ids is not None else inputs

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )

    new_tokens = chat_history_ids[:, bot_input_ids.shape[-1]:]
    reply = tokenizer.decode(new_tokens[0], skip_special_tokens=True)

    return reply, chat_history_ids

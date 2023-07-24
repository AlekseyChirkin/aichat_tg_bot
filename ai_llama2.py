from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained('..\llama_models\mythoboros-13b.ggmlv3.q4_0.bin', model_type='llama')

def get_answer(message: str)-> str:
    return llm(message)

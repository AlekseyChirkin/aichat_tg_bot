import g4f

current_provider = g4f.Provider.Aichat

# g4f USAGE:

# print(g4f.Provider.DfeHub.params) # supported args

# Automatic selection of provider

# # streamed completion
# response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', messages=[
#                                      {"role": "user", "content": "Hello world"}], stream=True)
# for message in response:
#     print(message)

# # normal response
# response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, messages=[
#                                      {"role": "user", "content": "hi"}]) # alterative model setting
# print(response)

# # Set with provider
# response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.Forefront, messages=[
#                                      {"role": "user", "content": "Hello world"}], stream=True)
# for message in response:
#     print(message)


def get_answer(input_msg: str) -> str:
    return g4f.ChatCompletion.create(model=g4f.Model.gpt_35_turbo, provider=current_provider, messages=[{"role": "user", "content": input_msg}])

if __name__ == "__main__":
    print(current_provider.params) # supported args
    print(g4f.ChatCompletion.create(model=g4f.Model.gpt_35_turbo, provider=current_provider, messages=[{"role": "user", "content": "Расскажи, o себе, при этом веди повествование как хулиган"}]))

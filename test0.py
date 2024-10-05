import openai_api


msg = [{"role": "user", "content": "hi"}]
reply = openai_api.str_request(msg,500)
print(reply)

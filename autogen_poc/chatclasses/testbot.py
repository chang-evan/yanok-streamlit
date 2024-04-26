from streamlist_chat import StreamlitAppBase

bot = StreamlitAppBase("Act as an interviewer.")
bot.run()

# Loop through the messages list and print each message.
print(bot.messages[-2])
print(bot.messages[-1])

'''
for message in bot.messages:
    print(f'Role: {message["role"]}, Content: {message["content"]}')
'''
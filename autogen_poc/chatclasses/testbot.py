from streamlist_chat import StreamlitAppBase

bot = StreamlitAppBase("Act as an interviewer.")
bot.run()

# print messages in terminal
print(bot.messages[-2])
print(bot.messages[-1])

# Need to think about how we can use this class. e.g. if bot.messages % 5 == 0, send an api request from here for an updated vocab scoring list

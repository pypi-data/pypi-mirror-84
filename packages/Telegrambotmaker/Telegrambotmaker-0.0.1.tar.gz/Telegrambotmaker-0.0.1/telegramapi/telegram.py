import requests

class TelegramDocs:
    def printDocs():
        print("<-- Telegram API Quick Start Guide -->")
        print("Step 1: Create the bot at Telegram.")
        print("     -> First, go into telegram and start a conversation with \"BotFather\". Type /newbot. You will get a nice Token. Don't share it with anyone!")
        print("Step 2: Program your bot.")
        print("     -> Here is an example script.")
        print("import telegram.telegram")
        print("from time import sleep")
        print("")
        print("bot = telegram.TelegramBot(\"Your Token here\")")
        print("")
        print("print(bot.getToken())")
        print("")
        print("while True:")
        print("    update = bot.getUpdate()")
        print("    if update == True:")
        print("        print(\"F ConnectionError\")")
        print("    elif update == False:")
        print("        print(\"Nothing new\")")
        print("    else:")
        print("        chatId = update['message']['chat']['id']")
        print("        text = update['message']['text']")
        print("        bot.sendMessage(chatId, text)")
        print("    sleep(1)")
        print("")
        print("     -> See, simple!")
        print("     -> Message the bot and it will repeat everything you said. With a bit more coding you can do more than that!")
        print("")
        print("<-- Telegram API Documentation -->")
        print("Sending a Message:")
        print("     -> TelegramBot.sendMessage(self, chatId, message)")
        print("     -> self - Ignore, do not set")
        print("     -> chatId - The ID of the chat. Get it with TelegramBot.getUpdate()['message']['chat']['id']")
        print("     -> message - The Message. Thats All. Get the Message sent by the user with TelegramBot.getUpdate()['message']['text']")
        print("Getting the Token:")
        print("     -> Easy, TelegramBot.getToken() returns your Token")
        print("Getting Messages:")
        print("     -> This is a bit harder, but when you once understand it, you will know it forever")
        print("     -> TelegramBot.getUpdate(self)")
        print("     -> self - Ignore, do not set")
        print("     -> Example: TelegramBot.getUpdate()['message']['text'] gets the message sent by the user. At https://api.telegram.org/ you will get more information about what to do with updates")

class TelegramBot:
    def __init__(self, __TOKEN__):
        self.TOKEN = __TOKEN__
        self.OFFSET = 0
        self.api = "https://api.telegram.org/bot" + self.TOKEN + "/"
        self.updatesURL = self.api+"getUpdates"
        self.sendURL = self.api+"sendMessage"

    def sendMessage(self, chatId, message):
        requests.post(self.sendURL + "?chat_id="+str(chatId)+"&text="+message)

    def getToken(self):
        return self.TOKEN

    def extract_result(self, dict):
        result_array = dict['result']

        if result_array == []:
            return False
        else:
            result_dic = result_array[0]
            return result_dic

    def getUpdate(self):
        url = self.updatesURL
        try:
            update_raw = requests.get(url + "?offset="+str(self.OFFSET))
            update = update_raw.json()

            rsult = []

            result_array = update['result']

            if result_array == []:
                return False

            result_dic = result_array[0]
            rsult = result_dic

            #rsult = extract_result(update)

            if rsult != False:
                self.OFFSET = rsult['update_id'] + 1

                #chatId = rsult['message']['chat']['id']
                #text = rsult['message']['text']

                return rsult
        except requests.exceptions.ConnectionError:
            return True
        return False

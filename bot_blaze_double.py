import datetime
import requests
import telebot
import time
import json
import csv


class WebScraper:
    
    def __init__(self):
        # EDIT!
        self.game = "Blaze Double"
        self.token = "" # config
        self.chat_id = "" # config
        self.url_API = "https://blaze-1.com/api/roulette_games/recent"
        self.gales = 2
        self.protection = True
        self.link = "[Clique aqui!](blaze.com/r/0aJYR6)"

        # MAYBE EDIT!
        self.win_results = 0
        self.branco_results = 0
        self.loss_results = 0
        self.max_hate = 0
        self.win_hate = 0

        # NO EDIT!
        self.count = 0
        self.analisar = True
        self.direction_color = "None"
        self.message_delete = False
        self.bot = telebot.TeleBot(token=self.token, parse_mode="MARKDOWN")
        self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))
        self.check_date = self.date_now

    def restart(self):
        if self.date_now != self.check_date:
            print("Reiniciando bot!")
            self.check_date = self.date_now

            self.bot.send_sticker(
                self.chat_id,
                sticker="CAACAgEAAxkBAAEBbJJjXNcB92-_4vp2v0B3Plp9FONrDwACvgEAAsFWwUVjxQN4wmmSBCoE",
            )
            self.results()

            # ZERA OS RESULTADOS
            self.win_results = 0
            self.loss_results = 0
            self.branco_results = 0
            self.max_hate = 0
            self.win_hate = 0
            time.sleep(10)

            self.bot.send_sticker(
                self.chat_id,
                sticker="CAACAgEAAxkBAAEBPQZi-ziImRgbjqbDkPduogMKzv0zFgACbAQAAl4ByUUIjW-sdJsr6CkE",
            )
            self.results()
            return True
        else:
            return False

    def results(self):
        if self.win_results + self.branco_results + self.loss_results != 0:
            a = (
                100
                / (self.win_results + self.branco_results + self.loss_results)
                * (self.win_results + self.branco_results)
            )
        else:
            a = 0
        self.win_hate = f"{a:,.2f}%"

        self.bot.send_message(
            chat_id=self.chat_id,
            text=(
                f"""

► PLACAR = ✅{self.win_results} | ⚪️{self.branco_results} | 🚫{self.loss_results} 
► Consecutivas = {self.max_hate}
► Assertividade = {self.win_hate}
    
    """
            ),
        )
        return

    def alert_sinal(self):
        message_id = self.bot.send_message(
            self.chat_id,
            text="""
⚠️ ANALISANDO, FIQUE ATENTO!!!
""",
        ).message_id
        self.message_ids = message_id
        self.message_delete = True
        return

    def alert_gale(self):
        self.message_ids = self.bot.send_message(
            self.chat_id, text=f"""⚠️ Vamos para o {self.count}ª GALE"""
        ).message_id
        self.message_delete = True
        return

    def delete(self):
        if self.message_delete == True:
            self.bot.delete_message(chat_id=self.chat_id, message_id=self.message_ids)
            self.message_delete = False

    def send_sinal(self):
        self.analisar = False
        self.bot.send_message(
            chat_id=self.chat_id,
            text=(
                f"""

🎲 *ENTRADA CONFIRMADA!*

🎰 Apostar no {self.direction_color}
⚪️ Proteger no Branco
🔁 Fazer até {self.gales} gales

📱 *{self.game}* """
                f"{self.link}"
                """

    """
            ),
        )
        return

    def martingale(self, result):
        if result == "WIN":
            print(f"WIN")
            self.win_results += 1
            self.max_hate += 1
            # self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAEBuhtkFBbPbho5iUL3Cw0Zs2WBNdupaAACQgQAAnQVwEe3Q77HvZ8W3y8E')
            self.bot.send_message(chat_id=self.chat_id, text=(f"""✅✅✅ WIN ✅✅✅"""))

        elif result == "LOSS":
            self.count += 1

            if self.count > self.gales:
                print(f"LOSS")
                self.loss_results += 1
                self.max_hate = 0
                # self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAEBuh9kFBbVKxciIe1RKvDQBeDu8WfhFAACXwIAAq-xwEfpc4OHHyAliS8E')
                self.bot.send_message(chat_id=self.chat_id, text=(f"""🚫🚫🚫 LOSS 🚫🚫🚫"""))

            else:
                print(f"Vamos para o {self.count}ª gale!")
                self.alert_gale()
                return

        elif result == "BRANCO":
            print(f"BRANCO")
            self.branco_results += 1
            self.max_hate += 1
            # self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAEBuiNkFBbYDjGessfawWa3v9i4Kj35sgACQAUAAmq0wEejZcySuMSbsC8E')
            self.bot.send_message(chat_id=self.chat_id, text=(f"""✅✅✅ BRANCO ✅✅✅"""))

        self.count = 0
        self.analisar = True
        self.results()
        self.restart()
        return

    def check_results(self, results):
        if results == "B" and self.protection == True:
            self.martingale("BRANCO")
            return
        elif results == "B" and self.protection == False:
            self.martingale("LOSS")
            return

        if results == "B" and self.direction_color == "⚪️":
            self.martingale("EMPATE")
            return

        elif results != "B" and self.direction_color == "⚪️":
            self.martingale("LOSS")
            return

        if results == "V" and self.direction_color == "🔴":
            self.martingale("WIN")
            return
        elif results == "V" and self.direction_color == "⚫️":
            self.martingale("LOSS")
            return

        if results == "P" and self.direction_color == "⚫️":
            self.martingale("WIN")
            return
        elif results == "P" and self.direction_color == "🔴":
            self.martingale("LOSS")
            return

    def start(self):
        check = []
        while True:
            try:
                self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))

                results = []
                time.sleep(1)

                response = requests.get(self.url_API)
                json_data = json.loads(response.text)



                for i in json_data:
                    results.append(i['roll'])

                if check != results:
                    check = results
                    self.delete()
                    self.estrategy(results)

            except Exception as e:
                print("ERROR - 404!", e)
                continue

    def estrategy(self, results):
        finalnum = results
        finalcor = []

        for i in results:
            if i >= 1 and i <= 7:
                finalcor.append("V")
            elif i >= 8 and i <= 14:
                finalcor.append("P")
            else:
                finalcor.append("B")

        print(finalnum[0:10])
        print(finalcor[0:10])

        if self.analisar == False:
            self.check_results(finalcor[0])
            return

        # EDITAR ESTRATÉGIAS
        elif self.analisar == True:
            # ESTRATÉGIAS COM BASE NO CSV
            with open("bot_blaze_estrategy.csv", newline="") as f:
                reader = csv.reader(f)

                ESTRATEGIAS = []

                for row in reader:
                    string = str(row[0])
                    split_string = string.split("=")

                    lista = split_string[0].split("-")
                    aposta = list(split_string[1])

                    count = 0
                    sinal = True
                    estrategias = lista[::-1]
                    
                    for i in estrategias:
                        if i == "X" or i == finalcor[count] or i == str(finalnum[count]):
                            pass
                        else:
                            sinal = False

                        count += 1

                    if sinal == True:
                        if aposta[0] == "P":
                            self.direction_color = "⚫️"
                        elif aposta[0] == "V":
                            self.direction_color = "🔴"
                        elif aposta[0] == "B":
                            self.direction_color = "⚪️"

                        print("Sinal encontrado", estrategias, self.direction_color)
                        self.send_sinal()
                        return

                    count = 0
                    alerta = True
                    alertas = estrategias[1:]
                    
                    for i in alertas:
                        if i == "X" or i == finalcor[count] or i == str(finalnum[count]):
                            pass
                        else:
                            alerta = False
                        count += 1

                    if alerta == True:
                        print("ALERTA POSSIVEL SINAL")
                        self.alert_sinal()
                        return


scraper = WebScraper()
scraper.start()

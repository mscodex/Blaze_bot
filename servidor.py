from requests.adapters import HTTPAdapter, Retry
from flask import Flask, request
import mysql.connector
import webbrowser
import requests
import time
import json

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504, 104],
    allowed_methods=["HEAD", "POST", "PUT", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/87.0.4280.88 Safari/537.36"
}

class Blaze_AUTO:
    def __init__(self):
        self.user = {
                'email':'',
                'senha':'',
                'token':'',
                'wallet_id':''
            }

    def version(self):
        try:
            con = mysql.connector.connect(
                host='mxvinvest.com', user='mxvinv71_admin', password='@Xz25w09', database='mxvinv71_xxxx')
            cursor = con.cursor()
            cursor.execute(
                f'SELECT * FROM version WHERE name = "BLAZE_AUTO"')
            result = cursor.fetchone()
            if result:
                if result[2] != 1001:
                    print(f"Upgrade - version {result[2]} not available.")
                    time.sleep(5)
                    webbrowser.open('https://t.me/bymscodex')
                    return False
                
                else:
                    print(f"Version {result[2]} working.")
                    return True
            else:
                return False
        except:
            print("Upgrade - version not available.")
            time.sleep(5)
            webbrowser.open('https://t.me/bymscodex')
            while True:
                pass
            
    def send_request(self, method, url, **kwargs):
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.5,
                      status_forcelist=[500, 502, 503, 504])
        session.mount("http://", HTTPAdapter(max_retries=retry))
        session.mount("https://", HTTPAdapter(max_retries=retry))
        session.request(method, url, **kwargs)

    def send_request_two(self, method, url, **kwargs):
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session.request(method, url, **kwargs)
    
    def make_request(self, url, headers, post=None, req_type="GET"):
        """
        Make a request to the given url with the given headers.

        Args:
            url (str): The url to make the request to.
            headers (dict): The headers to use in the request.
            post (dict): The post data to use in the request.

        Returns:
            The response from the request.
        """
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.5,
                      status_forcelist=[500, 502, 503, 504])
        session.mount("http://", HTTPAdapter(max_retries=retry))
        session.mount("https://", HTTPAdapter(max_retries=retry))

        if req_type == "GET":
            response = session.get(url, headers=headers)
        elif req_type == "POST" and post is not None:
            response = session.post(url, headers=headers, data=post)
        elif req_type == "PUT" and post is not None:
            response = session.put(url, headers=headers, data=post)

        return response

    def get_history_data(self):
        """
        Get the data from the double data page.

        Returns:
            The data from the double data page.
        """
        url = "https://blaze-4.com/api/roulette_games/recent"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36",
        }
        response = self.make_request(url, headers)
        return response.json()

    def get_roulete_data(self):
        """
        Get the data from the roulete page.

        Returns:
            The data from the roulete page.
        """
        url = "https://blaze-4.com/api/roulette_games/current"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36",
        }
        response = self.make_request(url, headers)
        return response.json()

    def make_bet(self, color, value, token, wallet_id):

        while True:
            url = requests.get('https://api-v2.blaze-4.com/roulette_games/current')
            results = url.json()
            self.status = results['status']

            if self.status == 'waiting':  # JOGADORES APOSTANDO
                self.status = 'NONE'
                break

            elif self.status == 'rolling':  # BLAZE GIRANDO
                while self.status == 'rolling':
                    try:
                        url = requests.get(
                            'https://api-v2.blaze-4.com/roulette_games/current')
                        results = url.json()
                        self.status = results['status']
                    except:
                        continue

            elif self.status == 'complete':  # BLAZE GIROU
                while self.status == 'complete':
                    try:
                        url = requests.get(
                            'https://api-v2.blaze-4.com/roulette_games/current')
                        results = url.json()
                        self.status = results['status']
                    except:
                        continue



        """
        Make a bet on the roulete.

        """
        url = "https://blaze-4.com/api/roulette_bets"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {token}",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://blaze-4.com",
            "referer": "https://blaze-4.com/pt/games/double",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36",
        }

        data = {}
        data["amount"] = round(float("{:,.2f}".format(value)), 2)
        data["currency_type"] = "BRL"
        data["color"] = color
        data["free_bet"] = False
        data["wallet_id"] = wallet_id
        bet_payload = json.dumps(data)

        response = self.make_request(
            url, headers, bet_payload, req_type="POST")
        if response.status_code == 200:
            # print(f"[Bot] - Aposta: {'WHITE'if color == 0 else 'BLACK' if color == 2 else 'RED'} - Valor: R$ {data['amount']} Confirmada!")
            # ultimaApostaId = ultimoResultadoId
            # corAposta = color
            return {'message':'Bet send'}
        else:
            error_message = response.json()["error"]
            with open("Erros_aposta.txt", "a") as f:
                f.write(f"{error_message} - cor = {color} - valor = {value}\n")
            # print(error_message)
            # print(f"[Bot] - Aposta: {'WHITE'if color == 0 else 'BLACK' if color == 2 else 'RED'} - Valor: R$ {data['amount']} Erro!")
            return response.json()["error"]

    def get_user_info(self, token):
        """
        Get the user info.

        Returns:
            The user info.
        """
        url = "https://blaze-4.com/api/users/me"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36",
        }
        user_data_request = self.make_request(url, headers)

        url = "https://blaze-4.com/api/wallets"
        wallet_data_request = self.make_request(url, headers)

        user_data = {}
        if user_data_request.status_code == 200 or wallet_data_request.status_code == 200:
            account_data = user_data_request.json()
            wallet_data = wallet_data_request.json()
            user_data["username"] = account_data["username"]
            user_data["balance"] = "{:,.2f}".format(
                float(wallet_data[0]["balance"]))
            user_data["wallet_id"] = wallet_data[0]["id"]
            user_data["tax_id"] = account_data["tax_id"]
            return user_data

    def get_code(self):
        try:
            try:
                url = requests.get(
                    f"http://api.mxvinvest.com:8867/hcaptcha/token")
            except:
                return False
                
            if url.status_code == 500:
                return False
            elif url.status_code == 200:
                return json.loads(url.content)
        except:
            print("Erro ao conectar!")
            return False

    def authorization(self, username, password):
        global headers
        global is_logged

        # a = self.get_code()
        data = {
            "username": username,
            "password": password
        }
        # headers["x-captcha-response"] = f"{a}"
        headers["referer"] = f"https://blaze-4.com/pt/?modal=auth&tab=login"
        response = self.send_request_two("PUT",
                                f"https://blaze-4.com/api/auth/password",
                                json=data,
                                headers=headers)

        if not response.json().get("error"):
            token = response.json()["access_token"]

            return token
        return response.json()

    def get_blaze_token(self, email, password):
        ba = self.authorization(email, password)
        try:
            return ba
        except:
            print("Email ou senha incorreto.")
            return False

    def get_bet_result(self, id):
        """
        Get the bet result.

        Args:
            id (str): The bet id.

        Returns:
            The bet result.
        """
        url = f"https://blaze-4.com/api/roulette_games/{id}?page=1"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36",
        }
        response = self.make_request(url, headers)
        return response.json()

    def getToken(self, email, senha):
        try:
            token = self.get_blaze_token(email, senha)
            return token
        except:
            return False

    def getUser(self, token):
        # loop = asyncio.get_event_loop()
        return self.get_user_info(token)

    def apostar(self, cor, valor, token, wallet_id):
        # 0 = branco / 1 = vermelho / 2 = preto
        return self.make_bet(cor, valor, token, wallet_id)

    def getHistorico(self):
        hist = self.get_history_data()

        historicoCores = [f"{result.get('color')}".replace("0", "b").replace("1", "v").replace("2", "p")
                          for result in hist]
        # inverte lista
        historicoCores = historicoCores[::-1]
        return historicoCores

    def getUltimoResultado(self):
        hist = self.get_history_data()
        return hist[0]

    def getStatusRoleta(self):
        # waiting - rolling - complete
        return self.get_roulete_data()

    def getResultado(self, id):
        return self.get_bet_result(id)

    def start(self):
        # Cria uma instância do Flask
        app = Flask(__name__)

        # Define uma rota para a página inicial
        @app.route('/')
        def home():
            webbrowser.open('https://t.me/bymscodex')
            return 'Bem vindo!'

        #http://127.0.0.1:3333/login?email=EMAIL&senha=SENHA
        @app.route('/login')
        def login():
            try:
                email = request.args.get('email')
                senha = request.args.get('senha')
                token = self.authorization(email, senha)
                user = self.getUser(token)

                self.user = {
                    'email':email,
                    'senha':senha,
                    'token':token,
                    'wallet_id':user['wallet_id']
                }
                self.version()
                return 'Login successful'
            except:
                self.version()
                self.user = {
                    'email':'',
                    'senha':'',
                    'token':'',
                    'wallet_id':''
                }
                return False

        #http://127.0.0.1:3333/bet?color=v&value=0.1
        @app.route('/bet')
        def bet():
            try:
                color = request.args.get('color')
                value = float(request.args.get('value'))
                token =  self.user['token']
                wallet_id = self.user['wallet_id']

                if color == "b" or color == "B":
                    colorx = 0

                elif color == "v" or color == "V":
                    colorx = 1

                elif color == "p" or color == "P":
                    colorx = 2
                
                else:
                    return 'Error color.'

                bet = self.make_bet(colorx, value, token, wallet_id)
                return bet['message']
            except:
                self.version()
                return f'URL Error!'

        #http://127.0.0.1:3333/balance
        @app.route('/balance')
        def balance():
            try:
                user = self.getUser(self.user['token'])
                if user:
                    return user['balance']
                else:
                    return 'Error get balance.'
            except:
                return('Error get balance.')

        # Executa o servidor Flask
        if __name__ == '__main__':
            app.run(host='0.0.0.0', port=3333)

MainBOT = Blaze_AUTO()
MainBOT.start()
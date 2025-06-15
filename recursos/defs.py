import pyttsx3
import pickle
import os
import datetime
import speech_recognition as sr

LOG_PATH = "log.dat"

def speak(text):
    """
    Fala o texto recebido usando pyttsx3.
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Erro ao falar:", e)

def salvar_partida(pontuacao, nome_jogador):
    """
    Salva a pontuação, nome e data/hora da partida no arquivo log.dat.
    """
    partida = {
        "nome": nome_jogador,
        "pontuacao": pontuacao,
        "datahora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    partidas = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "rb") as f:
            try:
                partidas = pickle.load(f)
            except:
                partidas = []
    partidas.insert(0, partida)
    partidas = partidas[:5]
    with open(LOG_PATH, "wb") as f:
        pickle.dump(partidas, f)

def ler_ultimas_partidas():
    """
    Lê as últimas 5 partidas do arquivo log.dat.
    """
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "rb") as f:
        try:
            return pickle.load(f)
        except:
            return []

def reconhecer_nome():
    """
    Usa o microfone para reconhecer o nome do jogador via voz.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Diga seu nome...")
            audio = r.listen(source, timeout=5)
            nome = r.recognize_google(audio, language='pt-BR')
            print("Você disse:", nome)
            return nome
        except sr.UnknownValueError:
            print("Não entendi o que você disse. Tente novamente.")
            return ""
        except sr.RequestError:
            print("Erro de conexão com o serviço do Google. Verifique sua internet.")
            return ""
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido. Fale mais rápido.")
            return ""
        except Exception as e:
            print("Erro inesperado:", e)
            return ""
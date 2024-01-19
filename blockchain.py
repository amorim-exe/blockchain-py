import hashlib
import time
import json
from flask import Flask, request

class Bloco:
    def __init__(self, indice, hash_anterior, timestamp, dados, hash):
        self.indice = indice
        self.hash_anterior = hash_anterior
        self.timestamp = timestamp
        self.dados = dados
        self.hash = hash

def calcular_hash(indice, hash_anterior, timestamp, dados):
    bloco_string = f"{indice}{hash_anterior}{timestamp}{json.dumps(dados)}"
    return hashlib.sha256(bloco_string.encode()).hexdigest()

def criar_bloco_genesis():
    return Bloco(0, "0", time.time(), "Bloco Genesis", calcular_hash(0, "0", time.time(), "Bloco Genesis"))

def criar_novo_bloco(bloco_anterior, dados):
    indice = bloco_anterior.indice + 1
    timestamp = time.time()
    hash = calcular_hash(indice, bloco_anterior.hash, timestamp, dados)
    return Bloco(indice, bloco_anterior.hash, timestamp, dados, hash)

# Classe simples de blockchain
class Blockchain:
    def __init__(self):
        self.corrente = [criar_bloco_genesis()]

    def obter_ultimo_bloco(self):
        return self.corrente[-1]

    def adicionar_bloco(self, bloco):
        self.corrente.append(bloco)

# Aplicação web Flask para interagir com a blockchain
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def minerar():
    ultimo_bloco = blockchain.obter_ultimo_bloco()
    novos_dados = "Novo Bloco #{}".format(ultimo_bloco.indice + 1)
    novo_bloco = criar_novo_bloco(ultimo_bloco, novos_dados)
    blockchain.adicionar_bloco(novo_bloco)
    resposta = {
        'mensagem': 'Bloco minerado com sucesso!',
        'indice': novo_bloco.indice,
        'hash': novo_bloco.hash,
        'hash_anterior': novo_bloco.hash_anterior,
        'timestamp': novo_bloco.timestamp,
        'dados': novo_bloco.dados
    }
    return json.dumps(resposta), 200

@app.route('/chain', methods=['GET'])
def obter_corrente():
    dados_corrente = []
    for bloco in blockchain.corrente:
        dados_corrente.append({
            'indice': bloco.indice,
            'hash': bloco.hash,
            'hash_anterior': bloco.hash_anterior,
            'timestamp': bloco.timestamp,
            'dados': bloco.dados
        })
    resposta = {
        'corrente': dados_corrente,
        'tamanho': len(dados_corrente)
    }
    return json.dumps(resposta), 200

if __name__ == '__main__':
    app.run(port=5000)

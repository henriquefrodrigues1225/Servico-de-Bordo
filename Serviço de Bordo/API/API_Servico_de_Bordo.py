# -*- coding: utf-8 -*-

# Importando os módulos necessários do Flask.
# Flask: O núcleo do nosso micro-framework web.
# jsonify: Para converter dicionários Python para o formato JSON, o padrão de comunicação em APIs REST.
# request: Para acessar os dados enviados na requisição (por exemplo, o número do assento e o lanche escolhido).
from flask import Flask, jsonify, request
from flask_cors import CORS # Importa o CORS

# --- Configuração da Aplicação ---
# Em um ambiente de produção na Azul, usaríamos configurações mais avançadas,
# mas para este projeto, a inicialização padrão é suficiente.
app = Flask(__name__)

# Habilitando o CORS. Isso é crucial para permitir que seu front-end (HTML/CSS/JS),
# que rodará em uma origem diferente, possa fazer requisições para esta API.
CORS(app)


# --- Camada de Dados ---
# Em um sistema real, esses dados viriam de um banco de dados (ex: PostgreSQL, Oracle).
# Para este protótipo, vamos mantê-los em memória como variáveis globais.
# Isso simula o "estado" do nosso serviço de bordo.

SNACKS = {
    1: {"name": 'Amendoim', "image_url": '/static/IMG/Amendoim.png'},
    2: {"name": 'Aviõezinhos', "image_url": '/static/IMG/Aviaozin.png'}, 
    3: {"name": 'Bolinho', "image_url": '/static/IMG/bolo.png'},
    4: {"name": 'Bolinho Sabor Laranja', "image_url": '/static/IMG/Bolinho.png'},
    5: {"name": 'Batatinhas Chips', "image_url": '/static/IMG/Chips.png'},
    6: {"name": 'Cookie Integral', "image_url": '/static/IMG/Cookie.png'},
    7: {"name": 'Goiabinha Integral', "image_url": '/static/IMG/Goiabinha.png'},
    8: {"name": 'Maçã', "image_url": '/static/IMG/Maca.png'},
    9: {"name": 'Pão na Chapa', "image_url": '/static/IMG/Pao.png'},
    10: {"name": 'Polvilho Salgado', "image_url": '/static/IMG/Polvilho.png'},
    11: {"name": 'Queijo Integral', "image_url": '/static/IMG/Queijo.png'},
    12: {"name": 'Torresminho', "image_url": '/static/IMG/Torresminho.png'}
}

# Estrutura de dados otimizada. Usar um dicionário com o número do assento como chave
# permite acesso direto e mais rápido (O(1)) do que percorrer uma lista (O(n)).
# Isso é uma otimização de performance importante em sistemas de larga escala.
ASSENTOS = {
    1: {"Status": 'Topázio', "Pedidos": 0},
    2: {"Status": 'Básico', "Pedidos": 0},
    3: {"Status": 'Básico', "Pedidos": 0},
    4: {"Status": 'Diamante', "Pedidos": 0},
    5: {"Status": 'Safira', "Pedidos": 0},
    6: {"Status": 'Safira', "Pedidos": 0},
    10: {"Status": 'Básico', "Pedidos": 0},
    22: {"Status": 'Topázio', "Pedidos": 0},
    23: {"Status": 'Topázio', "Pedidos": 0}
}


# --- Definição dos Endpoints da API (Nossas "Rotas") ---

@app.route('/api/snacks', methods=['GET'])
def get_snacks():
    """
    Endpoint para listar todos os snacks disponíveis.
    Método HTTP: GET
    Retorno: Um objeto JSON com a lista de snacks.
    """
    # A boa prática é sempre retornar uma resposta JSON estruturada.
    return jsonify({"snacks": SNACKS})

@app.route('/api/assentos', methods=['GET'])
def get_assentos():
    """
    Endpoint para consultar o status de todos os assentos.
    Método HTTP: GET
    Retorno: Um objeto JSON com os dados dos assentos.
    """
    return jsonify({"assentos": ASSENTOS})

@app.route('/api/pedido', methods=['POST'])
def realizar_pedido():
    """
    Endpoint para processar um novo pedido de snack.
    Método HTTP: POST (pois esta ação "cria" um novo pedido e modifica o estado do sistema).
    Corpo da Requisição (JSON esperado):
    {
        "assento_id": <numero>,
        "snack_id": <numero>
    }
    """
    # Extrai os dados JSON enviados pelo cliente (front-end).
    dados_pedido = request.get_json()

    # --- Validação de Entrada ---
    # É fundamental validar os dados recebidos para garantir a integridade do sistema.
    if not dados_pedido or "assento_id" not in dados_pedido or "snack_id" not in dados_pedido:
        # Retornamos um código de status HTTP 400 (Bad Request) para indicar um erro do cliente.
        return jsonify({"status": "erro", "mensagem": "Estrutura da requisição inválida."}), 400

    assento_id = dados_pedido["assento_id"]
    snack_id = dados_pedido["snack_id"]

    # Verifica se o assento e o snack existem em nossa "base de dados".
    if assento_id not in ASSENTOS:
        return jsonify({"status": "erro", "mensagem": f"Assento {assento_id} não encontrado."}), 404 # Not Found
    if snack_id not in SNACKS:
        return jsonify({"status": "erro", "mensagem": f"Snack com ID {snack_id} é inválido."}), 400

    # --- Lógica de Negócio ---
    # Esta é a lógica principal do seu sistema, agora adaptada para o contexto da API.
    assento = ASSENTOS[assento_id]
    
    # A regra para clientes 'Básico'
    if assento["Status"] == 'Básico' and assento["Pedidos"] > 0:
        return jsonify({
            "status": "recusado",
            "mensagem": "Seu plano de fidelidade permite apenas um snack por viagem."
        }), 403 # Forbidden

    # Se a regra de negócio permitir, o pedido é processado.
    assento["Pedidos"] += 1
    
    # --- Resposta de Sucesso ---
    # Retornamos um código de status HTTP 200 (OK) e uma mensagem de sucesso.
    return jsonify({
        "status": "sucesso",
        "mensagem": f"Pedido do snack '{SNACKS[snack_id]["name"]}' para o assento {assento_id} realizado com sucesso!",
        "dados_assento": assento
    })

# --- Ponto de Entrada da Aplicação ---
# Este bloco garante que o servidor de desenvolvimento do Flask só será iniciado
# quando o script for executado diretamente.
if __name__ == '__main__':
    # app.run() inicia o servidor.
    # debug=True é útil durante o desenvolvimento, pois reinicia o servidor automaticamente
    # a cada alteração no código e fornece mais detalhes sobre erros.
    # Em produção, essa opção deve ser desativada.
    app.run(debug=True, port=5000)
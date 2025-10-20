document.addEventListener('DOMContentLoaded', () => {

    // URL base da nossa API. Em um ambiente real, isso viria de um arquivo de configuração.
    const API_URL = 'http://127.0.0.1:5000/api';

    // Cria um objeto para facilmente buscar parâmetros da URL (query string).
    const urlParams = new URLSearchParams(window.location.search);
    // Pega o valor do parâmetro 'assento'. Será null se não existir.
    const MEU_ASSENTO_ID = urlParams.get('assento');

    // Referências aos elementos HTML que vamos manipular.
    const snacksContainer = document.getElementById('snacks-container');
    const btnPedir = document.getElementById('btn-pedir');
    const mensagemStatus = document.getElementById('mensagem-status');
    const meuAssentoContainer = document.getElementById('meu-assento-status-container');
    const tituloPedido = document.getElementById('titulo-pedido');

    // Valida se o ID do assento foi encontrado na URL e atualiza a interface.
    if (MEU_ASSENTO_ID) {
        tituloPedido.textContent = `Serviço de Bordo - Assento ${MEU_ASSENTO_ID}`;
    } else {
        tituloPedido.textContent = 'Erro: Assento Não Identificado';
        // Desabilita funcionalidades se não sabemos qual é o assento.
        btnPedir.disabled = true;
        btnPedir.style.backgroundColor = '#ccc';
        exibirMensagem('Acesse a página com a identificação do seu assento na URL (ex: .../index.html?assento=4)', 'erro');
    }
    
    /**
     * Função para buscar os snacks da API e criar os cartões visuais.
     */
    async function carregarSnacks() {
        try {
            const response = await fetch(`${API_URL}/snacks`);
            const data = await response.json();
            snacksContainer.innerHTML = ''; // Limpa a mensagem "Carregando...".

            for (const id in data.snacks) {
                // Agora 'snack' é um objeto com 'name' e 'image_url'
                const snack = data.snacks[id];
                
                const card = document.createElement('div');
                card.className = 'snack-card';
                
                // Usamos 'dataset' para armazenar o ID do snack.
                card.dataset.snackId = id;

                // ATUALIZADO: Criamos o HTML interno do cartão com imagem e nome.
                // Usamos template literals (crases ``) para facilitar a montagem.
                card.innerHTML = `
                    <img src="${API_URL.replace('/api', '')}${snack.image_url}" alt="${snack.name}">
                    <span>${snack.name}</span>
                `;

                // Adiciona o evento de clique para a seleção.
                card.addEventListener('click', () => {
                    const currentSelected = document.querySelector('.snack-card.selected');
                    if (currentSelected) {
                        currentSelected.classList.remove('selected');
                    }
                    card.classList.add('selected');
                });

                snacksContainer.appendChild(card);
            }

        } catch (error) {
            console.error('Erro ao carregar snacks:', error);
            snacksContainer.innerHTML = '<p class="erro">Não foi possível carregar os snacks.</p>';
        }
    }

    /**
     * Função para buscar os dados de todos os assentos, mas renderizar apenas o assento atual.
     */
    async function carregarMeuAssento() {
        if (!MEU_ASSENTO_ID) return;

        try {
            const response = await fetch(`${API_URL}/assentos`);
            const data = await response.json();
            const meuAssento = data.assentos[MEU_ASSENTO_ID];

            if (meuAssento) {
                meuAssentoContainer.innerHTML = '';
                const card = document.createElement('div');
                
                // --- SOLUÇÃO APLICADA ---
                // 1. Converte para minúsculas
                // 2. Normaliza para remover acentos
                const statusNormalizado = normalizarString(meuAssento.Status.toLowerCase());
                
                card.className = `assento-card status-${statusNormalizado}`;

                card.innerHTML = `
                    <div class="numero">Assento ${MEU_ASSENTO_ID}</div>
                    <div class="status">Status Fidelidade: <strong>${meuAssento.Status}</strong></div>
                    <div class="pedidos">Snacks Pedidos: <strong>${meuAssento.Pedidos}</strong></div>
                `;
                meuAssentoContainer.appendChild(card);
            } else {
                // ... (resto do código sem alterações)
            }
        } catch (error) {
            // ... (resto do código sem alterações)
        }
    }

    /**
     * Função para enviar o pedido para a API.
     */
    async function enviarPedido() {
        // Procura pelo cartão que tem a classe 'selected' para saber a escolha do usuário.
        const selectedCard = document.querySelector('.snack-card.selected');

        if (!MEU_ASSENTO_ID) {
            exibirMensagem('Assento não identificado. Não é possível fazer o pedido.', 'erro');
            return;
        }
        
        if (!selectedCard) {
            exibirMensagem('Por favor, selecione um snack clicando em uma das opções.', 'erro');
            return;
        }

        // Pega o ID do snack que guardamos no 'dataset' do cartão selecionado.
        const snackId = selectedCard.dataset.snackId;

        try {
            const response = await fetch(`${API_URL}/pedido`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    assento_id: parseInt(MEU_ASSENTO_ID),
                    snack_id: parseInt(snackId)
                })
            });

            const resultado = await response.json();

            if (response.ok) {
                exibirMensagem(resultado.mensagem, 'sucesso');
                // Após o pedido, atualiza o status do assento para refletir a mudança.
                carregarMeuAssento();
            } else {
                exibirMensagem(resultado.mensagem, 'erro');
            }

        } catch (error) {
            console.error('Erro ao enviar pedido:', error);
            exibirMensagem('Erro de comunicação com o servidor.', 'erro');
        }
    }
    
    /**
     * Função auxiliar para exibir mensagens de status na tela.
     */
    function exibirMensagem(texto, tipo) {
        mensagemStatus.textContent = texto;
        mensagemStatus.className = tipo; // Aplica a classe CSS 'sucesso' ou 'erro'.
    }

    // --- Ponto de Entrada: Eventos e Inicialização ---

    // Adiciona o "ouvinte" de evento ao botão de confirmação.
    btnPedir.addEventListener('click', enviarPedido);

        /**
     * Normaliza uma string, removendo acentos e diacríticos.
     * @param {string} str A string a ser normalizada.
     * @returns {string} A string sem acentos.
     */
    function normalizarString(str) {
        return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }

    // Chama as funções para carregar os dados iniciais assim que a página é aberta.
    carregarSnacks();
    carregarMeuAssento();
});
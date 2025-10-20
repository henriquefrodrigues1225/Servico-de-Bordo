document.addEventListener('DOMContentLoaded', () => {
    // Pega os elementos do HTML
    const searchButton = document.getElementById('search-button');
    const flightCodeInput = document.getElementById('flight-code-input');
    const resultContainer = document.getElementById('flight-result-container');
    const allFlightsContainer = document.getElementById('all-flights-list-container'); // Novo container

    // --- FUNÇÃO PARA BUSCAR UM VOO ESPECÍFICO (poucas mudanças) ---
    const fetchFlightStatus = async () => {
        const flightCode = flightCodeInput.value.trim().toUpperCase();
        if (!flightCode) {
            alert('Por favor, digite um código de voo.');
            return;
        }
        resultContainer.innerHTML = '<p class="placeholder">Buscando dados do voo...</p>';
        try {
            const apiUrl = `http://127.0.0.1:8000/status/${flightCode}`;
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error('Voo não encontrado. Verifique o código e tente novamente.');
            }
            const data = await response.json();
            displayFlightData(data);
        } catch (error) {
            displayError(error.message);
        }
    };

    // --- NOVA FUNÇÃO PARA BUSCAR TODOS OS VOOS ---
    const fetchAllFlights = async () => {
        try {
            const apiUrl = 'http://127.0.0.1:8000/status/all';
            const response = await fetch(apiUrl);

            if (!response.ok) {
                throw new Error('Não foi possível carregar a lista de voos.');
            }
            const flights = await response.json();
            displayAllFlights(flights);

        } catch (error) {
            allFlightsContainer.innerHTML = `<p class="placeholder" style="color: red;">${error.message}</p>`;
        }
    };

    // --- NOVA FUNÇÃO PARA EXIBIR A LISTA DE TODOS OS VOOS ---
    const displayAllFlights = (flights) => {
        // Se não houver voos, exibe uma mensagem
        if (flights.length === 0) {
            allFlightsContainer.innerHTML = '<p class="placeholder">Nenhum voo programado para hoje.</p>';
            return;
        }

        // Limpa a mensagem "Carregando..."
        allFlightsContainer.innerHTML = '';

        // Cria um card para cada voo na lista
        flights.forEach(flight => {
            const { info_voo, status_calculado } = flight;
            const statusSlug = status_calculado.split(' ')[0].toLowerCase();

            const miniCardHtml = `
                <div class="mini-flight-card">
                    <div class="info">
                        <strong>${info_voo.codigo_voo}</strong>
                        <p>${info_voo.origem} → ${info_voo.destino}</p>
                    </div>
                    <div class="mini-status-tag status-${statusSlug}">
                        ${status_calculado.replace('Adiado - ', '')}
                    </div>
                </div>
            `;
            allFlightsContainer.innerHTML += miniCardHtml;
        });
    };
    
    // Funções para exibir o resultado da busca (inalteradas)
    const displayFlightData = (data) => {
        const { info_voo, status_calculado } = data;
        const statusClass = 'status-' + status_calculado.split(' ')[0].toLowerCase();
        let delayedHtml = '';
        if (info_voo.status === 'Adiado') {
            delayedHtml = `
                <div class="delayed-info">
                    <p><strong>Nova Partida:</strong> ${info_voo.nova_partida}</p>
                    <p><strong>Nova Chegada:</strong> ${info_voo.nova_chegada}</p>
                </div>
            `;
        }
        const flightCardHtml = `
            <div class="flight-card ${statusClass}">
                <h3>
                    ${info_voo.codigo_voo}
                    <span class="status-tag">${status_calculado}</span>
                </h3>
                <div class="flight-info">
                    <p><strong>Origem:</strong> ${info_voo.origem}</p>
                    <p><strong>Destino:</strong> ${info_voo.destino}</p>
                    <p><strong>Data:</strong> ${info_voo.dia_partida}</p>
                    <p><strong>Partida Programada:</strong> ${info_voo.partida_programada}</p>
                    <p><strong>Chegada Programada:</strong> ${info_voo.chegada_programada}</p>
                    <p><strong>Tipo de Voo:<strong> ${info_voo.voo}<p>
                </div>
                ${delayedHtml}
            </div>
        `;
        resultContainer.innerHTML = flightCardHtml;
    };

    const displayError = (message) => {
        const errorHtml = `<div class="flight-card status-erro"><p>${message}</p></div>`;
        resultContainer.innerHTML = errorHtml;
    };

    // Event Listeners
    searchButton.addEventListener('click', fetchFlightStatus);
    flightCodeInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            fetchFlightStatus();
        }
    });

    // --- RODA A FUNÇÃO PARA CARREGAR TODOS OS VOOS QUANDO A PÁGINA ABRIR ---
    fetchAllFlights();
});
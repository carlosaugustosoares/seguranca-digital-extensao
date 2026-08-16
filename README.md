# Quiz de Segurança Digital

Projeto educativo em Python para uma atividade de extensão.

## Inclui
- Quiz com 5 perguntas.
- Explicação de cada resposta.
- SQLite para guardar respostas.
- Código anônimo por participante.
- Dashboard protegido por senha.
- Indicadores e barras de desempenho por pergunta.
- Exportação CSV.
- QR Code para celulares na mesma rede Wi-Fi.

## Instalação
No terminal, dentro da pasta do projeto:

    pip install -r requirements.txt

## Executar

    python app.py

O terminal mostrará o endereço do computador e da rede Wi-Fi.

Computador: http://000.0.0.0:0000
Dashboard: http://000.0.0.0:0000/admin
Senha inicial: seguranca123

## Celulares
1. Conecte computador e celulares à mesma rede Wi-Fi.
2. Execute `python app.py`.
3. Entre no dashboard no computador.
4. Clique em QR Code.
5. Os participantes escaneiam o QR Code.
6. Mantenha o terminal do Flask aberto durante a atividade.

O projeto não pede nome, telefone ou e-mail dos participantes.

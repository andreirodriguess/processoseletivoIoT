## Relatório do Candidato

### Identificação do Candidato

- **Nome completo: Andrei Luiz da Silva Rodrigues**
- **GitHub: https://github.com/andreirodriguess**

---

## Visão Geral da Solução

O objetivo do projeto é simular um contador de produção não intrusivo, para ser aplicado como uma solução industrial de baixo custo para linhas de montagem. Utilizando um sensor óptico para detectar a passagem de peças em uma esteira, incrementando o valor de um contador ao longo de seu funcionamento. O sistema também pode ser resetado conforme necessário, por meio de um botão, e é capaz de detectar travamentos na esteira de produtos e alertar caso uma peça obstrua a fonte de luz por tempo prolongado. O usuário pode interagir com a simulação controlando a intensidade luminosa (dada em Lux) e avaliando as saídas de acordo com a maior ou menor quantidade, indicando a passagem de objetos pela esteira.  


---

## Arquitetura do Sistema Embarcado

* Fluxo principal do programa (`main.py`):  
 O código roda em um laço infinito (`while True`), lendo os dados do sensor óptico a cada ciclo, atualizando a máquina de estados da esteira e verificando o estado lógico do botão de reset, acionando as devidas rotinas para cada tarefa.
* Estrutura de estados, loops e temporizações:  
 Utilizando variáveis de controle (como `bloqueado` e `tempo_inicio_passagem`), gerenciam-se as transições da esteira, avaliando se ela está livre ou bloqueada. Utilizam-se temporizações não-bloqueantes para avaliar se a esteira está parada por um intervalo crítico (emitindo o alerta de micro-parada) e para realizar o debounce do botão, averiguando há quanto tempo foi apertado, além de identificar o momento exato em que é solto.
* Interação entre os componentes:   
O ESP32 recebe os dados analógicos do sensor óptico e os converte via ADC pela GPIO 33, enquanto recebe o estado lógico do botão de reset pela GPIO 19. Utilizando esses dados, o ESP32 controla os estados da aplicação e envia registros na saída serial sobre a situação atual da linha (alertas de micro-parada e confirmação de reset).
---

## Componentes Utilizados na Simulação

1. **Microcontrolador (`board-esp32-devkit-c-v4`):**
Foi responsável pelo processamento dos dados, pela comunicação serial (emitindo alertas e avisos quando necessário) e pela contagem de tempo, interagindo diretamente com os periféricos.
2. **Botão (`wokwi-pushbutton`):**
Utilizado para o reset e configurado na GPIO 19 do ESP32, zerava o valor das variáveis de controle quando pressionado, permitindo ao usuário resetar o turno. Configurado utilizando o resistor interno de Pull-up.
3. **Sensor Fotorresistor LDR (`wokwi-photoresistor-sensor`):**
Atua na detecção de objetos na esteira, enviando dados analógicos para a GPIO 33 do microcontrolador com informações sobre a intensidade da iluminação, a qual, quando reduzida, indica a presença de um objeto na esteira.

---

## Decisões Técnicas Relevantes
1. **Mapeamento por faixas**
Como o projeto só precisava lidar com certos níveis de intensidade de luminosidade, e como havia uma imprecisão no sensor fotorresistor que tornava difícil a criação de um algoritmo 100% eficiente na conversão do valor digital em bits para o valor correto em Lux, foi decidido fazer uma análise empírica das saídas para determinados valores em Lux escolhidos na simulação Wokwi. Com esses dados, foi possível identificar quando a luminosidade estava abaixo de certos níveis, indicando se a esteira estava ou não bloqueada.

Por exemplo, após a leitura do sensor em um ambiente com 500 Lux de intensidade (limite que indicava esteira livre), a saída convertida no algoritmo era de 750 Lux devido à imprecisão do sensor. Optou-se, nesse caso, por converter todas as saídas abaixo de 750 Lux para um valor abaixo de 500, como 480 Lux. Isso foi aplicado em todos os limites de luminosidade, permitindo que o projeto funcionasse corretamente mesmo sem uma conversão exata. Foi uma decisão de engenharia na qual o problema foi resolvido de forma eficiente, sem a necessidade de criar um algoritmo complexo para lidar com a queda logarítmica do valor da saída do sensor.

2. **Decisões gerais**
Para organizar o fluxo do sistema, utilizaram-se variáveis de controle no gerenciamento dos estados do botão e no monitoramento de travamentos da esteira (registrando há quanto tempo o sensor permaneceu obstruído). Temporizações não-bloqueantes foram empregadas para identificar micro-paradas e realizar o debounce do botão. A solução foi modularizada em funções dedicadas para a leitura/conversão do sensor LDR e para o tratamento do botão de reset. Por fim, constantes foram definidas para armazenar parâmetros imutáveis, como os limiares de luminosidade (Lux) e o tempo limite para disparo dos alertas.

---

## Resultados Obtidos

O projeto funcionou conforme o esperado. O valor obtido do sensor foi convertido de forma proporcional à intensidade da luz, e a imprecisão da conversão foi devidamente tratada por software.

Os requisitos foram atendidos com sucesso, sendo eles:

1. **Alerta de micro-parada**
Dispara corretamente após 5 segundos de bloqueio contínuo da esteira.
2. **Contagem:**
Funciona corretamente, contabilizando o produto apenas quando a luminosidade supera o valor pré-definido para esteira livre (500 Lux) após ter ficado abaixo do limite de bloqueio (100 Lux).
3. **Botão de reset:**
Funciona perfeitamente, emitindo o aviso serial correspondente e zerando as variáveis de controle para reiniciar o turno.
4. **Validação no Wokwi CI:**
O projeto obteve aprovação total nos testes automatizados executados via GitHub Actions.

Todos os requisitos e comportamentos foram testados e validados empiricamente no simulador Wokwi.

---

## Comentários Adicionais (Opcional)
1. **Aplicabilidade**
A solução é aplicável na indústria real, contudo, precisaria de alguns reajustes dependendo do ambiente em que fosse instalada.
2. **Maior adversidade encontrada**
A maior dificuldade encontrada deveu-se ao comportamento do sensor fotorresistor (LDR), cuja resposta varia de forma logarítmica em relação à luminosidade. Isso exigiu o desenvolvimento de uma solução via software para contornar essa não-linearidade e adequar a leitura ao cenário da simulação.
3. **Melhorias no hardware**
Em uma aplicação industrial real, seria mais eficiente a substituição do LDR por um sensor óptico infravermelho ou laser industrial. Isso eliminaria a interferência da luz ambiente e dispensaria o tratamento analógico complexo.
4. **Principais aprendizados**
O projeto foi de grande valia para a consolidação prática no uso de sensores fotorresistores (LDR) e na aplicação de um ambiente de desenvolvimento padronizado via Docker. O uso do container facilitou significativamente o gerenciamento de dependências, a reprodutibilidade do ambiente e a eficiência em todo o processo de programação do sistema embarcado.
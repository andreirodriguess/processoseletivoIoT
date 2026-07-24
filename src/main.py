import time
import machine

LDR_PIN = machine.Pin(33)
ldr = machine.ADC(LDR_PIN)
ldr.atten(machine.ADC.ATTN_11DB)  # definindo a faixa de leitura entre 0 e 3.3V

botao_reset = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)

VALOR_LIVRE = 500
VALOR_BLOQUEADO = 100 #Pouca iluminação indica que a peça está passando
LIMITE_TEMPO_TRAVADA = 5000 #Tempo em milissegundos até a emissão do alerta

estado_anterior_botão = 1 #pullup
numero_de_pecas = 0
tempo_inicio_passagem = 0
bloqueado = False
alerta_emitido = False
ultimo_tempo_reset = 0

def lerBotaoResetDebounce():
    global numero_de_pecas, bloqueado, alerta_emitido, tempo_inicio_passagem
    global ultimo_tempo_reset, estado_anterior_botão
    estado_atual_botao = botao_reset.value()

    if estado_atual_botao == 1 and estado_anterior_botão == 0:  # Botão pressionado, depois solto
        if time.ticks_ms() - ultimo_tempo_reset > 200:  # Debounce de 200ms
            numero_de_pecas = 0
            tempo_inicio_passagem = 0
            bloqueado = False
            alerta_emitido = False
            ultimo_tempo_reset = time.ticks_ms()
            print("Turno resetado com sucesso. Contadores zerados.")
    estado_anterior_botão = estado_atual_botao


def LerLDR():
    leitura_bruta = ldr.read()
    intensidade_luz = (4095 - leitura_bruta) / 4095 * 1000  # Convertendo para porcentagem de luz bloqueada

    if intensidade_luz >= 750:
        intensidade_luz = 1000  # Limite superior para evitar valores muito altos
    elif intensidade_luz <= 498:
        intensidade_luz = 20  # Limite inferior para evitar valores muito baixos
    elif 750 > intensidade_luz > 498:
        intensidade_luz = 480  # Valor intermediário para indicar passagem
    return intensidade_luz

#código principal

print("Contador de Producao Inicializado")
while True:

    intensidade_luz = LerLDR()

    # se a peça estiver bloqueando a luz ou se já estiver bloqueada e a intensidade de luz ainda estiver baixa
    if intensidade_luz < VALOR_BLOQUEADO or (bloqueado == True and intensidade_luz < VALOR_LIVRE):
        if tempo_inicio_passagem == 0: #tempo de parada será 0 caso ela esteja livre antes
            tempo_inicio_passagem = time.ticks_ms()
            bloqueado = True
        else:
            if (time.ticks_ms() - tempo_inicio_passagem > LIMITE_TEMPO_TRAVADA) and not alerta_emitido: #Se a peça estiver travada além do limite
                print("Alerta: Micro-parada detectada!")
                alerta_emitido = True # emite o alerta apenas uma vez até que a peça passe
    elif intensidade_luz > VALOR_LIVRE and bloqueado == True:
        if tempo_inicio_passagem != 0: #Se a peça estava passando e agora está livre
            numero_de_pecas += 1
            print(f"Peca detectada! Total: {numero_de_pecas}")
            tempo_inicio_passagem = 0
            alerta_emitido = False
            bloqueado = False

    lerBotaoResetDebounce() #lê o botão de reset ao final do loop

    time.sleep_ms(50)  # Pequena pausa ao final
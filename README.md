## Relatório do Candidato

O arquivo **`README.md` do seu repositório** deve ser utilizado como o  
**relatório final do desafio técnico**.

Preencha todas as seções abaixo de forma **clara, objetiva e técnica**.

> **Dica importante**  
> Não é necessário um relatório extenso.  
> O principal critério é demonstrar **clareza nas decisões técnicas**, organização e entendimento do sistema embarcado desenvolvido.
> Não mantenha os demais conteúdos escritos nesse arquivo README, aqui devem ser concentradas apenas informações referentes ao projeto desenvolvido.

---

### Identificação do Candidato

- **Nome completo: Andrei Luiz da Silva Rodrigues**
- **GitHub: https://github.com/andreirodriguess**

---

## Visão Geral da Solução

O objetivo do projeto é simular um contador de produção não intrusivo, para ser aplicado como uma solução industrial de baixo custo para linhas de montagem. Utilizando um sensor óptico para detectar a passagem de peças em uma esteira, incrementando o valor de um contador ao longo de seu funcionamento. O sistema também pode ser resetado conforme necessário, por meio de um botão, e é capaz de detectar travamentos na esteira de produtos e alertar caso uma peça obstrua a fonte de luz por tempo prolongado. O usuário pode interagir com a simulação controlando a intensidade luminosa (dada em Lux) e avaliando as saídas de acordo com a maior ou menor quantidade, indicando a passagem de objetos pela esteira.  


---

## Arquitetura do Sistema Embarcado

Explique a arquitetura lógica do seu projeto, abordando:



- Fluxo principal do programa (`main.py`)
- Estrutura de estados, loops ou temporizações
- Como os componentes interagem entre si

Se desejar, utilize tópicos ou um pequeno diagrama em texto.

---

## Componentes Utilizados na Simulação

Liste os principais componentes definidos no `diagram.json`, por exemplo:

- Tipo de placa utilizada
- LEDs, botões, sensores, atuadores, etc.
- Função de cada componente no sistema

---

## Decisões Técnicas Relevantes

Explique brevemente decisões importantes tomadas durante o desenvolvimento, como:

- Organização do código
- Uso de funções, estados ou constantes
- Estratégias para temporização ou controle lógico

---

## Resultados Obtidos

Descreva o comportamento final do sistema:

- O que funciona corretamente
- Quais requisitos foram atendidos
- Resultado observado na simulação do Wokwi

---

## Comentários Adicionais (Opcional)

Utilize este espaço para comentar, se desejar:

- Dificuldades encontradas
- Limitações da solução
- Melhorias que você faria com mais tempo
- Principais aprendizados durante o desafio

---

> Este relatório faz parte da avaliação técnica.  
> Clareza, objetividade e organização são tão importantes quanto o funcionamento do código.

---

## Especificação dos Testes Automatizados (Wokwi CI)

Para que o projeto seja validado com sucesso na esteira de integração contínua (CI), o firmware escrito em MicroPython deve interagir corretamente com as leituras dos sensores descritos em cada cenário e enviar as mensagens de status exatas.

### Requisitos Críticos de Implementação

1. **Casamento Exato de Strings:** O Wokwi CI faz uma verificação estrita caractere por caractere. Se houver divergência em maiúsculas/minúsculas, acentuação ou falta de pontuação, o teste irá falhar.
2. **Arquitetura Não-Bloqueante:** Evite o uso de funções bloqueantes. Elas podem fazer com que o firmware perca a janela de tempo em que o simulador altera o peso, quebrando a sincronia do teste automatizado.

---

## Suporte

Em caso de dúvidas:

- Consulte o material dos cursos EAD
- Leia atentamente este README
- Analise os logs das GitHub Actions
- Utilize os canais oficiais para contato com os instrutores

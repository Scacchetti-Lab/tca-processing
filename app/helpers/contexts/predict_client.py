from app.types.predict_models import MeetingStrategicDto


def make_predict_client_context(
    client,
    current_analysis,
    strategic_history: list["MeetingStrategicDto"],
) -> str:
    if current_analysis is not None:
        bloco_agregado = f"""Media consolidada de {current_analysis.meetings_analysed} reuniao(oes), ultima analise em {current_analysis.last_analysis_at}:
- Performance: {current_analysis.performance}
- Probabilidade de fechamento: {current_analysis.closing_probability}
- Flexibilidade: {current_analysis.flexibility}
- Risco: {current_analysis.risk}
- Impacto financeiro: R$ {current_analysis.financial_impact} ({current_analysis.financial_status})"""
    else:
        bloco_agregado = "(nenhuma analise estrategica registrada ainda -- cliente sem reunioes analisadas ate o momento)"

    if strategic_history:
        linhas_historico = "\n".join(
            f"{i}. performance={h.closing_probability}, flexibilidade={h.flexibility}, "
            f"risco={h.risk}, impacto_financeiro=R${h.financial_impact} ({h.financial_impact_status}) | "
            f"feedback: {h.feedback}"
            for i, h in enumerate(strategic_history, start=1)
        )
    else:
        linhas_historico = "(nenhuma reuniao estrategica registrada ainda)"

    return f"""CLIENTE: {client.name} ({client.fantasy_name})
Status atual registrado: {client.status}
Faturamento mensal: R$ {client.revenue}

ESTADO AGREGADO ATUAL:
{bloco_agregado}

HISTORICO COMPLETO DE ANALISES ESTRATEGICAS (da mais antiga para a mais recente):
{linhas_historico}"""


def build_client_prediction_instruction(root_company_name: str = 'TOTVS') -> str:
    return f"""Voce e um analista preditivo de relacionamento comercial B2B da {root_company_name}. Voce recebe o estado agregado atual e o historico completo de analises estrategicas de um cliente ja existente na base, e precisa prever o RUMO GERAL do relacionamento -- expansao, estabilidade, ou risco de perda -- alem de recomendar como a equipe deve conduzir esse relacionamento daqui para frente.

FORMATO DE SAIDA: retorne APENAS o texto da previsao, em um paragrafo corrido, sem titulo, sem marcadores, sem introducao tipo "aqui esta a previsao". So o conteudo.

REGRAS:

1. USE APENAS O QUE FOI FORNECIDO. Nunca invente fato, numero ou evento que nao esteja nos dados recebidos. Se o cliente nao tiver nenhuma analise registrada ainda, diga isso explicitamente e limite-se a uma leitura muito cautelosa baseada so no que se sabe do cadastro (status, faturamento) -- nunca preencha a lacuna com suposicao sobre como o relacionamento provavelmente esta indo.

2. VOCE NUNCA CALCULA NUMERO NENHUM. As metricas que voce recebe (agregadas ou por reuniao) ja foram calculadas por um sistema externo. Sua funcao e interpretar o que elas sugerem sobre o futuro, nunca propor um novo numero, media ou percentual.

3. CALIBRE A CONFIANCA PELA QUANTIDADE DE HISTORICO. O estado agregado e uma MEDIA -- ele pode vir de 1 reuniao so ou de muitas, e o campo que informa quantas reunioes compoem a media esta disponivel no bloco de estado agregado. Baseado nisso, uma leitura sobre 1-2 reunioes deve soar cautelosa; historico maior com direcao consistente pode sustentar leitura mais assertiva.

4. DISTINGA MEDIA DE TENDENCIA. O bloco de estado agregado descreve a situacao atual consolidada -- nao fale dele como se fosse uma unica reuniao. Ja o historico completo, ordenado cronologicamente, e onde voce enxerga DIRECAO: risco subindo ou descendo ao longo das reunioes, probabilidade de fechamento evoluindo, temas recorrentes nos feedbacks (mesma reclamacao varias vezes, mesma promessa nao cumprida). Cruzar os dois -- "a media atual e X, e a tendencia recente aponta para Y" -- da uma leitura mais rica do que qualquer um dos dois sozinho.

5. USE O FATURAMENTO PARA DIMENSIONAR GRAVIDADE, NUNCA PARA CALCULAR NADA. Um mesmo nivel de risco importa mais para um cliente de faturamento alto do que para um de faturamento baixo -- isso deve se refletir no tom e na urgencia da recomendacao, nao em nenhum numero novo.

6. TERMINE COM ORIENTACAO PRATICA. O texto deve deixar claro nao so a leitura da trajetoria, mas o que a equipe deveria fazer -- manter, expandir, ou agir sobre um risco -- de forma especifica ao que foi observado, nunca conselho generico."""
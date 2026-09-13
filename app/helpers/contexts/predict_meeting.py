from app.types.predict_models import MeetingPerformanceDto, MeetingStrategicDto


def make_predict_meeting_context(
    client,
    performance_history: list["MeetingPerformanceDto"],
    strategic_history: list["MeetingStrategicDto"],
) -> str:
    """
    Monta o texto que vai como 'input' da chamada ao Gemini para prever uma
    reuniao futura -- historico do cliente (estrategico + desempenho do time),
    ambos ja vem ordenados do mais antigo para o mais recente pelo repository.
    """
    if strategic_history:
        linhas_estrategico = "\n".join(
            f"{i}. probabilidade_fechamento={h.closing_probability}, flexibilidade={h.flexibility}, "
            f"risco={h.risk}, impacto_financeiro=R${h.financial_impact} ({h.financial_impact_status}) | "
            f"feedback: {h.feedback}"
            for i, h in enumerate(strategic_history, start=1)
        )
    else:
        linhas_estrategico = "(nenhuma analise estrategica registrada ainda -- primeira interacao com esse cliente)"

    if performance_history:
        linhas_desempenho = "\n".join(
            f"{i}. engajamento={h.engagement}, comunicacao={h.communication_quality}, "
            f"aproveitamento={h.opportunities_seized}, tratamento_objecoes={h.objection_handling}, "
            f"erros={h.missed_opportunities} | dicas: {h.tips} | feedback: {h.feedback}"
            for i, h in enumerate(performance_history, start=1)
        )
    else:
        linhas_desempenho = "(nenhuma analise de desempenho registrada ainda)"

    return f"""CLIENTE: {client.name} ({client.fantasy_name})
Status atual registrado: {client.status}

HISTORICO ESTRATEGICO COM ESSE CLIENTE (saude do relacionamento, da mais antiga para a mais recente):
{linhas_estrategico}

HISTORICO DE DESEMPENHO DO TIME NAS REUNIOES COM ESSE CLIENTE (da mais antiga para a mais recente):
{linhas_desempenho}"""


def build_meeting_prediction_instruction(root_company_name: str = 'TOTVS') -> str:
    return f"""Voce e um analista preditivo de relacionamento comercial B2B da {root_company_name}. Voce recebe o historico completo de um cliente (analises estrategicas e de desempenho de reunioes ja realizadas) e precisa prever, para a PROXIMA reuniao com esse cliente, o que provavelmente sera discutido, quais riscos e oportunidades merecem atencao, e como o time deveria se preparar.

FORMATO DE SAIDA: retorne APENAS o texto da previsao, em um paragrafo corrido, sem titulo, sem marcadores, sem introducao tipo "aqui esta a previsao". So o conteudo.

REGRAS:

1. USE APENAS O QUE FOI FORNECIDO. Nunca invente fato, numero ou evento que nao esteja no historico recebido. Se o historico vier vazio ou muito curto, diga isso explicitamente no texto e reduza a confianca da sua leitura -- nao compense a falta de dado com suposicao.

2. VOCE NUNCA CALCULA NUMERO NENHUM. As metricas que voce recebe ja foram calculadas por um sistema externo. Sua funcao e interpretar o que elas sugerem, nunca propor um novo numero, media ou percentual.

3. CALIBRE A CONFIANCA PELA QUANTIDADE DE HISTORICO. Uma leitura baseada em 1 ou 2 reunioes deve soar cautelosa ("com base no pouco historico disponivel..."). Historico de 3 ou mais reunioes com direcao consistente pode sustentar uma leitura mais assertiva.

4. OBSERVE TENDENCIA, NAO SO O ESTADO ATUAL. O historico esta ordenado da mais antiga para a mais recente -- note se risco, probabilidade de fechamento, engajamento ou objecoes estao melhorando ou piorando ao longo das reunioes, e se ha tema recorrente nos feedbacks (mesma reclamacao, mesma promessa nao cumprida).

5. TERMINE COM ORIENTACAO PRATICA. O texto deve deixar claro nao so o que esperar, mas o que o time deveria fazer de diferente ou confirmar antes dessa proxima reuniao."""
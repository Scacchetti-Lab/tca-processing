import pandas as pd
from os import getcwd
from app.services import transcripts_service as trs, gemini_client_service as gen
from app.models.transcripts_models import TranscriptAnalyse
from fastapi import status, HTTPException
from pydantic import ValidationError

def main():
    df = pd.read_csv(f'{getcwd().replace('\\', '/')}/assets/anon_transcription.csv')
    transcript = df['ANON_TRANSCRICAO'].tolist()[0]
    print('\n\033[1;93m[EM ANDAMENTO] Analisando e Limpando Transcrição\033[m')
    cleaned_transcript = trs.clean_transcript(transcript)
    print('\033[1;32m[CONCLUÍDO] Analise e limpeza de transcrição!\033[m')
    try:
        print('\n\n\033[1;93m[EM ANDAMENTO] Analise do Gemini 3.6 Flash...\033[m')
        response = gen.analyse_transcript(cleaned_transcript)
        print('\033[1;32m[CONCLUÍDO] Analise do Gemini 3.6 Flash!\033[m')

        if (response.status != status.HTTP_200_OK):
            raise HTTPException(
                status_code=response.status,
                detail=response.message
            )
        transcript_analyzed = TranscriptAnalyse.model_validate_json(response.message)

        print(transcript_analyzed)

    except HTTPException as httpex:
        print('\033[1;31m[FALHA] Ocorreu algum problema no processo...\033[m')
        print(httpex.status_code)
        print(httpex.detail)

    except ValidationError as vex:
        print('\033[1;31m[FALHA] Ocorreu algum problema no processo...\033[m')
        error = vex.errors()[0]

        print('\n' + error['msg'])
        print(f'[{error['loc']}]: {error['input']}')

    except Exception as ex:
        print('\033[1;31m[FALHA] Ocorreu algum problema no processo...\033[m')
        print(ex)


if __name__ == "__main__":
    main()

'''

PRIMEIRA ANALISE DA IA

status='OK' 
type='SALER' 
score_type='PERFORMANCE' 
basic_description=TranscriptDescription(
    company_name='[EMPRESA] (Cliente do Segmento de Saúde)', 

    company_representor='TOTVS (Engenharia de Vendas e Comercial)', 

    duration_min=60, 

    stakeholders=['Locutor 102 (Engenharia de Vendas - TOTVS)', 'Locutor 49 (Comercial - TOTVS)', 'Locutor 3 ([PESSOA] Mesquita - Gerente de RH/DP)', 'Locutor 72 ([PESSOA] - Supervisor de Operações/RH)', 'Locutor 63 ([PESSOA] - TI/Infraestrutura)'], 
    
    meeting_summary='Reunião de apresentação comercial e demonstraçãotécnica dos módulos Meu RH e Ponto da TOTVS para cliente do setor hospitalar/saúde (folha de aproximadamente 10 mil colaboradores). O cliente busca substituir um portal interno deponto e necessita entender o funcionamento do sistema focado no perfil de gestor, incluindo controle de ponto, fluxos de aprovação de horas extras, relatórios e integração/homologação de atestados médicos com o SESMT. Houve um desalinhamento prévio, pois a apresentação foi focada na visão do colaborador. A equipe comercial assumiu o compromisso de coletar os requisitos específicos e agendar uma nova sessão com a Engenharia de Valor antes do dia 24 de março.', 
    
    insights=Insights(
        priority='HIGH', 

        comment='A evolução da compra do módulo Meu RH/Ponto depende da realização de uma nova demonstração focada na visão do gestor e do esclarecimento das regras de negócio (homologação de atestados pelo SESMT e aprovações dehoras extras pelo DP) até o dia 24 de março.', grade=8)
    ) 
    
    analytic=AnalayseCustomerDefinitions(
        engagement=8.0, 

        opportunities_seized=6.5, 

        communication_quality=7.5, 

        objection_handling=7.0, 

        converted_potencials=6.0, 

        leads_converted=0, 

        tips='Antes de reuniões de demonstração, realize um alinhamento prévio minucioso sobre o escopo desejado (ex: visão do gestor vs. visão do colaborador) e resgate o histórico comercial do cliente. Ao identificar demandas técnicas complexas e customizações de processo (como SESMT e relatórios específicos de horas extras), acione prontamente a Engenharia de Valor para preparar um ambiente personalizado.'
    ) 
    
    feedback='A reunião evidenciou um forte interesse do cliente em contratar as soluções de ponto e autosserviço da TOTVS para sua operação de 10.000 funcionários. No entanto, o cliente expressou frustração com o histórico de trocas no atendimento comercial e pela apresentação não ter atendido de imediato à sua principal necessidade: a gestão sob a perspectiva do gestor. O risco de estagnação da negociação é moderado se o prazo não for cumprido. Como próximo passo acionável, a equipe comercial deve organizar os requisitos recebidos do cliente, acionar a Engenharia de Valor e realizar a nova demonstração técnica antesde 24 de março.'
'''
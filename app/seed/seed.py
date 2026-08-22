import pandas as pd
from os import getcwd
from app.services import transcripts_service as trs, gemini_client_service as gen
from app.types.transcripts_models import TranscriptAnalyse
from app.types.response_model import ResponseModel
from fastapi import status, HTTPException
from pydantic import ValidationError
import json

def main():
    print('\033[1;34m[INICIO] Processo de analise de transcrição!!\033[m\n\n')
    df = pd.read_csv(f'{getcwd().replace('\\', '/')}/seed/anon_transcription.json')

    n = 0
    while True:
        n = input('Digite quantos registros deseja analiar: ')
        if n.isnumeric():
            n = int(n)
            if n > 0 and n <= df.count().count():
                break
            print('Número inválido')
        else:
            print('Somente numeros são válidos')

    transcripts = df['ANON_TRANSCRICAO'].head(n).tolist()
    try:
        print('\n\033[1;93m[EM ANDAMENTO] Analisando e Limpando Transcrição\033[m')
        cleaned_transcripts = trs.clean_transcripts_batch(transcripts)
        print('\033[1;32m[CONCLUÍDO] Analise e limpeza de transcrição!\033[m')


        print('\n\n\033[1;93m[EM ANDAMENTO] Analise do Gemini 3.6 Flash...\033[m')
        analyzes: dict[str, ResponseModel] = {}
        for ct in cleaned_transcripts:
            key: str = str(df['ID_MEETING'])
            analyzes[key] = gen.analyse_transcript(ct)
        print('\033[1;32m[CONCLUÍDO] Analise do Gemini 3.6 Flash!\033[m')

        print('\n\n\033[1;93m[EM ANDAMENTO] Convertendo dados...\033[m')
        responses: dict[str, TranscriptAnalyse] = {}
        for key, ct in analyzes.items():
            if ct.status != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=ct.status,
                    detail=ct.content
                ) 
            responses[key] = TranscriptAnalyse.model_validate(ct.content)
        print('\033[1;32m[CONCLUÍDO] Conversão de dados!\033[m')


        print('\n\n\033[1;93m[EM ANDAMENTO] Escrevendo arquivo...\033[m')
        with open('analise_ia.json', 'w') as file:
            result = json.dumps(responses)
            file.write(result)
        print('\033[1;32m[CONCLUÍDO] Arquivo escrito com sucesso!\033[m')

        print('\n\n\033[1;34m[ENCERRADO] Processo finalizado!!\033[m')
            
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
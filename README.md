# tca-processing
Microserviço de processamento e análise de dados do TOTVS Commercial AI, construído com FastAPI e pandas. Responsável por tarefas de manipulação, transformação e enriquecimento de dados (ex: transcrições de reuniões, geração de embeddings para busca vetorial) que são consumidas pela API principal em Java.

## Como iniciar o docker?

```sh
docker compose up -d # No mesmo diretório do projeto com docker-compose e .env com as infos do BD
docker ps # Verifica status atual da imagem do docker, deve estar UP em status
```x
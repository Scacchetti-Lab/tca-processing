import re as _re
from cleantext import clean as __clean
import pandas as _pd
from os import getcwd as _getcwd, environ as _environ
from typing import TYPE_CHECKING
from app.helpers.is_valid_uuid import is_valid_uuid
from uuid import UUID

_RE_MULTI_NEWLINE = _re.compile(r'\n{2,}')
_RE_SPACES_TABS = _re.compile(r'[ \t]+')
_RE_SPACE_AROUND_NEWLINE = _re.compile(r' *\n *')
_RE_TAG_BLOCK_REPEAT = _re.compile(r'((?:\[[A-ZÀ-Ú_ ]+\][.,]?\s*)+?)\1+')
_RE_COLLPASED_TAGS = _re.compile(r'(\[[A-ZÀ-Ú_ ]+\])(?:[.,]?\s*\1)+')
_RE_LOCUTOR_TAG = _re.compile(r'\[LOCUTOR \d+\]:')
_RE_ANON_TAG = _re.compile(r'\[[A-ZÀ-Ú_ ]+\]')

_LOCUTOR_PLACEHOLDER = "§LOC{}§"
_ANON_PLACEHOLDER = "§ANON{}§"


USE_DB = bool(_environ['USE_DATABASE'])

if TYPE_CHECKING:
    from app.db_connect import SessionDep
    from app.repository.transcript import TranscriptRepository
    from app.models.transcript import transcript

def get_by_dataframe(id: str):
    if (not str.isnumeric(id)):
        return None
    
    df = _pd.read_json(f'{_getcwd()}/app/seed/anon_transcription.json')
    df_trs = df[df['ID_MEETING'] == int(id)]

    if df_trs.empty: 
        return None

    return str(df_trs['ANON_TRANSCRICAO'].values[0])


def get_transcript_by_id(id: str, session: SessionDep | None = None) -> str | None:
    ''''Partindo de um Id especificado, retorne a transcrição'''

    if not USE_DB:
        return get_by_dataframe(id)

    if session is None:
        raise ValueError('Variável session é null')

    transcript_repository = TranscriptRepository(session)

    if not is_valid_uuid(id):
        raise ValueError('ID fornecido é inválido')

    res = transcript_repository.get_by_id(UUID(id))
    if not res.is_valid:
        return None

    transcript_model = res.result
    if isinstance(transcript_model, transcript):
        return transcript_model.tr_raw_transcript
    return None

def clean_transcript(raw_transcript: str) -> str:
    if not raw_transcript or not raw_transcript.strip():
        return ""

    cleaned_txt = raw_transcript

    locutores = _RE_LOCUTOR_TAG.findall(cleaned_txt)
    for i, tag in enumerate(locutores):
        cleaned_txt = cleaned_txt.replace(tag, _LOCUTOR_PLACEHOLDER.format(i), 1)

    anon_tags = _RE_ANON_TAG.findall(cleaned_txt)
    for i, tag in enumerate(anon_tags):
        cleaned_txt = cleaned_txt.replace(tag, _ANON_PLACEHOLDER.format(i), 1)

    cleaned_txt = _RE_MULTI_NEWLINE.sub('\n', cleaned_txt)
    cleaned_txt = _RE_SPACES_TABS.sub(' ', cleaned_txt)
    cleaned_txt = _RE_SPACE_AROUND_NEWLINE.sub('\n', cleaned_txt)
    cleaned_txt = _RE_COLLPASED_TAGS.sub(r'\1', cleaned_txt)

    cleaned_txt = __clean(
        cleaned_txt,
        fix_unicode=True,
        to_ascii=False,        
        lower=False,           
        no_line_breaks=False,  
        no_urls=True,
        no_emails=True,
        no_phone_numbers=True,
        no_numbers=False,
        no_digits=False,
        no_currency_symbols=False,
        no_punct=False,
        no_emoji=True,
        replace_with_url="",
        replace_with_email="",
        replace_with_phone_number="",
        lang="pt",
    )

    for i, tag in enumerate(locutores):
        cleaned_txt = cleaned_txt.replace(_LOCUTOR_PLACEHOLDER.format(i), tag)
    for i, tag in enumerate(anon_tags):
        cleaned_txt = cleaned_txt.replace(_ANON_PLACEHOLDER.format(i), tag)

    cleaned_txt = _RE_TAG_BLOCK_REPEAT.sub(r'\1', cleaned_txt)

    return cleaned_txt.strip()

def clean_transcripts_batch(transcripts: list[str]) -> list[str]:
    return [clean_transcript(t) for t in transcripts]
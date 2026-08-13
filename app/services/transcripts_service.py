import re
from cleantext import clean

_RE_MULTI_NEWLINE = re.compile(r'\n{2,}')
_RE_SPACES_TABS = re.compile(r'[ \t]+')
_RE_SPACE_AROUND_NEWLINE = re.compile(r' *\n *')
_RE_TAG_BLOCK_REPEAT = re.compile(r'((?:\[[A-ZÀ-Ú_ ]+\][.,]?\s*)+?)\1+')
_RE_LOCUTOR_TAG = re.compile(r'\[LOCUTOR \d+\]:')
_RE_ANON_TAG = re.compile(r'\[[A-ZÀ-Ú_ ]+\]')

_LOCUTOR_PLACEHOLDER = "§LOC{}§"
_ANON_PLACEHOLDER = "§ANON{}§"


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

    cleaned_txt = clean(
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
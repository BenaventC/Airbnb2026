from pathlib import Path
import pandas as pd
import spacy

DATA_PATH = Path('data/reviews_select.csv')
OUT_PATH = Path('data/reviews_select_full.conllu')

SPACY_MODELS = {
    'fr': 'fr_core_news_sm',
    'en': 'en_core_web_sm',
    'es': 'es_core_news_sm',
    'de': 'de_core_news_sm',
    'pt': 'pt_core_news_sm',
    'it': 'it_core_news_sm',
}

MAX_CHARS = 2000
CHUNK_SIZE = 2000
BATCH_SIZE = 64


def load_models():
    models = {}
    for lang_code, model_name in SPACY_MODELS.items():
        try:
            models[lang_code] = spacy.load(model_name)
            print(f"[OK] modèle chargé: {lang_code} -> {model_name}")
        except Exception as exc:
            print(f"[WARN] modèle indisponible: {lang_code} -> {model_name} ({exc})")
    return models


def iter_lang_chunks(df_lang):
    total = len(df_lang)
    for start in range(0, total, CHUNK_SIZE):
        stop = min(start + CHUNK_SIZE, total)
        yield start, stop, df_lang.iloc[start:stop]


def main():
    print("Chargement des données...")
    df = pd.read_csv(DATA_PATH, index_col=0)
    df['lang_code'] = df['langue'].astype(str).str.lower().str.strip()

    nlp_models = load_models()
    keep_langs = sorted(nlp_models.keys())
    if not keep_langs:
        raise RuntimeError("Aucun modèle spaCy disponible")

    df = df[df['lang_code'].isin(keep_langs)].copy()
    df = df[df['comments'].notna()].copy()
    df['comments'] = df['comments'].astype(str).str.strip()
    df = df[df['comments'] != ''].copy()

    print(f"Reviews à annoter: {len(df)}")
    print(df['lang_code'].value_counts().to_string())

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    sent_id = 0
    token_count = 0
    review_done = 0

    with OUT_PATH.open('w', encoding='utf-8') as f:
        for lang_code in keep_langs:
            nlp = nlp_models[lang_code]
            df_lang = df[df['lang_code'] == lang_code][['comments']].copy()
            print(f"\n--- {lang_code.upper()} : {len(df_lang)} reviews ---")

            for start, stop, chunk in iter_lang_chunks(df_lang):
                texts = [text[:MAX_CHARS] for text in chunk['comments'].tolist()]
                docs = nlp.pipe(texts, batch_size=BATCH_SIZE)

                for local_idx, doc in enumerate(docs):
                    review_idx = start + local_idx

                    for sent in doc.sents:
                        sent_text = sent.text.strip()
                        if not sent_text:
                            continue

                        sent_id += 1
                        f.write(f"# sent_id = {sent_id}\n")
                        f.write(f"# lang = {lang_code}\n")
                        f.write(f"# review_index = {review_idx}\n")
                        f.write(f"# text = {sent_text}\n")

                        for token in sent:
                            token_id = token.i - sent.start + 1
                            head = 0 if token.dep_ == 'ROOT' else (token.head.i - sent.start + 1)

                            fields = [
                                str(token_id),
                                token.text.replace('\t', ' '),
                                token.lemma_ if token.lemma_ else '_',
                                token.pos_ if token.pos_ else '_',
                                token.tag_ if token.tag_ else '_',
                                '_',
                                str(head),
                                token.dep_ if token.dep_ else '_',
                                '_',
                                '_',
                            ]
                            f.write('\t'.join(fields) + '\n')
                            token_count += 1

                        f.write('\n')

                    review_done += 1

                if review_done % 10000 == 0:
                    print(f"Progression: {review_done} reviews, {sent_id} phrases, {token_count} tokens")

            print(f"Terminé {lang_code.upper()} ({review_done} reviews cumulées)")

    print("\nExport terminé")
    print(f"Fichier: {OUT_PATH}")
    print(f"Phrases: {sent_id}")
    print(f"Tokens: {token_count}")


if __name__ == '__main__':
    main()

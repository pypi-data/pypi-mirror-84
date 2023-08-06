import os
import logging
from typing import Set

from nltk import word_tokenize

from .lenerbr.config import Config
from .lenerbr.ner_model import NERModel

from .utils import get_sentence_splitter
from .special_tokens import is_specialtoken, ST_PREFIX

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf  # noqa: E402


tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


def get_config_ner():
    return Config()


def get_ner_model():
    return NERModel(get_config_ner())


# TODO: Don't build the model everytime
#     Problem: apply_batch from pipeline with serialization problems
def transform_ner(
    text: str,
    choosen_entities_types: Set[str] = set(["PESSOA",
                                            "LOCAL",
                                            "ORGANIZACAO",
                                            "JURISPRUDENCIA",
                                            "LEGISLACAO"]),
    remove_entities: bool = False,
    **kwargs
) -> str:
    '''
        Uses a NER model to analyse identify entities and remove or
        replace them with the special token prefix and their identified
        type.

        Arguments:
            :text: The text to identify entities.
            :choosen_entities_types: Set of strings with the types
                                    to be removed. They can be:
                                    PESSOA - For person names.
                                    TEMPO - for time related terms.
                                    LOCAL - For locations like countries,
                                            cities or states.
                                    ORGANIZACAO - For enterprise names.
                                    JURISPRUDENCIA - For jurisprudence
                                            related terms.
                                    LEGISLACAO - For law related terms.
            :remove_entities: Boolean, \
            true if the found entities should be removed.

        Returns:
            :replaced_text: the same text with the choosen entities
                            removed or replaced by special tokens

        Example:
        >>> CorpusHandler.transform_named_entities\
        ("Ronaldo Ribeiro de Faria - Tabelião ( PRAÇA DO DI) - TAGUATINGA")

        "ST_PESSOA ST_PESSOA ST_PESSOA ST_PESSOA - \
        Tabelião ( ST_LOCAL ST_LOCAL ST_LOCAL ) - ST_LOCAL"
    '''
    ner_model = get_ner_model()
    ner_model.logger.setLevel(logging.ERROR)

    # Must build inside function otherwise parallelization breaks
    ner_model.build()
    tf.reset_default_graph()
    config_ner = get_config_ner()
    ner_model.restore_session(config_ner.dir_model)

    sentence_splitter = get_sentence_splitter()
    sentence_splitter.train(text)

    doc_sentences = sentence_splitter.tokenize(text)
    replaced_sentences = []

    for sentence in doc_sentences:
        token_sentence = word_tokenize(sentence, language='portuguese')
        preds = ner_model.predict(token_sentence)

        for index, word in enumerate(token_sentence):

            # Removing entity types sufixes
            if preds[index][:2] in ['B-', 'I-', 'E-', 'S-']:
                preds[index] = preds[index][2:]

            if (preds[index] in choosen_entities_types
                    and not is_specialtoken(word)):

                if not remove_entities:
                    replaced_sentences.append(
                        ST_PREFIX + str(preds[index])
                    )
            else:
                replaced_sentences.append(word)

    replaced_text = " ".join(replaced_sentences)
    return replaced_text

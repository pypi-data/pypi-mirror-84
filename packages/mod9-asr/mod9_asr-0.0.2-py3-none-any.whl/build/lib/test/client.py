#!/usr/bin/env python3

import sys

# from mod9.asr import engine as speech
from mod9.asr import speech_mod9 as speech
# from mod9.asr import speech


class Mod9StreamingRequest(object):
    def __init__(self, audio_content):
        # Wrapper expects streaming audio bytes to be at `.audio_content` attribute.
        self.audio_content = audio_content


def prepare_dict_inputs():
    encoding = 'LINEAR16'
    sample_rate_hertz = 8000
    language_code = 'en-US'
    config = {
        'encoding': encoding,
        'sample_rate_hertz': sample_rate_hertz,
        'language_code': language_code,
        # 'enable_word_confidence': True,
        # 'enable_word_time_offsets': True,
        # 'max_alternatives': 2,
        'max_phrase_alternatives': 2,
        # 'enable_phrase_time_offsets': True,
    }
    # Comment out the following line to stop partial (non-final) result output.
    config = {'config': config, 'interim_results': True}
    # # Mod9
    # config = {
    #     'format': 'raw',
    #     'rate': 8000,
    #     'phrase-alternatives': True,
    #     'phrase-alternatives-max': 3,
    #     'partial': True,
    # }
    return config


def read_bytes_from_stdin(READ_IN_CHUNK_SIZE=1024):
    while True:
        yield sys.stdin.buffer.read(READ_IN_CHUNK_SIZE)


def get_responses_from_mod9():
    client = speech.SpeechClient()
    config_dict = prepare_dict_inputs()
    requests = (Mod9StreamingRequest(chunk) for chunk in read_bytes_from_stdin())
    return client.streaming_recognize(config_dict, requests)


if __name__ == '__main__':
    for response in get_responses_from_mod9():
        print(response.results[0])

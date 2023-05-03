import os
import re
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
from mutagen import File
import hashlib
import binascii

def hex2dec(hex, rev=True):
    """Convert a hexadecimal string to a decimal number"""
    if rev:
        hex = str(hex)[2:-1]
        new_hex = ''.join(reversed([hex[i:i+2] for i in range(0, len(hex), 2)]))
        new_hex = "0X" + new_hex
    else:
        new_hex = hex
    result_dec = int(new_hex,16)
    return result_dec

def read_wav_file(filename, buffer_size=2**10*8):
    file_hash = hashlib.sha256()
    info = dict()
    with open(filename, mode="rb") as f:
        info.update({
            "ChunkID": f.read(4),
            "ChunkSize": hex2dec(binascii.hexlify(f.read(4))),
            "Format": f.read(4),
            "Subchunk1ID": f.read(4),
            "Subchunk1Size": hex2dec(binascii.hexlify(f.read(4))),
            "AudioFormat": hex2dec(binascii.hexlify(f.read(2))),
            "NumChannels": hex2dec(binascii.hexlify(f.read(2))),
            "SampleRate": hex2dec(binascii.hexlify(f.read(4))),
            "ByteRate": hex2dec(binascii.hexlify(f.read(4))),
            "BlockAlign": hex2dec(binascii.hexlify(f.read(2))),
            "BitsPerSample": hex2dec(binascii.hexlify(f.read(2))),
            "Subchunk2ID": f.read(4),
            "Subchunk2Size": hex2dec(binascii.hexlify(f.read(4))),
        })
        info["data"] = f.read(info["Subchunk2Size"])
    return info



class Song:
    def __init__(self, path):
        self.path = path
        self._initialize_attributes()
        self._load_metadata()

    def _initialize_attributes(self):
        attrs = ['title', 'artist', 'album', 'date', 'genre']
        for attr in attrs:
            setattr(self, attr, 'None')
        self.lyrics = ''
        self.cover = b''
        self.sample_rate = self.bits_per_sample = self.bitrate = self.channels = self.length = 0
        self.audio_type = ''

    def _load_metadata(self):
        if not self.path:
            return
        filetype = self.path.split('.')[-1].lower()

        if filetype in ['wav', 'wave']:
            self._load_wav_metadata()
        elif filetype == 'mp3':
            self._load_mp3_metadata()
        else:
            self.audio_type = 'UNKNOWN'
            audio = File(self.path)

        self._load_lyrics()

    def _load_wav_metadata(self):
        self.audio_type = 'WAV'
        wav_info = read_wav_file(self.path)
        self._parse_wav_info(wav_info)
        audio = WAVE(self.path)
        self._parse_id3_tag(audio)
        if self.title == 'None':
            self.title = self.path.split('/')[-1].split('.')[0]

    def _load_mp3_metadata(self):
        self.audio_type = 'MP3'
        audio = MP3(self.path)
        self._parse_audio_info(audio.info)
        self._parse_id3_tag(audio)

    def _parse_audio_info(self, audio_info):
        self.sample_rate = audio_info.sample_rate
        self.channels = audio_info.channels
        self.length = audio_info.length
        self.bitrate = audio_info.bitrate

    #extract metadata from the ID3 tags which is commonly used in MP3
    def _parse_id3_tag(self, audio):
        for item in audio:
            if 'APIC' in item:
                self.cover = audio.get(item).data
            if 'USLT' in item:
                self.lyrics = str(audio.get(item))
        if audio.get('TIT2'):
            self.title = str(audio.get('TIT2'))
        if audio.get('TPE1'):
            self.artist = str(audio.get('TPE1'))
        if audio.get('TALB'):
            self.album = str(audio.get('TALB'))
        if audio.get('TDRC'):
            self.date = str(audio.get('TDRC'))
        if audio.get('TCON'):
            self.genre = str(audio.get('TCON'))

    def _parse_wav_info(self, wav_info):
        self.sample_rate = wav_info["SampleRate"]
        self.channels = wav_info["NumChannels"]
        self.bits_per_sample = wav_info["BitsPerSample"]
        self.audio_type = 'WAV'

        # Calculate the length of the song in seconds
        self.length = wav_info["Subchunk2Size"] / (self.sample_rate * self.channels * (self.bits_per_sample // 8))

    def _load_lyrics(self):
        lyrics_path = os.path.splitext(self.path)[0] + '.lrc'
        if not self.lyrics and os.path.exists(lyrics_path):
            with open(lyrics_path, "r", encoding='utf-8', errors='ignore') as f:
                self.lyrics = f.read()

    def get_lyrics_dictionary(self):
        if not self.lyrics:
            return {}
        lrc_lines = self.lyrics.splitlines()
        time_pattern = re.compile("\\[.*?]")
        lyrics_dict = {}
        for line in lrc_lines:
            matched_time = time_pattern.search(line)
            if not matched_time:
                continue

            time_str = matched_time.group()[1:-1]
            time_parts = time_str.split(":")
            if not time_parts[0].isdigit():
                continue
            timestamp = int(time_parts[0]) * 60000 + int(float(time_parts[1]) * 1000)
            lyrics_text = time_pattern.sub('', line)
            cleaned_lyrics_text = ' '.join(lyrics_text.split())
            if timestamp in lyrics_dict:
                lyrics_dict[timestamp].append(cleaned_lyrics_text)
            else:
                lyrics_dict[timestamp] = [cleaned_lyrics_text]
    
        return lyrics_dict

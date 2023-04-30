import os
import re
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
from mutagen import File
import hashlib
import binascii

def hex_to_dec(hex_str: str, reverse: bool = True) -> int:
    """
    Convert a hexadecimal string to a decimal number.
    """
    # Remove prefix "0X" if present
    hex_str = hex_str.lstrip("0x").lstrip("0X")
    # Reverse the string in pairs of two if requested
    if reverse:
        hex_str = "".join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))
    # Convert the hex string to a decimal number
    dec_num = int(hex_str, 16)
    return dec_num


def read_wav_file(filename, buffer_size=2**10*8):
    """
    Read the wave file and return its metadata.
    """
    info = {}
    with open(filename, mode="rb") as f:
        data = f.read(12)
        keys = ["ChunkID", "ChunkSize", "Format", "Subchunk1ID", "Subchunk1Size", "AudioFormat", "NumChannels", "SampleRate", "ByteRate", "BlockAlign", "BitsPerSample", "Subchunk2ID", "Subchunk2Size"]
        values = [data[0:4], int.from_bytes(data[4:8], byteorder="little"), data[8:12], data[12:16], int.from_bytes(data[16:20], byteorder="little"), int.from_bytes(data[20:22], byteorder="little"), int.from_bytes(data[22:24], byteorder="little"), int.from_bytes(data[24:28], byteorder="little"), int.from_bytes(data[28:32], byteorder="little"), int.from_bytes(data[32:34], byteorder="little"), int.from_bytes(data[34:36], byteorder="little"), data[36:40], int.from_bytes(data[40:44], byteorder="little")]
        info.update(dict(zip(keys, values)))
        info["data"] = f.read(info["Subchunk2Size"])
        file_hash = hashlib.sha256(info["data"]).hexdigest()
    return info


class Song:
    def __init__(self, path):
        self.path = path
        self.reset_attributes()
        self.load_metadata()

    def reset_attributes(self):
        self.title = 'None'
        self.artist = 'None'
        self.album = 'None'
        self.date = 'None'
        self.genre = 'None'
        self.lyrics = ''
        self.cover = b''
        self.sample_rate = 0
        self.bits_per_sample = 0
        self.bitrate = 0
        self.channels = 0
        self.length = 0
        self.audio_type = ''

    def load_metadata(self):
        if not self.path:
            return
    
    filetype = self.path.split('.')[-1].lower()
    
    if filetype in ('wav', 'wave'):
        self.audio_type = 'WAV'
        wav_info = read_wav_file(self.path)
        self.parse_wav_info(wav_info)
        audio = WAVE(self.path)
        self.parse_id3_tag(audio)
    elif filetype == 'mp3':
        self.audio_type = 'MP3'
        audio = MP3(self.path)
        self.parse_audio_info(audio.info)
        self.parse_id3_tag(audio)
    else:
        self.audio_type = 'UNKNOWN'
        audio = File(self.path)
    
    self.title = self.title or os.path.splitext(os.path.basename(self.path))[0]
    self.load_lyrics()


    def get_lyrics_dictionary(self):
        if not self.lyrics:
            return {}

        lrc_list = self.lyrics.splitlines()
        func = re.compile("\\[.*?]")
        lrc_dict = {}

        for item in lrc_list:
            searched = func.search(item)
            if not searched:
                continue

            lrc_time = searched.group()
            time_str_list = lrc_time[1:-1].split(":")
            if not time_str_list[0].isdigit():
                continue

            lrc_time_int = int(time_str_list[0]) * 60000 + int(float(time_str_list[1]) * 1000)
            lrc_text = func.sub('', item)
            lrc_text = ' '.join(lrc_text.split())

            lrc_dict.setdefault(lrc_time_int, []).append(lrc_text)

        return lrc_dict

    def parse_audio_info(self, audio_info):
        self.sample_rate, self.channels, self.length, self.bitrate = (
            audio_info.sample_rate,
            audio_info.channels,
            audio_info.length,
            audio_info.bitrate
        )

    def parse_id3_tag(self, audio):
        for item in audio:
            if item.startswith('APIC'):
                self.cover = audio.get(item).data
            elif item.startswith('USLT'):
                self.lyrics = str(audio.get(item))
            elif item.startswith('TIT2'):
                self.title = str(audio.get(item))
            elif item.startswith('TPE1'):
                self.artist = str(audio.get(item))
            elif item.startswith('TALB'):
                self.album = str(audio.get(item))
            elif item.startswith('TDRC'):
                self.date = str(audio.get(item))
            elif item.startswith('TCON'):
                self.genre = str(audio.get(item))

    def parse_wav_info(self, wav_info):
        self.sample_rate = wav_info.get('SampleRate', 0)
        self.channels = wav_info.get('NumChannels', 0)
        self.bits_per_sample = wav_info.get('BitsPerSample', 0)
        self.audio_type = 'WAV'
        self.length = wav_info.get('Subchunk2Size', 0) / (self.sample_rate * self.channels * (self.bits_per_sample // 8))

def load_lyrics(self):
    lyrics_path = os.path.splitext(self.path)[0] + '.lrc'
    if not self.lyrics and os.path.exists(lyrics_path):
        with open(lyrics_path, encoding='utf-8', errors='ignore') as f:
            self.lyrics = f.read()

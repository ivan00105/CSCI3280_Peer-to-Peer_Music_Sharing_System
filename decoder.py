import hashlib
import binascii
import pyaudio
import time
import threading
import os
import audioop
from pydub import AudioSegment

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
        info["ChunkID"] = f.read(4)
        info["ChunkSize"] = hex2dec(binascii.hexlify(f.read(4)))
        info["Format"] = f.read(4)
        info["Subchunk1ID"] = f.read(4)
        info["Subchunk1Size"] = hex2dec(binascii.hexlify(f.read(4)))
        info["AudioFormat"] = hex2dec(binascii.hexlify(f.read(2)))
        info["NumChannels"] = hex2dec(binascii.hexlify(f.read(2)))
        info["SampleRate"] = hex2dec(binascii.hexlify(f.read(4)))
        info["ByteRate"] = hex2dec(binascii.hexlify(f.read(4)))
        info["BlockAlign"] = hex2dec(binascii.hexlify(f.read(2)))
        info["BitsPerSample"] = hex2dec(binascii.hexlify(f.read(2)))
        info["Subchunk2ID"] = f.read(4)
        info["Subchunk2Size"] = hex2dec(binascii.hexlify(f.read(4)))
        #read the audio data
        audio_data = f.read(info["Subchunk2Size"])
        info["data"] = audio_data
    return info

class AudioPlayer:
    def __init__(self, wav_data, progress_callback):
        self.wav_data = wav_data
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(wav_data['BitsPerSample'] // 8),
                                  channels=wav_data['NumChannels'],
                                  rate=wav_data['SampleRate'],
                                  output=True)
        self.stop_flag = threading.Event()
        self.pause_flag = threading.Event()
        self.index = 0
        self.chunk_size = self.p.get_sample_size(self.p.get_format_from_width(self.wav_data['BitsPerSample'] // 8)) * self.wav_data['NumChannels']
        self.playing = False  # Initialize the playing attribute
        self.progress_callback = progress_callback
        self.volume = 1.0  # Initialize the volume attribute to 1.0 (100%)
        

    def pause(self):
        self.pause_flag.set()

    def resume(self):
        self.pause_flag.clear()

    def play_audio(self):
        data = self.wav_data['data']
        while self.index < len(data) and not self.stop_flag.is_set():
            if not self.pause_flag.is_set():
                if self.playing:
                    end_index = min(self.index + self.chunk_size, len(data))
                    # Apply the volume level to the audio samples
                    samples = audioop.mul(data[self.index:end_index], self.wav_data['BitsPerSample'] // 8, self.volume)
                    self.stream.write(samples)
                    self.index = end_index
                else:
                    time.sleep(0.1)
            else:
                time.sleep(0.1)

    def play(self):
        if self.playing:
            self.stop_flag.set()
            time.sleep(0.1)  # give some time for the previous thread to stop
        self.playing = True
        self.stop_flag.clear()

        playback_thread = threading.Thread(target=self.play_audio)
        playback_thread.start()

    def seek(self, percentage):
        if self.playing:
            total_length = len(self.wav_data['data'])
            self.index = int(total_length * float(percentage) / 100)

    def set_position(self, new_position):
        self.index = new_position

    def _on_audio_data(self, in_data, frame_count, time_info, status):
        start = self.index
        end = start + frame_count
        audio_data = self.wav_data['data'][start:end]
        self.index += frame_count
        return audio_data, pyaudio.paContinue

    def set_volume(self, volume):
        self.volume = volume

    def stop(self):
        self.stop_flag.set()
        time.sleep(0.1)  # give some time for the thread to stop
        self.index = 0

    def close(self):
        self.stop_flag.set()
        time.sleep(0.1)  # give some time for the thread to stop
        if not self.stream.is_stopped():
            self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()




# def read_wav_file(file_path):
#     with open(file_path, "rb") as file:
#         # Read RIFF header
#         riff_header = file.read(12)

#         # Read fmt sub-chunk
#         fmt_chunk_size = int.from_bytes(file.read(4), byteorder="little")
#         fmt_chunk_data = file.read(fmt_chunk_size)

#         # Extract relevant information from fmt sub-chunk
#         num_channels = int.from_bytes(fmt_chunk_data[2:4], byteorder="little")
#         sample_rate = int.from_bytes(fmt_chunk_data[4:8], byteorder="little")
#         bits_per_sample = int.from_bytes(fmt_chunk_data[14:16], byteorder="little")

#         # Read data sub-chunk
#         data_chunk_id = file.read(4)
#         while data_chunk_id != b"data":
#             data_chunk_size = int.from_bytes(file.read(4), byteorder="little")
#             file.read(data_chunk_size)
#             data_chunk_id = file.read(4)

#         data_chunk_size = int.from_bytes(file.read(4), byteorder="little")
#         data_chunk_data = file.read(data_chunk_size)

#     return {
#         "num_channels": num_channels,
#         "sample_rate": sample_rate,
#         "bits_per_sample": bits_per_sample,
#         "data_chunk_data": data_chunk_data,
#     }

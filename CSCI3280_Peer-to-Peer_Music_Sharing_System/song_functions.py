from PyQt5 import QtWidgets
from music_player import MusicPlayer


def song_timer():
        
        if not MusicPlayer.is_sliderPress:
            MusicPlayer.ui.label_time_start.setText(MusicPlayer.ms_to_str(MusicPlayer.player.position()))
            MusicPlayer.ui.label_time_end.setText(MusicPlayer.ms_to_str(MusicPlayer.player.duration()))
        
        if len(MusicPlayer.lrc_time_list) != 0:
            while True:
                if MusicPlayer.lrc_time_index > len(MusicPlayer.lrc_time_list) - 1:
                    break
                elif MusicPlayer.lrc_time_list[MusicPlayer.lrc_time_index] < MusicPlayer.player.position():
                    MusicPlayer.lrc_time_index += 1
                else:
                    break
            # PlayerWindow.ui.listWidget_2.verticalScrollBar().setSliderPosition(PlayerWindow.lrc_time_index - 1)
            MusicPlayer.ui.lyric_listWidget.setCurrentRow(MusicPlayer.lrc_time_index - 1)
            item = MusicPlayer.ui.lyric_listWidget.item(MusicPlayer.lrc_time_index - 1)
            MusicPlayer.ui.lyric_listWidget.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtCenter)

        
        MusicPlayer.ui.hSlider.setMaximum(MusicPlayer.player.duration())
        MusicPlayer.ui.hSlider.setMinimum(0)
        
        if not MusicPlayer.is_sliderPress:
            MusicPlayer.ui.hSlider.setValue(MusicPlayer.player.position())
        
        if MusicPlayer.player.position() == MusicPlayer.player.duration():
            print('Time over')
            MusicPlayer.play_next()

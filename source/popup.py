# -*- coding: utf-8 -*-
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class PopUp:
    def __init__(self, text):
        popup_builder = Gtk.Builder()
        popup_builder.add_from_file("glade/popup.glade")

        self.__popup_window = popup_builder.get_object("popup_window")
        self.__popup_label = popup_builder.get_object("popup_label")
        self.__popup_button = popup_builder.get_object("popup_button")

        popup_builder.connect_signals(self)

        self.__popup_label.set_label(text)

    def show(self):
        self.__popup_window.show()

    def popup_button_clicked_cb(self, button):
        self.__popup_window.destroy()

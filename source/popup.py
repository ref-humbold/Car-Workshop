# -*- coding: utf-8 -*-
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class PopUp:
    def __init__(self, text):
        popup_builder = Gtk.Builder()
        popup_builder.add_from_file("glade/popup.glade")

        self._popup_window = popup_builder.get_object("popup_window")
        self._popup_label = popup_builder.get_object("popup_label")
        self._popup_button = popup_builder.get_object("popup_button")

        self._popup_label.set_label(text)
        popup_builder.connect_signals(self)

    def show(self):
        self._popup_window.show()

    def popup_button_clicked_cb(self, button):
        self._popup_window.destroy()

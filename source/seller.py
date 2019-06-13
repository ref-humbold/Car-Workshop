# -*- coding: utf-8 -*-
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from .clients import Clients
from .commissions import Commissions
from .orders import Orders


class Seller:
    def __init__(self, conndb):
        self.conn = conndb

        sprzedawca_builder = Gtk.Builder()
        sprzedawca_builder.add_from_file("glade/seller.glade")

        self.__sprzedawca_window = sprzedawca_builder.get_object("sprzedawca_window")

        self.__sprzedawca_button_1 = sprzedawca_builder.get_object("sprzedawca_button_1")
        self.__sprzedawca_button_2 = sprzedawca_builder.get_object("sprzedawca_button_2")
        self.__sprzedawca_button_3 = sprzedawca_builder.get_object("sprzedawca_button_3")

        sprzedawca_builder.connect_signals(self)

        self.__sprzedawca_window.show()

    def sprzedawca_window_destroy_cb(self, window):
        """Zamyka okno sprzedawcy."""
        self.conn.close()
        Gtk.main_quit()

    def sprzedawca_button_1_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku zarządania zleceniami."""
        zlecenia_window = Orders(self.conn)

    def sprzedawca_button_2_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku zarządania klientami."""
        clients_window = Clients(self.conn)

    def sprzedawca_button_3_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku zarządania usługami."""
        uslugi_window = Commissions(self.conn)

# -*- coding: utf-8 -*-
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from .popup import PopUp


class Mechanic:
    def __init__(self, conndb):
        self.conn = conndb

        mechanik_builder = Gtk.Builder()
        mechanik_builder.add_from_file("glade/mechanic.glade")

        self.mechanik_window = mechanik_builder.get_object("mechanik_window")

        self.mechanik_comboboxtext1_1b = mechanik_builder.get_object("mechanik_comboboxtext1_1b")
        self.mechanik_button1_1c = mechanik_builder.get_object("mechanik_button1_1c")

        self.mechanik_comboboxtext2_1b = mechanik_builder.get_object("mechanik_comboboxtext2_1b")
        self.mechanik_comboboxtext2_2b = mechanik_builder.get_object("mechanik_comboboxtext2_2b")
        self.mechanik_comboboxtext2_3b = mechanik_builder.get_object("mechanik_comboboxtext2_3b")
        self.mechanik_button2_4a = mechanik_builder.get_object("mechanik_button2_4a")
        self.mechanik_button2_4b = mechanik_builder.get_object("mechanik_button2_4b")

        self.mechanik_comboboxtext3_1b = mechanik_builder.get_object("mechanik_comboboxtext3_1b")
        self.mechanik_entry3_2b = mechanik_builder.get_object("mechanik_entry3_2b")
        self.mechanik_button3_3a = mechanik_builder.get_object("mechanik_button3_3a")
        self.mechanik_button3_3b = mechanik_builder.get_object("mechanik_button3_3b")

        self.__load_ids(self.mechanik_comboboxtext1_1b, "zlecenia")
        self.__load_ids(self.mechanik_comboboxtext2_1b, "carparts")
        self.__load_ids(self.mechanik_comboboxtext2_2b, "uslugi")
        self.__load_ids(self.mechanik_comboboxtext2_3b, "cars")
        self.__load_ids(self.mechanik_comboboxtext3_1b, "carparts")

        mechanik_builder.connect_signals(self)

        self.mechanik_window.show()

    def __load_ids(self, comboboxtext, tablename):
        """Ładuje identyfikatory (klucze główne) z określonej tabeli do zadanego pola wyboru."""
        cur = self.conn.cursor()

        if tablename == "carparts":
            cur.execute("SELECT id FROM carparts;")
        elif tablename == "uslugi":
            cur.execute("SELECT nazwa FROM uslugi;")
        elif tablename == "cars":
            cur.execute("SELECT model FROM cars;")
        elif tablename == "zlecenia":
            cur.execute("SELECT id FROM zlecenia WHERE data_real IS NULL;")

        idents = cur.fetchall()
        self.conn.commit()
        cur.close()

        for s in [str(i[0]) for i in idents]:
            comboboxtext.append_text(s)

        comboboxtext.set_active(0)

    def mechanik_window_destroy_cb(self, window):
        """Zamyka okno mechanika."""
        self.conn.close()
        Gtk.main_quit()

    def mechanik_button1_1c_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku zakończenia zlecenia."""
        ident = self.mechanik_comboboxtext1_1b.get_active_text()  # SQL integer

        args = [int(ident)]
        cur = self.conn.cursor()

        try:
            cur.execute("UPDATE TABLE zlecenia SET data_real = now() WHERE id = %s", args)
        except:
            self.conn.rollback()
            PopUp("WYSTĄPIŁ BŁĄD WEWNĘTRZNY BAZY. PRZERWANO.").show()
        else:
            self.conn.commit()
            PopUp("ZLECENIE " + str(ident) + " ZOSTAŁO POMYŚLNIE ZAKOŃCZONE.").show()
        finally:
            cur.close()

    def mechanik_button2_4a_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku przypisania części samochodowej do usługi."""
        ident = self.mechanik_comboboxtext2_1b.get_active_text()  # SQL integer
        nazwa = self.mechanik_comboboxtext2_2b.get_active_text()  # SQL text

        args = [int(ident), nazwa]
        cur = self.conn.cursor()

        try:
            cur.execute("INSERT INTO czeusl(cze_id, usl_nazwa) VALUES(%s, %s);", args)
        except:
            self.conn.rollback()
            cur.close()
            PopUp("WYSTĄPIŁ BŁĄD WEWNĘTRZNY BAZY. PRZERWANO.").show()
        else:
            self.conn.commit()
            PopUp("POMYŚLNIE PRZYPISANO CZĘŚĆ DO USŁUGI.").show()
        finally:
            cur.close()

    def mechanik_button2_4b_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku przypisania części samochodowej do modelu samochodu."""
        ident = self.mechanik_comboboxtext2_1b.get_active_text()  # SQL integer
        model = self.mechanik_comboboxtext2_3b.get_active_text()  # SQL text

        args = [int(ident), model]
        cur = self.conn.cursor()

        try:
            cur.execute("INSERT INTO czesam(cze_id, sam_model) VALUES(%s, %s);", args)
        except:
            self.conn.rollback()
            cur.close()
            PopUp("WYSTĄPIŁ BŁĄD WEWNĘTRZNY BAZY. PRZERWANO.").show()
        else:
            self.conn.commit()
            PopUp("POMYŚLNIE PRZYPISANO CZĘŚĆ DO MODELU SAMOCHODU.").show()
        finally:
            cur.close()

    def mechanik_button3_3a_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku wyświetlenia ilości części."""
        ident = self.mechanik_comboboxtext3_1b.get_active_text()  # SQL integer

        args = [int(ident)]
        cur = self.conn.cursor()

        try:
            cur.execute("SELECT ilosc FROM carparts WHERE id = %s", args)
            wyn = cur.fetchone()[0]
        except:
            self.conn.rollback()
            cur.close()
            PopUp("WYSTĄPIŁ BŁĄD WEWNĘTRZNY BAZY. PRZERWANO.").show()
        else:
            self.conn.commit()
            PopUp("W MAGAZYNIE ZNAJDUJE SIĘ " + str(wyn) +
                  " CZĘŚCI NUMER " + str(ident) + ".").show()
        finally:
            cur.close()

    def mechanik_button3_3b_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku pobrania określonej ilości części."""
        ident = self.mechanik_comboboxtext3_1b.get_active_text()  # SQL integer
        ilosc = self.mechanik_entry3_2b.get_text()  # SQL integer

        args = [int(ilosc), int(ident)]
        cur = self.conn.cursor()

        try:
            cur.execute("UPDATE TABLE carparts SET ilosc = ilosc-%s WHERE id = %s", args)
        except:
            self.conn.rollback()
            PopUp("WYSTĄPIŁ BŁĄD WEWNĘTRZNY BAZY. PRZERWANO.").show()
        else:
            self.conn.commit()
            PopUp("POBRANO " + str(ilosc) +
                  " JEDNOSTEK CZĘŚCI NUMER " + str(ident) + ".").show()
        finally:
            cur.close()

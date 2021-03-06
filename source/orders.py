# -*- coding: utf-8 -*-
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from .popup import PopUp


class Orders:

    def __init__(self, conndb):
        self.conn = conndb

        zlecenia_builder = Gtk.Builder()
        zlecenia_builder.add_from_file("glade/orders.glade")

        self.zlecenia_window = zlecenia_builder.get_object("zlecenia_window")

        self.zlecenia_entry1_1ba = zlecenia_builder.get_object("zlecenia_entry1_1ba")
        self.zlecenia_entry1_1bc = zlecenia_builder.get_object("zlecenia_entry1_1bc")
        self.zlecenia_comboboxtext1_2b = zlecenia_builder.get_object("zlecenia_comboboxtext1_2b")
        self.zlecenia_comboboxtext1_3b = zlecenia_builder.get_object("zlecenia_comboboxtext1_3b")
        self.zlecenia_comboboxtext1_4b = zlecenia_builder.get_object("zlecenia_comboboxtext1_4b")
        self.zlecenia_button1_5b = zlecenia_builder.get_object("zlecenia_button1_5b")

        self.zlecenia_comboboxtext2_1b = zlecenia_builder.get_object("zlecenia_comboboxtext2_1b")
        self.zlecenia_comboboxtext2_2b = zlecenia_builder.get_object("zlecenia_comboboxtext2_2b")
        self.zlecenia_button2_3b = zlecenia_builder.get_object("zlecenia_button2_3b")

        self.zlecenia_comboboxtext3_1b = zlecenia_builder.get_object("zlecenia_comboboxtext3_1b")
        self.zlecenia_button3_1c = zlecenia_builder.get_object("zlecenia_button3_1c")

        self.__load_ids(self.zlecenia_comboboxtext1_3b, "clients")
        self.__load_ids(self.zlecenia_comboboxtext1_4b, "cars")
        self.__load_ids(self.zlecenia_comboboxtext2_1b, "zlecenia")
        self.__load_ids(self.zlecenia_comboboxtext2_2b, "uslugi")
        self.__load_ids(self.zlecenia_comboboxtext3_1b, "zlecenia")

        zlecenia_builder.connect_signals(self)

        self.zlecenia_window.show()

    def __load_ids(self, comboboxtext, tablename):
        """Ładuje identyfikatory (klucze główne) z określonej tabeli do zadanego pola wyboru."""
        cur = self.conn.cursor()

        if tablename == "zlecenia":
            cur.execute("SELECT id FROM zlecenia;")
        elif tablename == "clients":
            cur.execute("SELECT id FROM clients;")
        elif tablename == "cars":
            cur.execute("SELECT model FROM cars;")
        elif tablename == "uslugi":
            cur.execute("SELECT nazwa FROM uslugi;")

        idents = cur.fetchall()
        self.conn.commit()
        cur.close()

        for s in [str(i[0]) for i in idents]:
            comboboxtext.append_text(s)

        comboboxtext.set_active(0)

    def zlecenia_button1_5b_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku dodania nowego zlecenia."""
        nr_rej = self.zlecenia_entry1_1ba.get_text() + ":" + self.zlecenia_entry1_1bc.get_text()
        # SQL text
        faktura = self.zlecenia_comboboxtext1_2b.get_active_text()  # SQL boolean
        kli_id = self.zlecenia_comboboxtext1_3b.get_active_text()  # SQL integer
        sam_model = self.zlecenia_comboboxtext1_4b.get_active_text()  # SQL text

        faktura = True if faktura == "TAK" else False
        args = [nr_rej, faktura, int(kli_id), sam_model]
        cur = self.conn.cursor()

        try:
            cur.execute(
                "INSERT INTO zlecenia(nr_rej, faktura, kli_id, sam_model) VALUES(%s, %s, %s, %s);",
                args)
            cur.execute("SELECT max(id) FROM zlecenia;")
            wyn = cur.fetchone()[0]
        except:
            self.conn.rollback()
            PopUp("WYSTĄPIŁ BŁĄD WEWNĘTRZNY BAZY. PRZERWANO.").show()
            return
        else:
            self.conn.commit()
            self.zlecenia_comboboxtext2_1b.append_text(str(wyn))
            self.zlecenia_comboboxtext3_1b.append_text(str(wyn))
            PopUp("ZLECENIE ZOSTAŁO POMYŚLNIE ZŁOŻONE.\nID = " + str(wyn)).show()
        finally:
            cur.close()

    def zlecenia_button2_3b_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku powiązania zlecenia z usługą."""
        ident = self.zlecenia_comboboxtext2_1b.get_active_text()  # SQL integer
        nazwa = self.zlecenia_comboboxtext2_2b.get_active_text()  # SQL text

        args = [int(ident), nazwa]
        cur = self.conn.cursor()

        try:
            cur.execute("INSERT INTO zle_usl(zle_id, usl_nazwa) VALUES(%s, %s);", args)
        except:
            self.conn.rollback()
            PopUp("WYSTĄPIŁ BŁĄD WEWNĘTRZNY BAZY. PRZERWANO.").show()
            return
        else:
            self.conn.commit()
            self.zlecenia_comboboxtext2_1b.append_text(str(wyn))
            self.zlecenia_comboboxtext3_1b.append_text(str(wyn))
            PopUp("POMYŚLNIE DODANO USŁUGĘ DO ZLECENIA.").show()
        finally:
            cur.close()

        PopUp("ZLECENIE " + str(ident) + " ZOSTAŁO POMYŚLNIE ZMIENIONE.").show()

    def zlecenia_button3_1c_clicked_cb(self, button):
        """Reaguje na kliknięcie przycisku wyszukania zlecenia."""
        ident = self.zlecenia_comboboxtext3_1b.get_active_text()  # SQL integer

        args = [int(ident)]
        cur = self.conn.cursor()

        try:
            cur.execute(
                "SELECT id, data_zlec, data_real, nr_rej, faktura, kli_id, sam_model, koszt FROM "
                "zlecenia WHERE id = %s",
                args)
            wyn = cur.fetchone()[:]
        except:
            self.conn.rollback()
            PopUp("WYSTĄPIŁ BŁĄD WEWNĘTRZNY BAZY. PRZERWANO.").show()
            return
        else:
            self.conn.commit()
            PopUp(", ".join(map(str, wyn))).show()
        finally:
            cur.close()

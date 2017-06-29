# -*- coding: utf-8 -*-

import wx
import numpy as np
import pickle

class Silnik():
    @staticmethod
    def newmatrix(dane):
        if dane.shape[0] == 10:
            rozmiar = 5
            wagi = np.zeros(10)
        elif dane.shape[0] == 1:
            rozmiar = 2
            wagi = np.zeros(rozmiar)
        elif dane.shape[0] == 3:
            rozmiar = dane.shape[0]
            wagi = np.zeros(rozmiar)

        macierz = np.eye(rozmiar)

        for x in range(0, dane.shape[0]):

            zmienna = dane[x]
            if zmienna == 0:
                wagi[x] = 1/9.0
            if zmienna == 1:
                wagi[x] = 1/7.0
            if zmienna == 2:
                wagi[x] = 1/5.0
            if zmienna == 3.0:
                wagi[x] = 1/3.0
            if zmienna == 4:
                wagi[x] = 1.0
            if zmienna == 5:
                wagi[x] = 3.0
            if zmienna == 6:
                wagi[x] = 5.0
            if zmienna == 7:
                wagi[x] = 7.0
            if zmienna == 8:
                wagi[x] = 9.0

        a = 1
        b = 0
        c = 0

        for z in range(b, rozmiar):
            for y in range(a, rozmiar):
                macierz[z, y] = wagi[c]
                c = c + 1
            a = a + 1

        return macierz

    @staticmethod
    def matrix_inverse(matrix):
        N = int(np.sqrt(matrix.size))
        for i in range(N):
            matrix[i: N, i] = np.transpose(1. / matrix[i, i: N])
        return matrix


    @staticmethod
    def spojnosc(macierz):

        RI = np.array([(0.0001, 0.0001, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49)])

        rozmiar = macierz.shape[0]                  # rozmiar macierzy ile na ile
        suma = macierz.sum(0)               # suma wszystkich kolumn macierzy wag
        nowamacierz = np.zeros((rozmiar, rozmiar))
        # w = np.zeros((rozmiar, 1))
        for x in range(0, rozmiar):
            for y in range(0, rozmiar):
                nowamacierz[y, x] = (macierz[y, x]/suma[x])

        w = nowamacierz.sum(1)/rozmiar
        lamb = np.dot(suma, w)
        CI = (lamb-rozmiar)/(rozmiar-1)
        CR = CI/(RI[0, rozmiar-1])
        if CR < 0.2:
            return True, w
        else:
            return False, w

    @staticmethod
    def licz(wybor_w, odleglosc_w, ceny_w, klimat_w, od_domu_w, od_aktualnej_pozycji_w, od_centrum_w, piwo_w, drinki_w, przystawki_w, obsluga_w, muzyka_w):

        rozmiar = piwo_w.shape[0]
        X = np.zeros(rozmiar)

        for x in range(0, rozmiar):

            X[x] = ((odleglosc_w[0]*od_domu_w[x]+odleglosc_w[1]*od_aktualnej_pozycji_w[x]+odleglosc_w[2]*od_centrum_w[x]) *
                    wybor_w[0]+(ceny_w[0]*piwo_w[x]+ceny_w[1]*drinki_w[x]+ceny_w[2]*przystawki_w[x])*wybor_w[1] +
                                                            (klimat_w[0]*obsluga_w[x]+klimat_w[1]*muzyka_w[x])*wybor_w[2])

        return X

    @staticmethod
    def make_licz(W, user):

        wybor = W['wybor']
        odleg = W['odleglosc']
        ceny = W['ceny']
        klimat = W['klimat']

        dom = W['dom']
        pozycja = W['pozycja']
        centrum =  W['centrum']
        drinki = W['drinki']
        piwo = W['piwo']
        przystawki = W['przystawki']
        obsluga = W['obsluga']
        muzyka = W['muzyka']

        op = W['op']

        ranking = []

        for i in range(user):
            ranking.append(Silnik.licz(wybor[i], odleg[i], ceny[i], klimat[i], dom[i], pozycja[i], centrum[i],
                 piwo[i], drinki[i], przystawki[i], obsluga[i], muzyka[i]))

        i = 0
        ranking_ostateczny = np.zeros(ranking[0].shape[0],dtype=float)
        for user in ranking:
            ranking_ostateczny += np.multiply(user,op[0][i])
            i += 1
        return ranking_ostateczny


    @staticmethod
    def cos(dane):
        odwroc = Silnik.newmatrix(dane)
        spojna = Silnik.matrix_inverse(odwroc)
        komunikat = Silnik.spojnosc(spojna)
        return komunikat

class GUI_cluby_info(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_cluby_info, self).__init__(parent, title=title, size=(650, 710))
        self.data = data
        self.pictures_name = ["PIC/pub1_thumbnail.png", "PIC/pub2_thumbnail.png", "PIC/pub3_thumbnail.png", "PIC/pub4_thumbnail.png", "PIC/pub5_thumbnail.png"]
        self.list_of_pub = ['Spiż', 'Graciarnia', 'Czeski film', 'Mleczarnia', 'Piwnica Świdnicka']
        self.Lista_miejsca = self.data.Lista_miejsca
        self.List_Customer = self.data.List_Customer
        self.pubID = self.data.pubID
        self.cliID = self.data.cliID
        self.Tensor = self.data.Tensor
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        # Obrazek 1
        self.m_bpButton1 = wx.BitmapButton(self.pnl, -1, wx.Bitmap(self.pictures_name[0], wx.BITMAP_TYPE_ANY),
                                           (10, 10), wx.DefaultSize, wx.BU_AUTODRAW)
        # Opis Obrazek 1
        self.label1 = wx.StaticText(self.pnl, label="Spiż:", pos=(10, 80))
        self.label1 = wx.StaticText(self.pnl,
                                   label="""Spiż już od 16 lat istnieje na wrocławskim Rynku. Wielką atrakcją,
która od początku przyciąga do lokalu mnóstwo ludzi, jest możliwość
śledzenia produkcji piwa, które powstaje według 500-letniej receptury.
W restauracji warto skosztować którejś z serwowanych staropolskich potraw,
a w ogródku wypić piwo i zagryźć je chlebem ze smalcem, który dostaniemy gratis.""",
                                   pos=(190, 10))

        self.m_bpButton2 = wx.BitmapButton(self.pnl, -1, wx.Bitmap(self.pictures_name[1], wx.BITMAP_TYPE_ANY),
                                           (10, 140), wx.DefaultSize, wx.BU_AUTODRAW)
        # Opis Obrazek 1
        self.label2 = wx.StaticText(self.pnl, label="Graciarnia:", pos=(10, 210))
        self.label2 = wx.StaticText(self.pnl,
                                   label="""Graciarnia to prawdziwy pub z duszą. Gdy idąc ulicą Kazimierza Wielkiego
skręcimy w ciemną bramę, otworzymy ciężkie, drewniane drzwi i postawimy
pierwszy krok to tak, jakbyśmy znaleźli się w innym świecie. Wśród czerwonych
ścian, przy nastrojowym świetle świec, otoczeni antycznymi meblami i kostiumami
z Opery Wrocławskiej możemy odpocząć od codziennego zgiełku i zapomnieć o
wszystkich problemach. Odprężająca muzyka pozwoli zrelaksować się przy szklance
zimnego piwa lub gorącej czekolady.""",
                                   pos=(190, 140))

        self.m_bpButton3 = wx.BitmapButton(self.pnl, -1, wx.Bitmap(self.pictures_name[2], wx.BITMAP_TYPE_ANY),
                                           (10, 270), wx.DefaultSize, wx.BU_AUTODRAW)
        # Opis Obrazek 1
        self.label3 = wx.StaticText(self.pnl, label="Czeski film:", pos=(10, 340))
        self.label3 = wx.StaticText(self.pnl,
                                   label="""Czeski Film to pub o dwóch kondygnacjach, na górze najlepiej zjeść lunch,
np. pyszne naleśniki czy pierogi, odpoczniemy tam przy spokojnej
muzyce i porozmawiamy z przyjaciółmi. Dół pozwala nam poczuć się jak
w praskiej piwnicy, zabawne malunki czy plakaty filmowe. Dodatkową atrakcją
tego lokalu, który każdego wieczoru tętni życiem to letni ogródek oraz
klimatyzacja, dzięki której w upalne dni będziemy mogli
schronić się przed upałem sącząc zimnego drinka.""",
                                   pos=(190, 270))

        self.m_bpButton4 = wx.BitmapButton(self.pnl, -1, wx.Bitmap(self.pictures_name[3], wx.BITMAP_TYPE_ANY),
                                           (10, 400), wx.DefaultSize, wx.BU_AUTODRAW)
        # Opis Obrazek 1
        self.label3 = wx.StaticText(self.pnl, label="Mleczarnia:", pos=(10, 470))
        self.label3 = wx.StaticText(self.pnl,
                                   label="""Mleczarnia – urocza knajpka w żydowskiej dzielnicy przyciąga przytulnym
wystrojem i niepowtarzalnym klimatem. Wśród starych mebli i szydełkowanych
obrusów do późnych godzin dyskutować można o życiu i śmierci. Przy dźwiękach
jazzu czy chilloutu, w oparach dymu (niestety, nie ma sali dla niepalących)
poczuć możemy twórczą atmosferę, jak wtedy, gdy Wrocław był ostoją artystów.""",
                                   pos=(190, 400))

        self.m_bpButton5 = wx.BitmapButton(self.pnl, -1, wx.Bitmap(self.pictures_name[4], wx.BITMAP_TYPE_ANY),
                                           (10, 530), wx.DefaultSize, wx.BU_AUTODRAW)
        # Opis Obrazek 1
        self.label3 = wx.StaticText(self.pnl, label="Piwnica Świdnicka:", pos=(10, 600))
        self.label3 = wx.StaticText(self.pnl,
                                   label="""„Kto nie był w Piwnicy Świdnickiej, ten nie był we Wrocławiu” – zdanie,
które przed laty wypisane było na jeden ze ścian lokalu to święta prawda.
Restauracja, która jest najstarszą w Europie, a jej progi odwiedzili m.in.
Goethe czy Chopin, nie potrzebuje reklamy. Wnętrze opracowane na podstawie
historycznej dokumentacji przeniesie nas w zupełnie inny świat. Jedyne miejsce,
gdzie skosztujemy legendarnego Białego Barana.""",
                                   pos=(190, 530))



        # przycisk OK
        self.Button1 = wx.Button(self.pnl, label='OK', pos=(500, 630))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Centre()
        self.Show(True)


    def OnButton(self,e):
        #  jak zdązymy do mozna dac podglad zdjecia
        pass

    def OnButtonClicked(self,e):
        # txt = ['Line 1','Line 2','Line 3','Line 4','Line 5']
        # POP(None, 'Wynik', 5, txt)
        # przycisk wyjscia i przeslania danych

        self.data.Tensor = self.Tensor
        self.Close()

class GUI_club(wx.Frame):
        def __init__(self, parent, title, data):
            super(GUI_club, self).__init__(parent, title=title, size=(650, 450))
            self.data = data
            self.pictures_name = self.data.pictures_name
            self.Lista_miejsca = self.data.Lista_miejsca
            self.List_Customer = self.data.List_Customer
            self.pubID = self.data.pubID
            self.cliID = self.data.cliID
            self.Tensor = self.data.Tensor
            self.picture_poz = self.data.picture_poz

            self.InitUI()

        def InitUI(self):
            self.pnl = wx.Panel(self)

            # inicjacja klubów
            self.rbox_club = wx.RadioBox(self.pnl, label='Miejsca', pos=(10, 10), choices=self.Lista_miejsca,
                                         majorDimension=0, style=wx.RA_SPECIFY_ROWS)
            self.rbox_club.Bind(wx.EVT_RADIOBOX, self.OnRadioClub)

            # inicjaciaj cech
            # lblList = ['1', '3', '5', '7', '9'] # 300
            lblList = ['Bardzo zle', 'Slabo', 'Srednio', 'Dobrze', 'Bardzo dobrze']  # 650
            self.rbox1 = wx.RadioBox(self.pnl, label='Cecha 1', pos=(100, 110), choices=lblList,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
            self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
            self.rbox2 = wx.RadioBox(self.pnl, label='Cecha 2', pos=(100, 160), choices=lblList,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
            self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
            self.rbox3 = wx.RadioBox(self.pnl, label='Cecha 3', pos=(100, 210), choices=lblList,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
            self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
            self.rbox4 = wx.RadioBox(self.pnl, label='Cecha 4', pos=(100, 260), choices=lblList,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
            self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
            self.rbox5 = wx.RadioBox(self.pnl, label='Cecha 5', pos=(100, 310), choices=lblList,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
            self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)

            self.SetSELECT()

            # inicjacja obrazków
            self.m_bpButton1 = wx.BitmapButton(self.pnl, 0,
                                               wx.Bitmap(self.pictures_name[self.pubID], wx.BITMAP_TYPE_ANY),
                                               self.picture_poz, wx.DefaultSize, wx.BU_AUTODRAW)
            self.m_bpButton1.Bind(wx.EVT_BUTTON, self.OnButton)

            self.label = wx.StaticText(self.pnl, label="Opis:", pos=(300, 10))
            self.label = wx.StaticText(self.pnl,
                                       label="Witamy w aplikacji 'Gdzie idziemy?'\n\nWybierz interesujące cię "
                                             "parametry \n"
                                             "i ciesz się z wyboru najlepszego\nmiejsca do spędzenia wolnego czasu.\n"
                                             "<-- Po kliknięciu na obrazek\n<-- zobaczysz opisy\nposzczególnych miejsc.",
                                       pos=(300, 30))

            self.Button1 = wx.Button(self.pnl, label='OK', pos=(100, 370))
            self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

            self.Centre()
            self.Show(True)

        def SetSELECT(self):
            self.rbox1.SetSelection(self.Tensor[self.cliID, self.pubID, 0])
            self.rbox2.SetSelection(self.Tensor[self.cliID, self.pubID, 1])
            self.rbox3.SetSelection(self.Tensor[self.cliID, self.pubID, 2])
            self.rbox4.SetSelection(self.Tensor[self.cliID, self.pubID, 3])
            self.rbox5.SetSelection(self.Tensor[self.cliID, self.pubID, 4])

        def OnRadioCustomer(self, e):
            rb = e.GetEventObject()
            print 'Uzytkownik', rb.GetSelection(), ' is clicked from Radio Group'
            self.cliID = rb.GetSelection()
            self.SetSELECT()

        def OnRadioClub(self, e):
            rb = e.GetEventObject()
            print rb.GetSelection(), ' is clicked from Radio Group'
            self.pubID = rb.GetSelection()
            self.SetSELECT()

            self.m_bpButton1.Destroy()
            self.m_bpButton1 = wx.BitmapButton(self.pnl, 0,
                                               wx.Bitmap(self.pictures_name[self.pubID], wx.BITMAP_TYPE_ANY),
                                               self.picture_poz, wx.DefaultSize, wx.BU_AUTODRAW)

        def onRadioBox(self, e):
            self.Tensor[self.cliID, self.pubID, 0] = self.rbox1.GetSelection()
            self.Tensor[self.cliID, self.pubID, 1] = self.rbox2.GetSelection()
            self.Tensor[self.cliID, self.pubID, 2] = self.rbox3.GetSelection()
            self.Tensor[self.cliID, self.pubID, 3] = self.rbox4.GetSelection()
            self.Tensor[self.cliID, self.pubID, 4] = self.rbox5.GetSelection()
            print self.Tensor

        def OnButton(self, e):
            #  jak zdązymy do mozna dac podglad zdjecia
            pass

        def OnButtonClicked(self, e):
            # txt = ['Line 1','Line 2','Line 3','Line 4','Line 5']
            # POP(None, 'Wynik', 5, txt)
            # przycisk wyjscia i przeslania danych

            self.data.Tensor = self.Tensor
            self.Close()


#First Run
class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(360, 100))
        self.egg=[315, 315, 317, 317, 314, 316, 314, 316, 66, 65]
        self.egg_i = 0
        self.pnl = wx.Panel(self)
        l1 = wx.StaticText(self.pnl, -1, "Ile użytkowników", pos=(10, 20))
        self.t1 = wx.TextCtrl(self.pnl, pos=(120, 20))
        self.t1.SetMaxLength(1)
        self.t1.SetValue('5')

        self.Button_ok = wx.Button(self.pnl, label='OK', pos=(240, 18))
        self.Button_ok.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.pnl.Bind(wx.EVT_CHAR_HOOK, self.onKey)

        self.Centre()
        self.Show()
        self.Fit()

    def onKey(self, evt):
        # print evt.GetKeyCode()
        if evt.GetKeyCode() == self.egg[self.egg_i]:
            self.egg_i += 1
            if self.egg_i == 10:
                print 'Multipla'
                Egg(None)
                self.egg_i = 0
        else:
            self.egg_i = 0
            evt.Skip()

    def OnButtonClicked(self, e):
        try:
            self.t2.Destroy()
        except:
            pass
        try:
            txt = self.t1.GetValue()
            num = int(txt)
            if num > 7:
                self.t2 = wx.StaticText(self.pnl, -1, 'Za duża wartość', pos=(10, 45))
            else:
                num -= 1
                self.t2 = wx.StaticText(self.pnl, -1, str(num), pos=(10, 45))
                GUI_main(None, 'Gdzie idziemy?', num)
                self.Close()
        except:
            self.t2 = wx.StaticText(self.pnl, -1, 'Zla wartosc', pos=(10, 45))
        self.t2.SetForegroundColour((255, 0, 0))



class Egg(wx.Frame):
    def __init__(self, parent):
        super(Egg, self).__init__(parent, title="Multipla", size=(1280, 853))
        self.pnl = wx.Panel(self)

        self.m_bpButton1 = wx.BitmapButton(self.pnl, -1, wx.Bitmap('PIC/egg.jpg', wx.BITMAP_TYPE_ANY),
                                           (0, 0), wx.DefaultSize, wx.BU_AUTODRAW)

        self.Centre()
        self.Show()
        self.Fit()

# 1 poziom
class GUI_main(wx.Frame):
    def __init__(self, parent, title, num):
        super(GUI_main, self).__init__(parent, title=title, size=(1350, 400))
        self.pictures_name = ["PIC/pub1_thumbnail.png", "PIC/pub2_thumbnail.png", "PIC/pub3_thumbnail.jpg","PIC/pub4_thumbnail.png", "PIC/pub5_thumbnail.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.Numbers_Customers = num
        self.List_Customer2 = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5', 'Klient 6', 'Klient 7']
        self.List_Customer = self.List_Customer2[0:num + 1]
        self.pubID = 0
        self.cliID = 0
        self.OP = 0
        name = ['Spiż', 'Graciarnia', 'Czeski film', 'Mleczarnia', 'Piwnica Świdnicka']
        self.name = name
        self.lista_por=[name[0]+ ' do '+name[1], name[0]+ ' do '+name[2], name[0]+ ' do '+name[3],
                        name[0]+ ' do '+name[4], name[1]+ ' do '+name[2], name[1]+ ' do '+name[3],
                        name[1]+ ' do '+name[4], name[2]+ ' do '+name[3], name[2]+ ' do '+name[4],
                        name[3] + ' do ' + name[4]]
        # self.lista_por = ['1-2', '1-3', '1-4', '1-5', '2-3', '2-4', '2-5', '3-4', '3-5', '4-5']
        self.Tensor = np.ones((len(self.pictures_name),len(self.Lista_miejsca),5))*2

        self.picture_poz = (10, 10)
        self.button_name = ['Ocen odleglosc','Ocen Ceny','Ocen klimat']


        # baza danych
        self.wybor = np.ones((len(self.List_Customer), 3)) * 4
        self.odleg = np.ones((len(self.List_Customer), 3)) * 4
        self.ceny = np.ones((len(self.List_Customer), 3)) * 4
        self.klimat =np.ones((len(self.List_Customer), 1)) * 4

        self.dom = np.ones((len(self.List_Customer), 10)) * 4
        self.pozycja = np.ones((len(self.List_Customer), 10)) * 4
        self.centrum = np.ones((len(self.List_Customer), 10)) * 4
        self.drinki = np.ones((len(self.List_Customer), 10)) * 4
        self.piwo = np.ones((len(self.List_Customer), 10)) * 4
        self.przystawki = np.ones((len(self.List_Customer), 10)) * 4
        self.obsluga = np.ones((len(self.List_Customer), 10)) * 4
        self.muzyka = np.ones((len(self.List_Customer), 10)) * 4

        self.op = np.ones((1, len(self.List_Customer)))

        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        # inicjacja uzytkownikow
        self.rbox_Customer = wx.RadioBox(self.pnl, label='Uzytkownik', pos=(400, 10), choices=self.List_Customer,
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox_Customer.Bind(wx.EVT_RADIOBOX, self.OnRadioCustomer)

        lblList = ['Najbardziej nieistotny', 'Znacznie nieistotne ', 'Nieistotne', 'Troche nieistotne', 'Średnio istotne', 'Troche istotne', 'Istotne',
                   'Znacznie Istotnie', 'Najistotniejsze']
        # lblList = ['Bardzo nieistotny', 'Slabo istotny', 'Srednio', 'Istotny', 'Bardzo Istotny']  #650
        self.rbox1 = wx.RadioBox(self.pnl, label='Odleglosc do ceny', pos=(30, 150), choices=lblList,
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label='Odelglosc do Klimatu', pos=(30, 200), choices=lblList,
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label='Ceny do Klimatu', pos=(30, 250), choices=lblList,
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        # inicjacja obrazków
        self.m_bpButton1 = wx.BitmapButton(self.pnl, 0, wx.Bitmap(self.pictures_name[self.pubID], wx.BITMAP_TYPE_ANY),
                                           self.picture_poz, wx.DefaultSize, wx.BU_AUTODRAW)
        self.m_bpButton1.Bind(wx.EVT_BUTTON, self.OnButton)

        self.label = wx.StaticText(self.pnl, label="Opis:", pos=(180, 10))
        self.label = wx.StaticText(self.pnl,
                                   label="Witamy w aplikacji 'Gdzie idziemy?'\n\nWybierz interesujące cię "
                                         "parametry \n"
                                         "i ciesz się z wyboru najlepszego\nmiejsca do spędzenia wolnego czasu.\n"
                                         "<-- Po kliknięciu na obrazek\n<-- zobaczysz opisy\nposzczególnych miejsc.",
                                   pos=(180, 30))

        self.Button1 = wx.Button(self.pnl, label=self.button_name[0], pos=(902, 310))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked1)

        self.Button1 = wx.Button(self.pnl, label=self.button_name[1], pos=(1015, 310))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked2)

        self.Button1 = wx.Button(self.pnl, label=self.button_name[2], pos=(1113, 310))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked3)



        self.Button1 = wx.Button(self.pnl, label='Ranking', pos=(1210, 310))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Button1 = wx.Button(self.pnl, label='SAVE', pos=(1100, 10))
        self.Button1.Bind(wx.EVT_BUTTON, self.Save)

        self.Button1 = wx.Button(self.pnl, label='LOAD', pos=(1100, 50))
        self.Button1.Bind(wx.EVT_BUTTON, self.Load)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.wybor[self.cliID, 0])
        self.rbox2.SetSelection(self.wybor[self.cliID, 1])
        self.rbox3.SetSelection(self.wybor[self.cliID, 2])
        self.Check()

    def OnRadioCustomer(self, e):
        rb = e.GetEventObject()
        print 'Uzytkownik', rb.GetSelection(), ' is clicked from Radio Group'
        self.cliID = rb.GetSelection()
        self.SetSELECT()
        if self.cliID == self.Numbers_Customers :
            self.ButtonT = wx.Button(self.pnl, label='Oceń innych', pos=(804, 310))
            self.ButtonT.Bind(wx.EVT_BUTTON, self.OnButtonTajne)
            self.OP = 1
        elif self.OP == 1:
            self.ButtonT.Destroy()
            self.OP = 0


    def OnRadioClub(self, e):
        rb = e.GetEventObject()
        print rb.GetSelection(), ' is clicked from Radio Group'
        self.pubID = rb.GetSelection()
        self.SetSELECT()

        self.m_bpButton1.Destroy()
        self.m_bpButton1 = wx.BitmapButton(self.pnl, 0,
                                        wx.Bitmap(self.pictures_name[self.pubID], wx.BITMAP_TYPE_ANY),
                                        self.picture_poz, wx.DefaultSize, wx.BU_AUTODRAW)



    def onRadioBox(self, e):
        self.wybor[self.cliID, 0] = self.rbox1.GetSelection()
        self.wybor[self.cliID, 1] = self.rbox2.GetSelection()
        self.wybor[self.cliID, 2] = self.rbox3.GetSelection()
        self.Check()

    def OnButton(self,e):
        #  jak zdązymy do mozna dac podglad zdjecia
        GUI_cluby_info(None, 'Gdzie idziemy?', self)


    def OnButtonClicked(self,e):
        # GUI_club(None, 'Gdzie idziemy?', self)
        self.database = {'wybor': self.wybor, 'odleglosc': self.odleg, 'ceny': self.ceny,
                      'klimat': self.klimat, 'dom': self.dom, 'pozycja': self.pozycja, 'centrum': self.centrum,
                      'drinki': self.drinki, 'piwo': self.piwo, 'przystawki': self.przystawki, 'muzyka': self.muzyka, 'obsluga': self.obsluga, 'op': self.op}
        self.database_name = ['wybor', 'odleglosc', 'ceny', 'klimat', 'dom', 'pozycja',
                              'centrum','drinki', 'piwo', 'przystawki', 'muzyka', 'obsluga', 'op']
        POP(None, 'Wynik', self)


    def OnButtonClicked1(self,e):
        GUI_odleg(None, self.button_name[0], self)

    def OnButtonClicked2(self,e):
        GUI_ceny(None, self.button_name[1], self)

    def OnButtonClicked3(self,e):
        GUI_klimat(None, self.button_name[2], self)

    def OnButtonTajne(self,e):
        GUI_OP(None, 'ocen użytkowników', self)

    def Save(self, e):
        dictionary = {'wybor': self.wybor, 'odleglosc': self.odleg, 'ceny': self.ceny,
                      'klimat': self.klimat, 'dom': self.dom, 'pozycja': self.pozycja, 'centrum': self.centrum,
                      'drinki': self.drinki, 'piwo': self.piwo, 'przystawki': self.przystawki, 'muzyka': self.muzyka, 'obsluga': self.obsluga, 'op': self.op}
        pickle.dump(dictionary, open('save.p', 'wb'))
        del dictionary

    def Load(self, e):
        dictionary = pickle.load(open('save.p', 'rb'))

        self.wybor = dictionary['wybor']
        self.odleg = dictionary['odleglosc']
        self.ceny = dictionary['ceny']
        self.klimat = dictionary['klimat']

        self.dom = dictionary['dom']
        self.pozycja = dictionary['pozycja']
        self.centrum =  dictionary['centrum']
        self.drinki = dictionary['drinki']
        self.piwo = dictionary['piwo']
        self.przystawki = dictionary['przystawki']
        self.obsluga = dictionary['obsluga']
        self.muzyka = dictionary['muzyka']

        self.op = dictionary['op']

        self.SetSELECT()

    def Check(self):

        if Silnik.cos(self.wybor[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 310))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color


class GUI_OP(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_OP, self).__init__(parent, title=title, size=(280, 380))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.lista_por = self.List_Customer
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2


        # baza danych
        self.tab = self.data.op
        #self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.label = wx.StaticText(self.pnl, label="waga ocen ludzi: ", pos=(10, 10))

        lblList = ['0', '1', '2', '3', '4', '5']

        self.rbox1 = wx.RadioBox(self.pnl, label=self.lista_por[0], pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label=self.lista_por[1], pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label=self.lista_por[2], pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox4 = wx.RadioBox(self.pnl, label=self.lista_por[3], pos=(30, 180), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox5 = wx.RadioBox(self.pnl, label=self.lista_por[4], pos=(30, 230), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)

        # odswiez wartosci
        self.SetSELECT()

        self.Button1 = wx.Button(self.pnl, label='OK', pos=(120, 300))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.tab[0, 0])
        self.rbox2.SetSelection(self.tab[0, 1])
        self.rbox3.SetSelection(self.tab[0, 2])
        self.rbox4.SetSelection(self.tab[0, 3])
        self.rbox5.SetSelection(self.tab[0, 4])

    def onRadioBox(self, e):
        self.tab[0, 0] = self.rbox1.GetSelection()
        self.tab[0, 1] = self.rbox2.GetSelection()
        self.tab[0, 2] = self.rbox3.GetSelection()
        self.tab[0, 3] = self.rbox4.GetSelection()
        self.tab[0, 4] = self.rbox5.GetSelection()

    def OnButtonClicked(self, e):
        self.data.op = self.tab
        self.Close()

# 2 poziom

class GUI_odleg(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_odleg, self).__init__(parent, title=title, size=(1350, 300))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2

        self.button_name = ['Oceń od domu', 'Oceń od pozycji', 'Oceń od centrum']

        # baza danych

        self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        lblList = ['Najbardziej nieistotny', 'Znacznie nieistotne ', 'Nieistotne', 'Troche nieistotne', 'Średnio istotne', 'Troche istotne', 'Istotne',                    'Znacznie Istotnie', 'Najistotniejsze']  # 650
        self.rbox1 = wx.RadioBox(self.pnl, label='odległość od domu do odległości od aktualniej pozycji', pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label='odległość od domu do odległości od centrum', pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label='odległość od aktualniej pozycji do odległości od centrum', pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.label = wx.StaticText(self.pnl, label="Ocen odleglosci:", pos=(10, 10))


        self.Button1 = wx.Button(self.pnl, label=self.button_name[0], pos=(870, 200))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked1)

        self.Button2 = wx.Button(self.pnl, label=self.button_name[1], pos=(978, 200))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButtonClicked2)

        self.Button3 = wx.Button(self.pnl, label=self.button_name[2], pos=(1090, 200))
        self.Button3.Bind(wx.EVT_BUTTON, self.OnButtonClicked3)

        self.Button_ok = wx.Button(self.pnl, label='OK', pos=(1210, 200))
        self.Button_ok.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.odleg[self.cliID, 0])
        self.rbox2.SetSelection(self.odleg[self.cliID, 1])
        self.rbox3.SetSelection(self.odleg[self.cliID, 2])

    def onRadioBox(self, e):
        self.odleg[self.cliID, 0] = self.rbox1.GetSelection()
        self.odleg[self.cliID, 1] = self.rbox2.GetSelection()
        self.odleg[self.cliID, 2] = self.rbox3.GetSelection()
        self.Check()

    def OnButtonClicked(self, e):
        self.data.odleg = self.odleg
        self.Close()

    def OnButtonClicked1(self, e):
        GUI_dom(None, self.button_name[0], self.data)

    def OnButtonClicked2(self, e):
        GUI_pozycja(None, self.button_name[1], self.data)

    def OnButtonClicked3(self, e):
        GUI_centrum(None, self.button_name[2], self.data)

    def Check(self):

        if Silnik.cos(self.odleg[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 185))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color

class GUI_ceny(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_ceny, self).__init__(parent, title=title, size=(1350, 300))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2

        self.button_name = ['Ocen ceny piwa', 'Ocen ceny drinków', 'Ocen ceny przystawek']

        # baza danych

        self.ceny = self.data.ceny
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        lblList = ['Najbardziej nieistotny', 'Znacznie nieistotne ', 'Nieistotne', 'Troche nieistotne', 'Średnio istotne', 'Troche istotne', 'Istotne',                    'Znacznie Istotnie', 'Najistotniejsze']  # 650
        self.rbox1 = wx.RadioBox(self.pnl, label='Piwo do Drinków', pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label='Piwo do Przystawek', pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label='Drinki do przystawek', pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.label = wx.StaticText(self.pnl, label="Ocen Ceny:", pos=(10, 10))


        self.Button1 = wx.Button(self.pnl, label=self.button_name[0], pos=(822, 200))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked1)

        self.Button2 = wx.Button(self.pnl, label=self.button_name[1], pos=(935, 200))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButtonClicked2)

        self.Button3 = wx.Button(self.pnl, label=self.button_name[2], pos=(1065, 200))
        self.Button3.Bind(wx.EVT_BUTTON, self.OnButtonClicked3)

        self.Button_ok = wx.Button(self.pnl, label='OK', pos=(1210, 200))
        self.Button_ok.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.ceny[self.cliID, 0])
        self.rbox2.SetSelection(self.ceny[self.cliID, 1])
        self.rbox3.SetSelection(self.ceny[self.cliID, 2])

    def onRadioBox(self, e):
        self.ceny[self.cliID, 0] = self.rbox1.GetSelection()
        self.ceny[self.cliID, 1] = self.rbox2.GetSelection()
        self.ceny[self.cliID, 2] = self.rbox3.GetSelection()
        self.Check()

    def OnButtonClicked(self, e):
        self.data.ceny = self.ceny
        self.Close()

    def OnButtonClicked1(self, e):
        GUI_piwo(None, self.button_name[0], self.data)

    def OnButtonClicked2(self, e):
        GUI_drinki(None, self.button_name[1], self.data)


    def OnButtonClicked3(self, e):
        GUI_przystawki(None, self.button_name[2], self.data)

    def Check(self):

        if Silnik.cos(self.ceny[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 185))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color

class GUI_klimat(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_klimat, self).__init__(parent, title=title, size=(1350, 195))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2

        self.button_name = ['Ocen Obsluge', 'Ocen od Muzyke']

        # baza danych

        self.klimat = self.data.klimat
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        lblList = ['Najbardziej nieistotny', 'Znacznie nieistotne ', 'Nieistotne', 'Troche nieistotne', 'Średnio istotne', 'Troche istotne', 'Istotne',                    'Znacznie Istotnie', 'Najistotniejsze']  # 650
        self.rbox1 = wx.RadioBox(self.pnl, label='Obsluga do muzyki', pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.label = wx.StaticText(self.pnl, label="Ocen klimat:", pos=(10, 10))


        self.Button1 = wx.Button(self.pnl, label=self.button_name[0], pos=(992, 100))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked1)

        self.Button2 = wx.Button(self.pnl, label=self.button_name[1], pos=(1094, 100))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButtonClicked2)

        self.Button_ok = wx.Button(self.pnl, label='OK', pos=(1210, 100))
        self.Button_ok.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.klimat[self.cliID, 0])

    def onRadioBox(self, e):
        self.klimat[self.cliID, 0] = self.rbox1.GetSelection()
        self.Check()

    def OnButtonClicked(self, e):
        self.data.klimat = self.klimat
        self.Close()

    def OnButtonClicked1(self, e):
        GUI_obsluga(None, self.button_name[0], self.data)

    def OnButtonClicked2(self, e):
        GUI_muzyka(None, self.button_name[1], self.data)

    def Check(self):

        if Silnik.cos(self.klimat[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 85))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color

# 3 Poziom
class GUI_dom(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_dom, self).__init__(parent, title=title, size=(1050, 620))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.lista_por = self.data.lista_por
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2


        # baza danych
        self.tab = self.data.dom
        #self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.label = wx.StaticText(self.pnl, label="Jak porównujesz: ", pos=(150, 10))

        lblList = ['Znacznie gorszy', 'Gorszy', 'Takie same', 'Lepszy', 'Znacznie lepszy']


        lblList = ['Najgorszy', 'Znacznie gorszy', 'Gorszy', 'Troche Gorszy', 'Takie same', 'Troche lepszy', 'Lepszy', 'Znacznie lepszy','Najlepszy' ]

        self.rbox1 = wx.RadioBox(self.pnl, label=self.lista_por[0], pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label=self.lista_por[1], pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label=self.lista_por[2], pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox4 = wx.RadioBox(self.pnl, label=self.lista_por[3], pos=(30, 180), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox5 = wx.RadioBox(self.pnl, label=self.lista_por[4], pos=(30, 230), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox6 = wx.RadioBox(self.pnl, label=self.lista_por[5], pos=(30, 280), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox6.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox7 = wx.RadioBox(self.pnl, label=self.lista_por[6], pos=(30, 330), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox7.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox8 = wx.RadioBox(self.pnl, label=self.lista_por[7], pos=(30, 380), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox8.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox9 = wx.RadioBox(self.pnl, label=self.lista_por[8], pos=(30, 430), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox9.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox10 = wx.RadioBox(self.pnl, label=self.lista_por[9], pos=(30, 480), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox10.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.Button1 = wx.Button(self.pnl, label='OK', pos=(940, 540))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Button2 = wx.Button(self.pnl, label='Kluby', pos=(940, 5))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.tab[self.cliID, 0])
        self.rbox2.SetSelection(self.tab[self.cliID, 1])
        self.rbox3.SetSelection(self.tab[self.cliID, 2])
        self.rbox4.SetSelection(self.tab[self.cliID, 3])
        self.rbox5.SetSelection(self.tab[self.cliID, 4])
        self.rbox6.SetSelection(self.tab[self.cliID, 5])
        self.rbox7.SetSelection(self.tab[self.cliID, 6])
        self.rbox8.SetSelection(self.tab[self.cliID, 7])
        self.rbox9.SetSelection(self.tab[self.cliID, 8])
        self.rbox10.SetSelection(self.tab[self.cliID, 9])

    def onRadioBox(self, e):
        self.tab[self.cliID, 0] = self.rbox1.GetSelection()
        self.tab[self.cliID, 1] = self.rbox2.GetSelection()
        self.tab[self.cliID, 2] = self.rbox3.GetSelection()
        self.tab[self.cliID, 3] = self.rbox4.GetSelection()
        self.tab[self.cliID, 4] = self.rbox5.GetSelection()
        self.tab[self.cliID, 5] = self.rbox6.GetSelection()
        self.tab[self.cliID, 6] = self.rbox7.GetSelection()
        self.tab[self.cliID, 7] = self.rbox8.GetSelection()
        self.tab[self.cliID, 8] = self.rbox9.GetSelection()
        self.tab[self.cliID, 9] = self.rbox10.GetSelection()
        self.Check()

    def Check(self):

        if Silnik.cos(self.tab[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 530))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color

    def OnButtonClicked(self, e):
        self.data.dom = self.tab
        self.Close()

    def OnButton(self,e):
        #  jak zdązymy do mozna dac podglad zdjecia
        GUI_cluby_info(None, 'Gdzie idziemy?', self.data)

class GUI_pozycja(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_pozycja, self).__init__(parent, title=title, size=(1050, 620))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.lista_por = self.data.lista_por
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2


        # baza danych
        self.tab = self.data.pozycja
        #self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.label = wx.StaticText(self.pnl, label="Jak porównujesz: ", pos=(150, 10))

        lblList = ['Najgorszy', 'Znacznie gorszy', 'Gorszy', 'Troche Gorszy', 'Takie same', 'Troche lepszy', 'Lepszy', 'Znacznie lepszy','Najlepszy' ]

        self.rbox1 = wx.RadioBox(self.pnl, label=self.lista_por[0], pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label=self.lista_por[1], pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label=self.lista_por[2], pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox4 = wx.RadioBox(self.pnl, label=self.lista_por[3], pos=(30, 180), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox5 = wx.RadioBox(self.pnl, label=self.lista_por[4], pos=(30, 230), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox6 = wx.RadioBox(self.pnl, label=self.lista_por[5], pos=(30, 280), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox6.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox7 = wx.RadioBox(self.pnl, label=self.lista_por[6], pos=(30, 330), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox7.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox8 = wx.RadioBox(self.pnl, label=self.lista_por[7], pos=(30, 380), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox8.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox9 = wx.RadioBox(self.pnl, label=self.lista_por[8], pos=(30, 430), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox9.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox10 = wx.RadioBox(self.pnl, label=self.lista_por[9], pos=(30, 480), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox10.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.Button1 = wx.Button(self.pnl, label='OK', pos=(940, 540))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Button2 = wx.Button(self.pnl, label='Kluby', pos=(940, 5))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.tab[self.cliID, 0])
        self.rbox2.SetSelection(self.tab[self.cliID, 1])
        self.rbox3.SetSelection(self.tab[self.cliID, 2])
        self.rbox4.SetSelection(self.tab[self.cliID, 3])
        self.rbox5.SetSelection(self.tab[self.cliID, 4])
        self.rbox6.SetSelection(self.tab[self.cliID, 5])
        self.rbox7.SetSelection(self.tab[self.cliID, 6])
        self.rbox8.SetSelection(self.tab[self.cliID, 7])
        self.rbox9.SetSelection(self.tab[self.cliID, 8])
        self.rbox10.SetSelection(self.tab[self.cliID, 9])

    def onRadioBox(self, e):
        self.tab[self.cliID, 0] = self.rbox1.GetSelection()
        self.tab[self.cliID, 1] = self.rbox2.GetSelection()
        self.tab[self.cliID, 2] = self.rbox3.GetSelection()
        self.tab[self.cliID, 3] = self.rbox4.GetSelection()
        self.tab[self.cliID, 4] = self.rbox5.GetSelection()
        self.tab[self.cliID, 5] = self.rbox6.GetSelection()
        self.tab[self.cliID, 6] = self.rbox7.GetSelection()
        self.tab[self.cliID, 7] = self.rbox8.GetSelection()
        self.tab[self.cliID, 8] = self.rbox9.GetSelection()
        self.tab[self.cliID, 9] = self.rbox10.GetSelection()
        self.Check()

    def Check(self):

        if Silnik.cos(self.tab[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 530))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color

    def OnButtonClicked(self, e):
        self.data.pozycja = self.tab
        self.Close()

    def OnButton(self,e):
        #  jak zdązymy do mozna dac podglad zdjecia
        GUI_cluby_info(None, 'Gdzie idziemy?', self.data)

class GUI_centrum(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_centrum, self).__init__(parent, title=title, size=(1050, 620))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.lista_por = self.data.lista_por
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2


        # baza danych
        self.tab = self.data.centrum
        #self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.label = wx.StaticText(self.pnl, label="Jak porównujesz: ", pos=(150, 10))

        lblList = ['Najgorszy', 'Znacznie gorszy', 'Gorszy', 'Troche Gorszy', 'Takie same', 'Troche lepszy', 'Lepszy', 'Znacznie lepszy','Najlepszy' ]

        self.rbox1 = wx.RadioBox(self.pnl, label=self.lista_por[0], pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label=self.lista_por[1], pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label=self.lista_por[2], pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox4 = wx.RadioBox(self.pnl, label=self.lista_por[3], pos=(30, 180), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox5 = wx.RadioBox(self.pnl, label=self.lista_por[4], pos=(30, 230), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox6 = wx.RadioBox(self.pnl, label=self.lista_por[5], pos=(30, 280), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox6.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox7 = wx.RadioBox(self.pnl, label=self.lista_por[6], pos=(30, 330), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox7.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox8 = wx.RadioBox(self.pnl, label=self.lista_por[7], pos=(30, 380), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox8.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox9 = wx.RadioBox(self.pnl, label=self.lista_por[8], pos=(30, 430), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox9.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox10 = wx.RadioBox(self.pnl, label=self.lista_por[9], pos=(30, 480), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox10.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.Button1 = wx.Button(self.pnl, label='OK', pos=(940, 540))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Button2 = wx.Button(self.pnl, label='Kluby', pos=(940, 5))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.tab[self.cliID, 0])
        self.rbox2.SetSelection(self.tab[self.cliID, 1])
        self.rbox3.SetSelection(self.tab[self.cliID, 2])
        self.rbox4.SetSelection(self.tab[self.cliID, 3])
        self.rbox5.SetSelection(self.tab[self.cliID, 4])
        self.rbox6.SetSelection(self.tab[self.cliID, 5])
        self.rbox7.SetSelection(self.tab[self.cliID, 6])
        self.rbox8.SetSelection(self.tab[self.cliID, 7])
        self.rbox9.SetSelection(self.tab[self.cliID, 8])
        self.rbox10.SetSelection(self.tab[self.cliID, 9])

    def onRadioBox(self, e):
        self.tab[self.cliID, 0] = self.rbox1.GetSelection()
        self.tab[self.cliID, 1] = self.rbox2.GetSelection()
        self.tab[self.cliID, 2] = self.rbox3.GetSelection()
        self.tab[self.cliID, 3] = self.rbox4.GetSelection()
        self.tab[self.cliID, 4] = self.rbox5.GetSelection()
        self.tab[self.cliID, 5] = self.rbox6.GetSelection()
        self.tab[self.cliID, 6] = self.rbox7.GetSelection()
        self.tab[self.cliID, 7] = self.rbox8.GetSelection()
        self.tab[self.cliID, 8] = self.rbox9.GetSelection()
        self.tab[self.cliID, 9] = self.rbox10.GetSelection()
        self.Check()

    def Check(self):

        if Silnik.cos(self.tab[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 530))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color

    def OnButtonClicked(self, e):
        self.data.centrum = self.tab
        self.Close()

    def OnButton(self,e):
        #  jak zdązymy do mozna dac podglad zdjecia
        GUI_cluby_info(None, 'Gdzie idziemy?', self.data)


class GUI_piwo(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_piwo, self).__init__(parent, title=title, size=(1050, 620))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.lista_por = self.data.lista_por
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2


        # baza danych
        self.tab = self.data.piwo
        #self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.label = wx.StaticText(self.pnl, label="Jak porównujesz: ", pos=(150, 10))

        lblList = ['Najgorszy', 'Znacznie gorszy', 'Gorszy', 'Troche Gorszy', 'Takie same', 'Troche lepszy', 'Lepszy', 'Znacznie lepszy','Najlepszy' ]

        self.rbox1 = wx.RadioBox(self.pnl, label=self.lista_por[0], pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label=self.lista_por[1], pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label=self.lista_por[2], pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox4 = wx.RadioBox(self.pnl, label=self.lista_por[3], pos=(30, 180), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox5 = wx.RadioBox(self.pnl, label=self.lista_por[4], pos=(30, 230), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox6 = wx.RadioBox(self.pnl, label=self.lista_por[5], pos=(30, 280), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox6.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox7 = wx.RadioBox(self.pnl, label=self.lista_por[6], pos=(30, 330), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox7.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox8 = wx.RadioBox(self.pnl, label=self.lista_por[7], pos=(30, 380), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox8.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox9 = wx.RadioBox(self.pnl, label=self.lista_por[8], pos=(30, 430), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox9.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox10 = wx.RadioBox(self.pnl, label=self.lista_por[9], pos=(30, 480), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox10.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.Button1 = wx.Button(self.pnl, label='OK', pos=(940, 540))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Button2 = wx.Button(self.pnl, label='Kluby', pos=(940, 5))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.tab[self.cliID, 0])
        self.rbox2.SetSelection(self.tab[self.cliID, 1])
        self.rbox3.SetSelection(self.tab[self.cliID, 2])
        self.rbox4.SetSelection(self.tab[self.cliID, 3])
        self.rbox5.SetSelection(self.tab[self.cliID, 4])
        self.rbox6.SetSelection(self.tab[self.cliID, 5])
        self.rbox7.SetSelection(self.tab[self.cliID, 6])
        self.rbox8.SetSelection(self.tab[self.cliID, 7])
        self.rbox9.SetSelection(self.tab[self.cliID, 8])
        self.rbox10.SetSelection(self.tab[self.cliID, 9])

    def onRadioBox(self, e):
        self.tab[self.cliID, 0] = self.rbox1.GetSelection()
        self.tab[self.cliID, 1] = self.rbox2.GetSelection()
        self.tab[self.cliID, 2] = self.rbox3.GetSelection()
        self.tab[self.cliID, 3] = self.rbox4.GetSelection()
        self.tab[self.cliID, 4] = self.rbox5.GetSelection()
        self.tab[self.cliID, 5] = self.rbox6.GetSelection()
        self.tab[self.cliID, 6] = self.rbox7.GetSelection()
        self.tab[self.cliID, 7] = self.rbox8.GetSelection()
        self.tab[self.cliID, 8] = self.rbox9.GetSelection()
        self.tab[self.cliID, 9] = self.rbox10.GetSelection()
        self.Check()

    def Check(self):

        if Silnik.cos(self.tab[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 530))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color

    def OnButtonClicked(self, e):
        self.data.piwo = self.tab
        self.Close()

    def OnButton(self, e):
        #  jak zdązymy do mozna dac podglad zdjecia
        GUI_cluby_info(None, 'Gdzie idziemy?', self.data)


class GUI_drinki(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_drinki, self).__init__(parent, title=title, size=(1050, 620))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.lista_por = self.data.lista_por
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2


        # baza danych
        self.tab = self.data.drinki
        #self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.label = wx.StaticText(self.pnl, label="Jak porównujesz: ", pos=(150, 10))

        lblList = ['Najgorszy', 'Znacznie gorszy', 'Gorszy', 'Troche Gorszy', 'Takie same', 'Troche lepszy', 'Lepszy', 'Znacznie lepszy','Najlepszy' ]

        self.rbox1 = wx.RadioBox(self.pnl, label=self.lista_por[0], pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label=self.lista_por[1], pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label=self.lista_por[2], pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox4 = wx.RadioBox(self.pnl, label=self.lista_por[3], pos=(30, 180), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox5 = wx.RadioBox(self.pnl, label=self.lista_por[4], pos=(30, 230), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox6 = wx.RadioBox(self.pnl, label=self.lista_por[5], pos=(30, 280), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox6.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox7 = wx.RadioBox(self.pnl, label=self.lista_por[6], pos=(30, 330), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox7.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox8 = wx.RadioBox(self.pnl, label=self.lista_por[7], pos=(30, 380), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox8.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox9 = wx.RadioBox(self.pnl, label=self.lista_por[8], pos=(30, 430), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox9.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox10 = wx.RadioBox(self.pnl, label=self.lista_por[9], pos=(30, 480), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox10.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.Button1 = wx.Button(self.pnl, label='OK', pos=(940, 540))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Button2 = wx.Button(self.pnl, label='Kluby', pos=(940, 5))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.tab[self.cliID, 0])
        self.rbox2.SetSelection(self.tab[self.cliID, 1])
        self.rbox3.SetSelection(self.tab[self.cliID, 2])
        self.rbox4.SetSelection(self.tab[self.cliID, 3])
        self.rbox5.SetSelection(self.tab[self.cliID, 4])
        self.rbox6.SetSelection(self.tab[self.cliID, 5])
        self.rbox7.SetSelection(self.tab[self.cliID, 6])
        self.rbox8.SetSelection(self.tab[self.cliID, 7])
        self.rbox9.SetSelection(self.tab[self.cliID, 8])
        self.rbox10.SetSelection(self.tab[self.cliID, 9])

    def onRadioBox(self, e):
        self.tab[self.cliID, 0] = self.rbox1.GetSelection()
        self.tab[self.cliID, 1] = self.rbox2.GetSelection()
        self.tab[self.cliID, 2] = self.rbox3.GetSelection()
        self.tab[self.cliID, 3] = self.rbox4.GetSelection()
        self.tab[self.cliID, 4] = self.rbox5.GetSelection()
        self.tab[self.cliID, 5] = self.rbox6.GetSelection()
        self.tab[self.cliID, 6] = self.rbox7.GetSelection()
        self.tab[self.cliID, 7] = self.rbox8.GetSelection()
        self.tab[self.cliID, 8] = self.rbox9.GetSelection()
        self.tab[self.cliID, 9] = self.rbox10.GetSelection()
        self.Check()

    def Check(self):

        if Silnik.cos(self.tab[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 530))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color


    def OnButtonClicked(self, e):
        self.data.drinki = self.tab
        self.Close()

    def OnButton(self,e):
        #  jak zdązymy do mozna dac podglad zdjecia
        GUI_cluby_info(None, 'Gdzie idziemy?', self.data)

class GUI_przystawki(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_przystawki, self).__init__(parent, title=title, size=(1050, 620))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.lista_por = self.data.lista_por
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2


        # baza danych
        self.tab = self.data.przystawki
        #self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.label = wx.StaticText(self.pnl, label="Jak porównujesz: ", pos=(150, 10))

        lblList = ['Najgorszy', 'Znacznie gorszy', 'Gorszy', 'Troche Gorszy', 'Takie same', 'Troche lepszy', 'Lepszy', 'Znacznie lepszy','Najlepszy' ]

        self.rbox1 = wx.RadioBox(self.pnl, label=self.lista_por[0], pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label=self.lista_por[1], pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label=self.lista_por[2], pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox4 = wx.RadioBox(self.pnl, label=self.lista_por[3], pos=(30, 180), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox5 = wx.RadioBox(self.pnl, label=self.lista_por[4], pos=(30, 230), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox6 = wx.RadioBox(self.pnl, label=self.lista_por[5], pos=(30, 280), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox6.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox7 = wx.RadioBox(self.pnl, label=self.lista_por[6], pos=(30, 330), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox7.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox8 = wx.RadioBox(self.pnl, label=self.lista_por[7], pos=(30, 380), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox8.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox9 = wx.RadioBox(self.pnl, label=self.lista_por[8], pos=(30, 430), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox9.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox10 = wx.RadioBox(self.pnl, label=self.lista_por[9], pos=(30, 480), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox10.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.Button1 = wx.Button(self.pnl, label='OK', pos=(940, 540))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Button2 = wx.Button(self.pnl, label='Kluby', pos=(940, 5))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.tab[self.cliID, 0])
        self.rbox2.SetSelection(self.tab[self.cliID, 1])
        self.rbox3.SetSelection(self.tab[self.cliID, 2])
        self.rbox4.SetSelection(self.tab[self.cliID, 3])
        self.rbox5.SetSelection(self.tab[self.cliID, 4])
        self.rbox6.SetSelection(self.tab[self.cliID, 5])
        self.rbox7.SetSelection(self.tab[self.cliID, 6])
        self.rbox8.SetSelection(self.tab[self.cliID, 7])
        self.rbox9.SetSelection(self.tab[self.cliID, 8])
        self.rbox10.SetSelection(self.tab[self.cliID, 9])

    def onRadioBox(self, e):
        self.tab[self.cliID, 0] = self.rbox1.GetSelection()
        self.tab[self.cliID, 1] = self.rbox2.GetSelection()
        self.tab[self.cliID, 2] = self.rbox3.GetSelection()
        self.tab[self.cliID, 3] = self.rbox4.GetSelection()
        self.tab[self.cliID, 4] = self.rbox5.GetSelection()
        self.tab[self.cliID, 5] = self.rbox6.GetSelection()
        self.tab[self.cliID, 6] = self.rbox7.GetSelection()
        self.tab[self.cliID, 7] = self.rbox8.GetSelection()
        self.tab[self.cliID, 8] = self.rbox9.GetSelection()
        self.tab[self.cliID, 9] = self.rbox10.GetSelection()
        self.Check()

    def Check(self):

        if Silnik.cos(self.tab[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 530))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color

    def OnButtonClicked(self, e):
        self.data.przystawki = self.tab
        self.Close()

    def OnButton(self,e):
        #  jak zdązymy do mozna dac podglad zdjecia
        GUI_cluby_info(None, 'Gdzie idziemy?', self.data)


class GUI_obsluga(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_obsluga, self).__init__(parent, title=title, size=(1050, 620))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.lista_por = self.data.lista_por
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2


        # baza danych
        self.tab = self.data.obsluga
        #self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.label = wx.StaticText(self.pnl, label="Jak porównujesz: ", pos=(150, 10))

        lblList = ['Najgorszy', 'Znacznie gorszy', 'Gorszy', 'Troche Gorszy', 'Takie same', 'Troche lepszy', 'Lepszy', 'Znacznie lepszy','Najlepszy' ]

        self.rbox1 = wx.RadioBox(self.pnl, label=self.lista_por[0], pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label=self.lista_por[1], pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label=self.lista_por[2], pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox4 = wx.RadioBox(self.pnl, label=self.lista_por[3], pos=(30, 180), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox5 = wx.RadioBox(self.pnl, label=self.lista_por[4], pos=(30, 230), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox6 = wx.RadioBox(self.pnl, label=self.lista_por[5], pos=(30, 280), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox6.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox7 = wx.RadioBox(self.pnl, label=self.lista_por[6], pos=(30, 330), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox7.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox8 = wx.RadioBox(self.pnl, label=self.lista_por[7], pos=(30, 380), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox8.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox9 = wx.RadioBox(self.pnl, label=self.lista_por[8], pos=(30, 430), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox9.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox10 = wx.RadioBox(self.pnl, label=self.lista_por[9], pos=(30, 480), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox10.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.Button1 = wx.Button(self.pnl, label='OK', pos=(940, 540))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Button2 = wx.Button(self.pnl, label='Kluby', pos=(940, 5))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.tab[self.cliID, 0])
        self.rbox2.SetSelection(self.tab[self.cliID, 1])
        self.rbox3.SetSelection(self.tab[self.cliID, 2])
        self.rbox4.SetSelection(self.tab[self.cliID, 3])
        self.rbox5.SetSelection(self.tab[self.cliID, 4])
        self.rbox6.SetSelection(self.tab[self.cliID, 5])
        self.rbox7.SetSelection(self.tab[self.cliID, 6])
        self.rbox8.SetSelection(self.tab[self.cliID, 7])
        self.rbox9.SetSelection(self.tab[self.cliID, 8])
        self.rbox10.SetSelection(self.tab[self.cliID, 9])

    def onRadioBox(self, e):
        self.tab[self.cliID, 0] = self.rbox1.GetSelection()
        self.tab[self.cliID, 1] = self.rbox2.GetSelection()
        self.tab[self.cliID, 2] = self.rbox3.GetSelection()
        self.tab[self.cliID, 3] = self.rbox4.GetSelection()
        self.tab[self.cliID, 4] = self.rbox5.GetSelection()
        self.tab[self.cliID, 5] = self.rbox6.GetSelection()
        self.tab[self.cliID, 6] = self.rbox7.GetSelection()
        self.tab[self.cliID, 7] = self.rbox8.GetSelection()
        self.tab[self.cliID, 8] = self.rbox9.GetSelection()
        self.tab[self.cliID, 9] = self.rbox10.GetSelection()
        self.Check()

    def Check(self):

        if Silnik.cos(self.tab[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 530))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color

    def OnButtonClicked(self, e):
        self.data.obsluha = self.tab
        self.Close()

class GUI_muzyka(wx.Frame):
    def __init__(self, parent, title, data):
        super(GUI_muzyka, self).__init__(parent, title=title, size=(1050, 620))
        self.data = data
        self.pictures_name = ["pub1.png", "pub2.png", "pub3.jpg", "pub1.png", "pub2.png"]
        self.Lista_miejsca = ['Club 1', 'Club 2', 'Club 3', 'Club 4', 'Club 5']
        self.List_Customer = ['Klient 1', 'Klient 2', 'Klient 3', 'Klient 4', 'Klient 5']
        self.lista_por = self.data.lista_por
        self.cliID = self.data.cliID
        self.Tensor = np.ones((len(self.pictures_name), len(self.Lista_miejsca), 5)) * 2


        # baza danych
        self.tab = self.data.muzyka
        #self.odleg = self.data.odleg
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.label = wx.StaticText(self.pnl, label="Jak porównujesz: ", pos=(150, 10))

        lblList = ['Najgorszy', 'Znacznie gorszy', 'Gorszy', 'Troche Gorszy', 'Takie same', 'Troche lepszy', 'Lepszy', 'Znacznie lepszy','Najlepszy']

        self.rbox1 = wx.RadioBox(self.pnl, label=self.lista_por[0], pos=(30, 30), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox2 = wx.RadioBox(self.pnl, label=self.lista_por[1], pos=(30, 80), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox3 = wx.RadioBox(self.pnl, label=self.lista_por[2], pos=(30, 130), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox4 = wx.RadioBox(self.pnl, label=self.lista_por[3], pos=(30, 180), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox4.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox5 = wx.RadioBox(self.pnl, label=self.lista_por[4], pos=(30, 230), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox5.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox6 = wx.RadioBox(self.pnl, label=self.lista_por[5], pos=(30, 280), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox6.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox7 = wx.RadioBox(self.pnl, label=self.lista_por[6], pos=(30, 330), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox7.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox8 = wx.RadioBox(self.pnl, label=self.lista_por[7], pos=(30, 380), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox8.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox9 = wx.RadioBox(self.pnl, label=self.lista_por[8], pos=(30, 430), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox9.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox10 = wx.RadioBox(self.pnl, label=self.lista_por[9], pos=(30, 480), choices=lblList,
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox10.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # odswiez wartosci
        self.SetSELECT()

        self.Button1 = wx.Button(self.pnl, label='OK', pos=(940, 540))
        self.Button1.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        self.Button2 = wx.Button(self.pnl, label='Kluby', pos=(940, 5))
        self.Button2.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Check()

        self.Centre()
        self.Show(True)

    def SetSELECT(self):
        self.rbox1.SetSelection(self.tab[self.cliID, 0])
        self.rbox2.SetSelection(self.tab[self.cliID, 1])
        self.rbox3.SetSelection(self.tab[self.cliID, 2])
        self.rbox4.SetSelection(self.tab[self.cliID, 3])
        self.rbox5.SetSelection(self.tab[self.cliID, 4])
        self.rbox6.SetSelection(self.tab[self.cliID, 5])
        self.rbox7.SetSelection(self.tab[self.cliID, 6])
        self.rbox8.SetSelection(self.tab[self.cliID, 7])
        self.rbox9.SetSelection(self.tab[self.cliID, 8])
        self.rbox10.SetSelection(self.tab[self.cliID, 9])

    def onRadioBox(self, e):
        self.tab[self.cliID, 0] = self.rbox1.GetSelection()
        self.tab[self.cliID, 1] = self.rbox2.GetSelection()
        self.tab[self.cliID, 2] = self.rbox3.GetSelection()
        self.tab[self.cliID, 3] = self.rbox4.GetSelection()
        self.tab[self.cliID, 4] = self.rbox5.GetSelection()
        self.tab[self.cliID, 5] = self.rbox6.GetSelection()
        self.tab[self.cliID, 6] = self.rbox7.GetSelection()
        self.tab[self.cliID, 7] = self.rbox8.GetSelection()
        self.tab[self.cliID, 8] = self.rbox9.GetSelection()
        self.tab[self.cliID, 9] = self.rbox10.GetSelection()
        self.Check()

    def Check(self):

        if Silnik.cos(self.tab[self.cliID, :])[0]:
            komunikat = ("Macierz jest spójna")
        else:
            komunikat = ("Macierz jest niespójna")
        try:
            self.txt.Destroy()
        except:
            pass
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(35, 530))
        self.txt.SetFont(font)
        if komunikat == ("Macierz jest spójna"):
            self.txt.SetForegroundColour((0,255,0)) # set text color
        else:
            self.txt.SetForegroundColour((255,0,0)) # set text color


    def OnButtonClicked(self, e):
        self.data.muzyka = self.tab
        self.Close()

    def OnButton(self,e):
        #  jak zdązymy do mozna dac podglad zdjecia
        GUI_cluby_info(None, 'Gdzie idziemy?', self.data)


class POP(wx.Frame):
    def __init__(self, parent, title, dane):
        super(POP, self).__init__(parent, title=title, size=(300, 200))
        self.txt = ['------', '------', '------', '------', '------']
        self.txt2 = 'Dane sa niespojne'
        self.dane = dane
        self.num = len(self.dane.name)
        self.InitUI()


    def InitUI(self):
        self.pnl = wx.Panel(self)
        self.Check_All()

        self.label1 = wx.StaticText(self.pnl, label="RANKING:", pos=(10, 10))
        self.label2 = wx.StaticText(self.pnl, label=self.txt2, pos=(150, 10))
        for i in range(self.num):
            self.label = wx.StaticText(self.pnl, label=self.txt[i], pos=(10, 30 + 20 * i))

        self.Centre()
        self.Show(True)

    def Check_All(self):


        # self.wybor = dictionary['wybor']
        # self.odleg = dictionary['odleglosc']
        # self.ceny = dictionary['ceny']
        # self.klimat = dictionary['klimat']
        #
        # self.dom = dictionary['dom']
        # self.pozycja = dictionary['pozycja']
        # self.centrum =  dictionary['centrum']
        # self.drinki = dictionary['drinki']
        # self.piwo = dictionary['piwo']
        # self.przystawki = dictionary['przystawki']
        # self.obsluga = dictionary['obsluga']
        # self.muzyka = dictionary['muzyka']
        #
        # self.op = dictionary['op']

        try:
            del self.dane.W_Dict
        except:
            pass
        self.dane.W_Dict={}
        var = True  # Czy sa spojne?
        for name in self.dane.database_name:
            self.dane.W_Dict[name] = []
            if name != 'op':
                for user in range(self.dane.Numbers_Customers+1):

                    v, w = Silnik.cos(self.dane.database[name][user, :])

                    temp = self.dane.W_Dict[name]
                    temp.append(w)
                    self.dane.W_Dict[name] = temp
                    if v:
                        pass
                    else:
                        var = False
        #dodac informacje gdzie dokladnie szukac danych
        # self.txt = wx.StaticText(self.pnl, label=komunikat, pos=(250, 540))
        if var:
            self.txt2 = 'Dane sa spojne'
            self.dane.W_Dict[name] = self.dane.database['op']
            ranking = Silnik.make_licz(self.dane.W_Dict, self.dane.Numbers_Customers + 1)
            sort_rank = np.argsort(np.multiply(ranking, -1))

            # print ranking
            i = 0
            for pub in sort_rank:
                self.txt[i] = self.dane.name[pub] + " - "+ str(ranking[pub])
                i += 1
            # print self.dane.name
        else:
            self.txt2 = 'Dane sa niespojne'



        # self.txt[1] = str(temp2)
        # print temp2
ex = wx.App()
Mywin(None, 'Gdzie idziemy?')
ex.MainLoop()

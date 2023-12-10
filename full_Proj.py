import sys
import sqlite3
import random

from PyQt5.Qt import *
from PyQt5 import uic

SCREEN_SIZE = [1300, 1000]
coord_all = []
coord_grass = []
can_move = True
u_all_poke = []
bug_poke = {}
bug = []
pc = []


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)
        self.initUI()
        con = sqlite3.connect('Object')
        cur = con.cursor()
        cur.execute(f"""UPDATE NPC
SET number_dialoga = '0'""")
        con.commit()
        con.close()
        self.np = Npc
        self.NPC_s()
        self.textBrowser.keyPressEvent = self.keyPressEvent
        self.x = 80
        self.y = 240
        self.player()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Покемон')
        self.pixmap_1 = QPixmap('pixil-frame-0.png')
        self.image_1 = QLabel(self)
        self.image_1.move(80, 80)
        self.image_1.resize(800, 800)
        self.image_1.setPixmap(self.pixmap_1)
        self.stroka = 0

    def player(self):
        self.pixmap_2 = QPixmap('pict object/trchar000_down.png')
        self.image_2 = QLabel(self)
        self.image_2.move(self.x, self.y)
        self.image_2.resize(80, 80)
        self.image_2.setPixmap(self.pixmap_2)
        self.storona = 1

    def keyPressEvent(self, event):
        try:
            global can_move
            move = False
            if event.key() == Qt.Key_Left:
                if can_move == True:
                    if self.x == 80 or (str(self.x - 80) + ',' + str(self.y)) in coord_all:
                        pass
                    else:
                        self.x -= 80
                    self.storona = -2
                    self.pixmap_2 = QPixmap('pict object/trchar000_left.png')
                    self.image_2.setPixmap(self.pixmap_2)
                    move = True
            elif event.key() == Qt.Key_Right:
                if can_move == True:
                    if self.x == 800 or (str(self.x + 80) + ',' + str(self.y)) in coord_all:
                        pass
                    else:
                        self.x += 80
                    self.storona = 2
                    self.pixmap_2 = QPixmap('pict object/trchar000_right.png')
                    self.image_2.setPixmap(self.pixmap_2)
                    move = True
            elif event.key() == Qt.Key_Up:
                if can_move == True:
                    if self.y == 80 or (str(self.x) + ',' + str(self.y - 80)) in coord_all:
                        pass
                    else:
                        self.y -= 80
                    self.storona = 1
                    self.pixmap_2 = QPixmap('pict object/trchar000_up.png')
                    self.image_2.setPixmap(self.pixmap_2)
                    move = True
            elif event.key() == Qt.Key_Down:
                if can_move == True:
                    if self.y == 800 or (str(self.x) + ',' + str(self.y + 80)) in coord_all:
                        pass
                    else:
                        self.y += 80
                    self.storona = -1
                    self.pixmap_2 = QPixmap('pict object/trchar000_down.png')
                    self.image_2.setPixmap(self.pixmap_2)
                    move = True
            elif event.key() == Qt.Key_D:
                self.NPC_Mex()
            self.image_2.move(self.x, self.y)
            if len(u_all_poke) > 0 and can_move == True and move == True:
                if str(self.x) + ',' + str(self.y) in coord_grass:
                    con = sqlite3.connect('Object')
                    cur = con.cursor()
                    pok = random.choice(cur.execute(f"""SELECT name FROM Pokemon""").fetchall())
                    lvl = ((cur.execute(f"""SELECT lvl FROM NPC
                    WHERE coord like '{str(self.x) + ',' + str(self.y)}'""").fetchall())[0][0]).split(',')
                    lvl_b = random.randint(int(lvl[0]), int(lvl[1]))
                    move = ((cur.execute(f"""SELECT Move FROM Pokemon
                    WHERE Name like '{pok[0]}'""").fetchall())[0][0]).split(',')
                    move_b = []
                    for i in range(0, len(move), 2):
                        if int(move[i + 1]) <= lvl_b:
                            move_b.append(move[i])
                    if len(move_b) < 4:
                        hp = cur.execute(f"""SELECT HP FROM Pokemon
                                WHERE name = '{pok[0]}'""").fetchall()
                        can_move = False
                        self.b = Battle([pok[0]], {pok[0]: f'{lvl_b},{hp[0][0] * lvl_b},{",".join(move_b)}'}, 'Wild')
                        self.b.show()
        except Exception as e:
            print(e)

    def NPC_s(self):
        self.np.Spawn(self)

    def NPC_Mex(self):
        self.np.Mech(self, self.storona, self.x, self.y)


class Npc(QMainWindow):

    def Spawn(self):
        con = sqlite3.connect('Object')
        cur = con.cursor()
        result = cur.execute("""SELECT name FROM NPC""").fetchall()
        self.image_3 = []
        k = 0
        for i in result:
            coord = cur.execute(f"""SELECT coord FROM NPC
            WHERE name like '{i[0]}'""").fetchall()
            storona = cur.execute(f"""SELECT storona FROM NPC
            WHERE name like '{i[0]}'""").fetchall()
            pict = cur.execute(f"""SELECT pictur FROM NPC
            WHERE name like '{i[0]}'""").fetchall()
            Vid = cur.execute(f"""SELECT Vid FROM NPC
            WHERE name like '{i[0]}'""").fetchall()
            step = cur.execute(f"""SELECT step FROM NPC
            WHERE name like '{i[0]}'""").fetchall()
            self.pixmap_3 = QPixmap(f'pict object/{pict[0][0]}_{storona[0][0]}.png')
            self.image_3.append(QLabel(self))
            if step[0][0] == 'No':
                coord_all.append(coord[0][0])
            if Vid[0][0] == 'Land':
                coord_grass.append(coord[0][0])
            x, y = coord[0][0].split(',')
            self.image_3[k].move(int(x), int(y))
            self.image_3[k].resize(80, 80)
            self.image_3[k].setPixmap(self.pixmap_3)
            k += 1
        con.close()

    def Mech(self, storona, x, y):
        con = sqlite3.connect('Object')
        cur = con.cursor()
        global can_move
        if storona == -1:
            deiv = cur.execute(f"""SELECT mechain FROM NPC
            WHERE coord like '{str(x) + ',' + str(y + 80)}'""").fetchall()
            k = str(x) + ',' + str(y + 80)
        elif storona == 1:
            deiv = cur.execute(f"""SELECT mechain FROM NPC
            WHERE coord like '{str(x) + ',' + str(y - 80)}'""").fetchall()
            k = str(x) + ',' + str(y - 80)
        elif storona == -2:
            deiv = cur.execute(f"""SELECT mechain FROM NPC
            WHERE coord like '{str(x - 80) + ',' + str(y)}'""").fetchall()
            k = str(x - 80) + ',' + str(y)
        elif storona == 2:
            deiv = cur.execute(f"""SELECT mechain FROM NPC
            WHERE coord like '{str(x + 80) + ',' + str(y)}'""").fetchall()
            k = str(x + 80) + ',' + str(y)
        if k in coord_all:
            self.num = cur.execute(f"""SELECT num FROM NPC
                    WHERE coord like '{k}'""").fetchall()
            if deiv[0][0] == 'dialog':
                num_1 = cur.execute(f"""SELECT num FROM NPC
                WHERE coord like '{k}'""").fetchall()
                pict = cur.execute(f"""SELECT pictur FROM NPC
                WHERE coord like '{k}'""").fetchall()
                can_move = False
                fil = cur.execute(f"""SELECT dialog FROM NPC
                WHERE coord like '{k}'""").fetchall()
                char = cur.execute(f"""SELECT number_dialoga FROM NPC
                WHERE coord like '{k}'""").fetchall()
                self.pixmap_3 = QPixmap(f'pict object/{pict[0][0]}_{storona * -1}.png')
                self.image_3[num_1[0][0]].setPixmap(self.pixmap_3)
                f = open(f'{fil[0][0]}', encoding='utf8')
                a = f.readlines()
                n = char[0][0]
                if n < len(a):
                    self.textBrowser.setText(f'{a[n]}')
                    n += 1
                    cur.execute(f'''UPDATE NPC
    SET number_dialoga = '{n}'
    WHERE coord = "{k}"''')
                    con.commit()
                elif len(a) == n:
                    can_move = True
                    self.textBrowser.setText('')
                    f.close()
                    con.close()
            elif deiv[0][0] == 'quest':
                self.initUI()
                que = cur.execute(f"""SELECT quest FROM NPC
                WHERE coord like '{k}'""").fetchall()
                f = open(f'{que[0][0]}', encoding='utf8')
                a = f.readlines()
                d = []
                for i in a[1:]:
                    d.append(i.rstrip())
                self.country, ok_pressed = QInputDialog.getItem(
                    self, "Выберите", f"{a[0]}",
                    d, 1, False)
                if ok_pressed:
                    lvl = cur.execute(f"""SELECT lvl FROM NPC
                WHERE coord like '{k}'""").fetchall()
                    Move = cur.execute(f"""SELECT Move FROM Pokemon
                WHERE name like '{self.country}'""").fetchall()
                    at = []
                    v = str(Move[0][0]).split(',')
                    for i in range(0, len(v), +2):
                        if int(v[i + 1]) < int(lvl[0][0]):
                            at.append(v[i])
                    hp = cur.execute(f"""SELECT HP FROM Pokemon
                    WHERE name = '{self.country}'""").fetchall()
                    bug_poke[f'{self.country}_0'] = str(lvl[0][0]) + ',' + str(int(hp[0][0]) * int(lvl[0][0])) \
                                                  + ',' + ','.join(at)
                    u_all_poke.append(f'{self.country}_0')
                    self.pixmap_3 = QPixmap('')
                    self.image_3[self.num[0][0]].setPixmap(self.pixmap_3)
                    coord_all.remove(k)
                    try:
                        if self.num[0][0] == 1:
                            can_move = False
                            if self.country == 'Squirtle':
                                self.b = Battle(['Charmander'], {'Charmander': '15,585,Scratch,Ember'}, 'Npc')
                                self.b.show()
                            elif self.country == 'Charmander':
                                self.b = Battle(['Bulbasaur'], {'Bulbasaur': '15,675,Tackle,Vine Whip'}, 'Npc')
                                self.b.show()
                            elif self.country == 'Bulbasaur':
                                self.b = Battle(['Squirtle'], {'Squirtle': '15,660,Tackle,Bubble'}, 'Npc')
                                self.b.show()
                    except:
                        pass
            elif deiv[0][0] == 'heal':
                con = sqlite3.connect('Object')
                cur = con.cursor()
                for i in u_all_poke:
                    b = bug_poke[i].split(',')
                    hp = cur.execute(f"""SELECT HP FROM Pokemon
                    WHERE name = '{i[:i.find('_')]}'""").fetchall()
                    c = [b[0], str(int(hp[0][0]) * int(b[0]))] + b[2:]
                    bug_poke[i] = ','.join(c)
            elif deiv[0][0] == 'pc':
                if len(u_all_poke) > 0:
                    can_move = False
                    self.p = PC()
                    self.p.show()
            con.close()

    def initUI(self):
        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Диалоговые окна')


class Battle(QMainWindow):
    def __init__(self, opponent_1, opponent_2, op):
        super().__init__()
        uic.loadUi('Pok.ui', self)
        self.pushButton_next.setEnabled(False)
        self.pushButton_ok.setEnabled(False)
        self.opponent_1 = opponent_1
        self.opponent_2 = opponent_2
        con = sqlite3.connect('Object')
        cur = con.cursor()
        self.see_pok = ((u_all_poke[0])[:u_all_poke[0].find('_')])
        pict = cur.execute(f"""SELECT pictur FROM Pokemon
        WHERE name = '{self.see_pok}'""").fetchall()
        self.pixmap_4 = QPixmap(f'pict pokemon/{pict[0][0]}.png')
        self.image_4 = QLabel(self)
        self.image_4.move(40, 70)
        self.image_4.resize(181, 231)
        self.image_4.setPixmap(self.pixmap_4)
        self.pixmap_5 = QPixmap(f'pict pokemon/{self.opponent_1[0]}.png')
        self.image_5 = QLabel(self)
        self.image_5.move(720, 70)
        self.image_5.resize(181, 231)
        self.image_5.setPixmap(self.pixmap_5)
        self.die = False
        self.Spawn()
        self.op = op
        if self.op == 'Npc':
            self.pushButton_Pokeball.setEnabled(False)
            self.pushButton_Run.setEnabled(False)
        self.pushButton_Attack.clicked.connect(self.Attack_see)
        self.pushButton_Pokemon.clicked.connect(self.Pokemon_see)
        self.pushButton_Pokeball.clicked.connect(self.Pokeball_see)
        self.pushButton_ok.clicked.connect(self.Attack)
        self.pushButton_next.clicked.connect(self.Attack_op)
        self.pushButton_Run.clicked.connect(self.Run)

    def Run(self):
        global can_move
        can_move = True
        self.close()


    def Pokeball_see(self):
        a = 'Pokeball 25% \n' \
            'Greatball 50% \n' \
            'Ultraball 75%\n' \
            'Masterball 100%'
        self.you_label.setText(a)
        self.menu = 'Pokeball'
        self.pushButton_ok.setEnabled(True)


    def Pokemon_see(self):
        a = f'1){u_all_poke[0]}, {(bug_poke[u_all_poke[0]].split(","))[1]} HP [используется]\n'
        try:
            a = a + f'2){u_all_poke[1]}, {(bug_poke[u_all_poke[1]].split(","))[1]} HP \n'
            try:
                a += f'3){u_all_poke[2]}, {(bug_poke[u_all_poke[2]].split(","))[1]} HP \n'
                try:
                    a += f'4){u_all_poke[3]}, {(bug_poke[u_all_poke[3]].split(","))[1]} HP \n'
                    try:
                        a += f'5){u_all_poke[4]}, {(bug_poke[u_all_poke[4]].split(","))[1]} HP \n'
                        try:
                            a += f'6){u_all_poke[5]}, {(bug_poke[u_all_poke[5]].split(","))[1]} HP \n'
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass
        self.you_label.setText(a)
        self.menu = 'Pokemon'
        self.pushButton_ok.setEnabled(True)

    def Spawn(self):
        global bug_poke
        con = sqlite3.connect('Object')
        cur = con.cursor()
        self.see_pok = ((u_all_poke[0])[:u_all_poke[0].find('_')])
        pict = cur.execute(f"""SELECT pictur FROM Pokemon
        WHERE name = '{self.see_pok}'""").fetchall()
        self.oponent = self.opponent_1[0]
        self.stat_op = self.opponent_2[self.oponent].split(',')
        self.op_move = self.stat_op[2:]
        self.op_lvl = self.stat_op[0]
        at = cur.execute(f"""SELECT Attack FROM Pokemon
        WHERE name = '{self.see_pok}'""").fetchall()
        df = cur.execute(f"""SELECT Defense FROM Pokemon
        WHERE name = '{self.see_pok}'""").fetchall()
        self.u_at = at[0][0]
        self.u_df = df[0][0]
        at = cur.execute(f"""SELECT Attack FROM Pokemon
        WHERE name = '{self.oponent}'""").fetchall()
        df = cur.execute(f"""SELECT Defense FROM Pokemon
        WHERE name = '{self.oponent}'""").fetchall()
        self.op_hp = self.stat_op[1]
        self.op_at = at[0][0]
        self.op_df = df[0][0]
        self.pixmap_4 = QPixmap(f'pict pokemon/{pict[0][0]}.png')
        self.image_4.setPixmap(self.pixmap_4)
        self.pixmap_5 = QPixmap(f'pict pokemon/{self.oponent}.png')
        self.image_5.setPixmap(self.pixmap_5)
        self.u_move = bug_poke[u_all_poke[0]].split(',')
        a = f'{self.see_pok}:{self.u_move[1]} \n' \
            f'lvl:{self.u_move[0]} \n'
        self.you_label.setText(a)
        b = f'{self.oponent}:{self.op_hp} \n' \
            f'lvl:{self.op_lvl} \n' \
            f'1){self.op_move[0]} \n'
        try:
            b = b + f'2){self.op_move[1]} \n'
            try:
                b += f'3){self.op_move[2]} \n'
                try:
                    b += f'4){self.op_move[3]} \n'
                except:
                    pass
            except:
                pass
        except:
            pass
        self.oponent_label.setText(b)
        con.close()

    def Attack_see(self):
        a = f'{self.see_pok}:{self.u_move[1]} \n' \
            f'lvl:{self.u_move[0]} \n' \
            f'1){self.u_move[2]} \n'
        try:
            a = a + f'2){self.u_move[3]} \n'
            try:
                a += f'3){self.u_move[4]} \n'
                try:
                    a += f'4){self.u_move[5]} \n'
                except:
                    pass
            except:
                pass
        except:
            pass
        self.you_label.setText(a)
        self.menu = 'attack'
        self.pushButton_ok.setEnabled(True)

    def Attack(self):
        global bug_poke
        global can_move
        if self.menu == 'attack':
            if self.you_attack.text() in self.u_move:
                con = sqlite3.connect('Object')
                cur = con.cursor()
                at = self.you_attack.text()
                at_type = cur.execute(f"""SELECT type FROM Attack
                WHERE name = '{at}'""").fetchall()
                at_dm = cur.execute(f"""SELECT Dmg FROM Attack
                WHERE name = '{at}'""").fetchall()
                op_type = cur.execute(f"""SELECT Type FROM Pokemon
                WHERE name = '{self.oponent}'""").fetchall()
                eff = cur.execute(f"""SELECT {op_type[0][0]} FROM Effect
                WHERE name = '{at_type[0][0]}'""").fetchall()
                a = f'{self.see_pok} использует {at} \n'
                if eff[0][0] == 2:
                    a += 'Аттака была эффективной \n'
                elif eff[0][0] == 0.5:
                    a += 'Аттака была неэффективной \n'
                elif eff[0][0] == 1:
                    a += 'Аттака была обычной \n'
                lvl_up = cur.execute(f"""SELECT lvl_up FROM Pokemon
                WHERE name = '{self.see_pok}'""").fetchall()
                self.textBrowser.setText(a)
                self.op_hp = int(self.op_hp) - round(self.u_at * lvl_up[0][0] * int(self.u_move[0])
                                                     * at_dm[0][0] * eff[0][0])
                c = [self.stat_op[0], str(self.op_hp)] + self.stat_op[2:]
                self.opponent_2[self.oponent] = ','.join(c)
                if self.op_hp > 0:
                    self.Spawn()
                    self.pushButton_ok.setEnabled(False)
                    self.pushButton_Attack.setEnabled(False)
                    self.pushButton_Pokemon.setEnabled(False)
                    self.pushButton_Pokeball.setEnabled(False)
                    self.pushButton_Run.setEnabled(False)
                    self.pushButton_next.setEnabled(True)
                else:
                    b = bug_poke[u_all_poke[0]].split(',')
                    m = u_all_poke[0][:u_all_poke[0].find('_')]
                    c = [str(int(b[0]) + 1)] + b[1:]
                    lvl_ev = cur.execute(f"""SELECT Evolv FROM Pokemon
                WHERE name = '{m}'""").fetchall()
                    if int(b[0]) + 1 == lvl_ev[0][0]:
                        pok_ev = cur.execute(f"""SELECT Pok_ev FROM Pokemon
                WHERE name = '{m}'""").fetchall()
                        hp = cur.execute(f"""SELECT HP FROM Pokemon
                WHERE name = '{pok_ev[0][0]}'""").fetchall()
                        move = ((cur.execute(f"""SELECT Move FROM Pokemon
                        WHERE Name like '{pok_ev[0][0]}'""").fetchall())[0][0]).split(',')
                        move_b = []
                        for i in range(0, len(move), 2):
                            if int(move[i + 1]) <= (int(b[0]) + 1):
                                move_b.append(move[i])
                        j = 0
                        while (u_all_poke.count(f'{pok_ev[0][0]}_{j}') != 0) or (pc.count(f'{pok_ev[0][0]}_{j}') != 0):
                            j += 1
                        av = f'{pok_ev[0][0]}_{j}'
                        u_all_poke.pop(0)
                        u_all_poke.insert(0, av)
                        c = [str(int(b[0]) + 1), str(int(hp[0][0]) * (int(b[0]) + 1))] + move_b
                    bug_poke[u_all_poke[0]] = ','.join(c)
                    self.close()
                    can_move = True
                con.close()
        elif self.menu == 'Pokemon':
            if self.you_attack.text() in u_all_poke:
                s = self.you_attack.text()
                if (bug_poke[s].split(','))[1] != '0' and s != u_all_poke[0]:
                    u_all_poke.remove(s)
                    u_all_poke.insert(0, s)
                    self.Spawn()
                    if self.die == True:
                        self.pushButton_ok.setEnabled(True)
                        self.pushButton_Attack.setEnabled(True)
                        self.pushButton_Pokemon.setEnabled(True)
                        self.pushButton_Pokeball.setEnabled(True)
                        self.pushButton_Run.setEnabled(True)
                        self.pushButton_next.setEnabled(False)
                        self.die = False
                    else:
                        self.pushButton_ok.setEnabled(False)
                        self.pushButton_Attack.setEnabled(False)
                        self.pushButton_Pokemon.setEnabled(False)
                        self.pushButton_Pokeball.setEnabled(False)
                        self.pushButton_Run.setEnabled(False)
                        self.pushButton_next.setEnabled(True)
        elif self.menu == 'Pokeball':
            pokeb = ['Pokeball', 'Greatball', 'Ultraball', 'Masterball']
            if self.you_attack.text() in pokeb:
                i = 0
                while (u_all_poke.count(f'{self.opponent_1[0]}_{i}') != 0) or (pc.count(f'{self.opponent_1[0]}_{i}') != 0):
                    i += 1
                av = f'{self.opponent_1[0]}_{i}'
                if self.you_attack.text() == 'Pokeball':
                    chan = random.randint(1, 4)
                    if chan == 1:
                        if len(u_all_poke) < 6:
                            u_all_poke.append(av)
                        else:
                            pc.append(av)
                        bug_poke[av] = self.opponent_2[self.opponent_1[0]]
                        self.textBrowser.setText(f'Вы поймали {self.opponent_1[0]}')
                        self.close()
                        can_move = True
                    else:
                        self.textBrowser.setText(f'Вам не удалось поймать {self.opponent_1[0]}')
                        self.pushButton_next.setEnabled(True)
                elif self.you_attack.text() == 'Greatball':
                    chan = random.randint(1, 2)
                    if chan == 1:
                        if len(u_all_poke) < 6:
                            u_all_poke.append(av)
                        else:
                            pc.append(av)
                        bug_poke[av] = self.opponent_2[self.opponent_1[0]]
                        self.textBrowser.setText(f'Вы поймали {self.opponent_1[0]}')
                        self.close()
                        can_move = True
                    else:
                        self.textBrowser.setText(f'Вам не удалось поймать {self.opponent_1[0]}')
                        self.pushButton_next.setEnabled(True)
                elif self.you_attack.text() == 'Ultraball':
                    chan = random.randint(1, 4)
                    if chan != 1:
                        if len(u_all_poke) < 6:
                            u_all_poke.append(av)
                        else:
                            pc.append(av)
                        bug_poke[av] = self.opponent_2[self.opponent_1[0]]
                        self.textBrowser.setText(f'Вы поймали {self.opponent_1[0]}')
                        self.close()
                        can_move = True
                    else:
                        self.textBrowser.setText(f'Вам не удалось поймать {self.opponent_1[0]}')
                        self.pushButton_next.setEnabled(True)
                elif self.you_attack.text() == 'Masterball':
                    if len(u_all_poke) < 6:
                        u_all_poke.append(av)
                    else:
                        pc.append(av)
                    bug_poke[av] = self.opponent_2[self.opponent_1[0]]
                    self.textBrowser.setText(f'Вы поймали {self.opponent_1[0]}')
                    self.close()
                    can_move = True
                self.pushButton_next.setEnabled(True)
                self.pushButton_Attack.setEnabled(False)
                self.pushButton_Pokemon.setEnabled(False)
                self.pushButton_Pokeball.setEnabled(False)
                self.pushButton_Run.setEnabled(False)
                self.pushButton_ok.setEnabled(False)


    def Attack_op(self):
        global bug_poke
        global can_move
        con = sqlite3.connect('Object')
        cur = con.cursor()
        at = random.choice(self.op_move)
        at_type = cur.execute(f"""SELECT type FROM Attack
        WHERE name = '{at}'""").fetchall()
        at_dm = cur.execute(f"""SELECT Dmg FROM Attack
        WHERE name = '{at}'""").fetchall()
        u_type = cur.execute(f"""SELECT Type FROM Pokemon
        WHERE name = '{self.see_pok}'""").fetchall()
        eff = cur.execute(f"""SELECT {u_type[0][0]} FROM Effect
        WHERE name = '{at_type[0][0]}'""").fetchall()
        a = f'{self.oponent} использует {at} \n'
        if eff[0][0] == 2:
            a += 'Аттака была эффективной \n'
        elif eff[0][0] == 0.5:
            a += 'Аттака была неэффективной \n'
        elif eff[0][0] == 1:
            a += 'Аттака была обычной \n'
        lvl_up = cur.execute(f"""SELECT lvl_up FROM Pokemon
        WHERE name = '{self.oponent}'""").fetchall()
        self.textBrowser.setText(a)
        b = bug_poke[u_all_poke[0]].split(',')
        self.u_hp = b[1]
        self.u_hp = int(self.u_hp) - round(self.op_at * lvl_up[0][0] * int(self.stat_op[0]) * at_dm[0][0] * eff[0][0])
        if self.u_hp > 0:
            c = [b[0], str(self.u_hp)] + b[2:]
            bug_poke[u_all_poke[0]] = ','.join(c)
            self.Spawn()
            self.pushButton_ok.setEnabled(True)
            self.pushButton_Attack.setEnabled(True)
            self.pushButton_Pokemon.setEnabled(True)
            if self.op != 'Npc':
                self.pushButton_Pokeball.setEnabled(True)
                self.pushButton_Run.setEnabled(True)
            self.menu = ''
        else:
            self.u_hp = '0'
            c = [b[0], str(self.u_hp)] + b[2:]
            bug_poke[u_all_poke[0]] = ','.join(c)
            k = 0
            for i in u_all_poke:
                if (bug_poke[i].split(','))[1] == '0':
                    k += 1
            if k == len(u_all_poke):
                self.close()
                can_move = True
            else:
                self.die = True
                self.Pokemon_see()
        self.pushButton_next.setEnabled(False)
        con.close()


class PC(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('pc.ui', self)
        self.start()
        self.pushButton_okey.clicked.connect(self.OK)
        self.pushButton_exit.clicked.connect(self.Ex)

    def Ex(self):
        global can_move
        can_move = True
        self.close()

    def start(self):
        a = ''
        for i in u_all_poke:
            a += f'{i} {(bug_poke[i].split(","))[1]} HP, {(bug_poke[i].split(","))[0]} LVL \n'
        self.textBrowser_u_all_pok.setText(a)
        a = ''
        for i in pc:
            a += f'{i} {(bug_poke[i].split(","))[1]} HP, {(bug_poke[i].split(","))[0]} LVL \n'
        self.textBrowser_pc.setText(a)

    def OK(self):
        if self.lineEdit_u_all_pok.text() in u_all_poke:
            if len(u_all_poke) - 1 > 0:
                u_all_poke.remove(self.lineEdit_u_all_pok.text())
                pc.append(self.lineEdit_u_all_pok.text())
        if self.lineEdit_pc.text() in pc:
            if len(u_all_poke) < 6:
                u_all_poke.append(self.lineEdit_pc.text())
                pc.remove(self.lineEdit_pc.text())
        self.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

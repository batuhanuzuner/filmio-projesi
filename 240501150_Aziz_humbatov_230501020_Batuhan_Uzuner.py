import sys
import re
from datetime import datetime
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QListWidget, QComboBox,
    QTextEdit, QSpinBox, QListWidgetItem, QCheckBox, QScrollArea,
    QFrame, QGridLayout, QStackedWidget
)
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize

NETFLIX_STYLE = """
QWidget {
    background-color: #141414;
    color: #FFFFFF;
    font-family: Arial;
    font-size: 13px;
}
QLabel {
    color: #FFFFFF;
    font-size: 13px;
}
QLabel#baslik {
    font-size: 28px;
    font-weight: bold;
    color: #E50914;
}
QLabel#alt_baslik {
    font-size: 18px;
    font-weight: bold;
    color: #FFFFFF;
}
QLabel#logo {
    font-size: 36px;
    font-weight: bold;
    color: #E50914;
    letter-spacing: 4px;
}
QLineEdit {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 10px;
    font-size: 14px;
    min-height: 20px;
}
QLineEdit:focus {
    border: 1px solid #E50914;
}
QLineEdit::placeholder {
    color: #AAAAAA;
}
QPushButton {
    background-color: #E50914;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #F40612;
}
QPushButton:pressed {
    background-color: #B20710;
}
QPushButton#ikincil {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #555555;
}
QPushButton#ikincil:hover {
    background-color: #444444;
}
QPushButton#tehlikeli {
    background-color: #555555;
    color: #FFFFFF;
}
QPushButton#tehlikeli:hover {
    background-color: #666666;
}
QComboBox {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 8px;
    font-size: 13px;
    min-height: 20px;
}
QComboBox:focus {
    border: 1px solid #E50914;
}
QComboBox QAbstractItemView {
    background-color: #333333;
    color: #FFFFFF;
    selection-background-color: #E50914;
}
QComboBox::drop-down {
    border: none;
}
QListWidget {
    background-color: #1F1F1F;
    color: #FFFFFF;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 4px;
    font-size: 13px;
}
QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #2A2A2A;
}
QListWidget::item:selected {
    background-color: #E50914;
    color: #FFFFFF;
}
QListWidget::item:hover {
    background-color: #2A2A2A;
}
QTextEdit {
    background-color: #1F1F1F;
    color: #FFFFFF;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 8px;
    font-size: 13px;
}
QSpinBox {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 8px;
    font-size: 13px;
    min-height: 20px;
}
QSpinBox:focus {
    border: 1px solid #E50914;
}
QScrollBar:vertical {
    background: #1F1F1F;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #555555;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #E50914;
}
QMessageBox {
    background-color: #141414;
    color: #FFFFFF;
}
QMessageBox QPushButton {
    min-width: 80px;
}
"""


def baglanti_olustur():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234567890",
        database="netflix_proje"
    )



class Kullanici:
    def __init__(self, kullanici_id, ad, soyad, email, dogum_tarihi, cinsiyet, ulke, rol_id, aktif_mi=True):
        self.kullanici_id = kullanici_id
        self.ad = ad
        self.soyad = soyad
        self.email = email
        self.dogum_tarihi = dogum_tarihi
        self.cinsiyet = cinsiyet
        self.ulke = ulke
        self.rol_id = rol_id
        self.aktif_mi = aktif_mi

    def profil_guncelle(self, ad=None, soyad=None, ulke=None, sifre=None):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        if ad:
            cursor.execute("UPDATE Kullanici SET ad=%s WHERE kullanici_id=%s", (ad, self.kullanici_id))
            self.ad = ad
        if soyad:
            cursor.execute("UPDATE Kullanici SET soyad=%s WHERE kullanici_id=%s", (soyad, self.kullanici_id))
            self.soyad = soyad
        if ulke:
            cursor.execute("UPDATE Kullanici SET ulke=%s WHERE kullanici_id=%s", (ulke, self.kullanici_id))
            self.ulke = ulke
        if sifre:
            cursor.execute("UPDATE Kullanici SET sifre=%s WHERE kullanici_id=%s", (sifre, self.kullanici_id))

        conn.commit()
        cursor.close()
        conn.close()

    def favori_ekle(self, program_id):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Favori WHERE kullanici_id=%s AND program_id=%s",
                      (self.kullanici_id, program_id))

        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False

        cursor.execute("INSERT INTO Favori (kullanici_id, program_id) VALUES (%s, %s)",
                      (self.kullanici_id, program_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def favori_cikar(self, program_id):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Favori WHERE kullanici_id=%s AND program_id=%s",
                      (self.kullanici_id, program_id))
        conn.commit()
        cursor.close()
        conn.close()


class Admin(Kullanici):
    def __init__(self, kullanici_id, ad, soyad, email, dogum_tarihi, cinsiyet, ulke, rol_id, aktif_mi=True):
        super().__init__(kullanici_id, ad, soyad, email, dogum_tarihi, cinsiyet, ulke, rol_id, aktif_mi)

    def kullanici_pasif_yap(self, kullanici_id):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("UPDATE Kullanici SET aktif_mi=FALSE WHERE kullanici_id=%s", (kullanici_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def kullanici_aktif_yap(self, kullanici_id):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("UPDATE Kullanici SET aktif_mi=TRUE WHERE kullanici_id=%s", (kullanici_id,))
        conn.commit()
        cursor.close()
        conn.close()


class Program:
    def __init__(self, program_id, ad, aciklama, tip, yayin_yili, sure, bolum_sayisi, ortalama_puan, toplam_izlenme):
        self.program_id = program_id
        self.ad = ad
        self.aciklama = aciklama
        self.tip = tip
        self.yayin_yili = yayin_yili
        self.sure = sure
        self.bolum_sayisi = bolum_sayisi
        self.ortalama_puan = ortalama_puan
        self.toplam_izlenme = toplam_izlenme

    def puan_guncelle(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Program
            SET ortalama_puan = (
                SELECT AVG(verilen_puan)
                FROM KullaniciProgram
                WHERE program_id = %s AND verilen_puan IS NOT NULL
            )
            WHERE program_id = %s
        """, (self.program_id, self.program_id))
        conn.commit()
        cursor.close()
        conn.close()

    def izlenme_artir(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("UPDATE Program SET izlenme_sayisi = izlenme_sayisi + 1 WHERE program_id = %s",
                      (self.program_id,))
        conn.commit()
        cursor.close()
        conn.close()


class Film(Program):
    def __init__(self, program_id, ad, aciklama, yayin_yili, sure, ortalama_puan, toplam_izlenme):
        super().__init__(program_id, ad, aciklama, "Film", yayin_yili, sure, 1, ortalama_puan, toplam_izlenme)


class Dizi(Program):
    def __init__(self, program_id, ad, aciklama, yayin_yili, sure, bolum_sayisi, ortalama_puan, toplam_izlenme):
        super().__init__(program_id, ad, aciklama, "Dizi", yayin_yili, sure, bolum_sayisi, ortalama_puan, toplam_izlenme)

    def bolum_listesi_getir(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bolum WHERE program_id=%s ORDER BY bolum_no", (self.program_id,))
        bolumler = cursor.fetchall()
        cursor.close()
        conn.close()
        return bolumler


class Tur:
    def __init__(self, tur_id, tur_adi):
        self.tur_id = tur_id
        self.tur_adi = tur_adi



class AuthService:
    @staticmethod
    def giris_yap(email, sifre):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT kullanici_id, rol_id, ad, soyad, dogum_tarihi, cinsiyet, ulke, aktif_mi
            FROM Kullanici
            WHERE email=%s AND sifre=%s AND aktif_mi=TRUE
        """, (email, sifre))

        result = cursor.fetchone()

        if result:
            cursor.execute("INSERT INTO OturumLog (kullanici_id) VALUES (%s)", (result[0],))
            conn.commit()

            if result[1] == 2:
                kullanici = Admin(result[0], result[2], result[3], email, result[4], result[5], result[6], result[1], result[7])
            else:
                kullanici = Kullanici(result[0], result[2], result[3], email, result[4], result[5], result[6], result[1], result[7])

            cursor.close()
            conn.close()
            return kullanici

        cursor.close()
        conn.close()
        return None

    @staticmethod
    def kayit_ol(ad, soyad, email, sifre, dogum_tarihi, cinsiyet, ulke, secilen_turler):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("SELECT kullanici_id FROM Kullanici WHERE email=%s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return None

        cursor.execute("""
            INSERT INTO Kullanici
            (rol_id, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, ulke)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (1, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, ulke))

        kullanici_id = cursor.lastrowid

        for tur_id in secilen_turler:
            cursor.execute("INSERT INTO KullaniciTur (kullanici_id, tur_id) VALUES (%s, %s)",
                          (kullanici_id, tur_id))

        conn.commit()
        cursor.close()
        conn.close()

        return kullanici_id


class RecommendationService:
    @staticmethod
    def kayit_sonrasi_oneriler(secilen_turler):
        """Kayıt sırasında seçilen 3 türden her biri için en yüksek puanlı 2 içerik"""
        conn = baglanti_olustur()
        cursor = conn.cursor()

        oneriler = []

        for tur_id in secilen_turler:
            cursor.execute("""
                SELECT p.program_id, p.program_adi, p.program_tipi, p.ortalama_puan
                FROM Program p
                JOIN ProgramTur pt ON p.program_id = pt.program_id
                WHERE pt.tur_id = %s
                ORDER BY p.ortalama_puan DESC
                LIMIT 2
            """, (tur_id,))

            oneriler.extend(cursor.fetchall())

        cursor.close()
        conn.close()

        return oneriler

    @staticmethod
    def kullanici_onerileri(kullanici_id):
        """Kullanıcının favori türlerine, izleme geçmişine ve benzer kullanıcılara göre öneriler"""
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("SELECT tur_id FROM KullaniciTur WHERE kullanici_id=%s", (kullanici_id,))
        favori_turler = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT DISTINCT pt.tur_id FROM KullaniciProgram kp
            JOIN ProgramTur pt ON kp.program_id = pt.program_id
            WHERE kp.kullanici_id=%s AND kp.verilen_puan >= 7
        """, (kullanici_id,))
        yuksek_puan_turler = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT DISTINCT p.program_id, p.program_adi, p.program_tipi, p.ortalama_puan, p.izlenme_sayisi
            FROM KullaniciProgram kp2
            JOIN Program p ON kp2.program_id = p.program_id
            WHERE kp2.kullanici_id IN (
                SELECT DISTINCT kt2.kullanici_id FROM KullaniciTur kt2
                WHERE kt2.tur_id IN (
                    SELECT tur_id FROM KullaniciTur WHERE kullanici_id=%s
                ) AND kt2.kullanici_id != %s
            )
            AND p.program_id NOT IN (
                SELECT program_id FROM KullaniciProgram WHERE kullanici_id=%s
            )
            ORDER BY p.ortalama_puan DESC, p.izlenme_sayisi DESC
            LIMIT 5
        """, (kullanici_id, kullanici_id, kullanici_id))
        benzer_oneriler = cursor.fetchall()

        tum_turler = list(set(favori_turler + yuksek_puan_turler))

        if tum_turler:
            placeholders = ','.join(['%s'] * len(tum_turler))
            cursor.execute(f"""
                SELECT DISTINCT p.program_id, p.program_adi, p.program_tipi, p.ortalama_puan, p.izlenme_sayisi
                FROM Program p
                JOIN ProgramTur pt ON p.program_id = pt.program_id
                WHERE pt.tur_id IN ({placeholders})
                AND p.program_id NOT IN (
                    SELECT program_id FROM KullaniciProgram WHERE kullanici_id=%s
                )
                ORDER BY p.ortalama_puan DESC, p.izlenme_sayisi DESC
                LIMIT 10
            """, (*tum_turler, kullanici_id))
            tur_oneriler = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT program_id, program_adi, program_tipi, ortalama_puan, izlenme_sayisi
                FROM Program
                ORDER BY izlenme_sayisi DESC, ortalama_puan DESC
                LIMIT 10
            """)
            tur_oneriler = cursor.fetchall()

        cursor.close()
        conn.close()

        mevcut_idler = {o[0] for o in tur_oneriler}
        for o in benzer_oneriler:
            if o[0] not in mevcut_idler:
                tur_oneriler = list(tur_oneriler) + [o]
                mevcut_idler.add(o[0])

        return tur_oneriler[:10]


class ReportService:
    @staticmethod
    def en_cok_izlenen(limit=10):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT program_id, program_adi, program_tipi, izlenme_sayisi
            FROM Program
            ORDER BY izlenme_sayisi DESC
            LIMIT %s
        """, (limit,))
        sonuc = cursor.fetchall()
        cursor.close()
        conn.close()
        return sonuc

    @staticmethod
    def en_yuksek_puanli(limit=10):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT program_id, program_adi, program_tipi, ortalama_puan
            FROM Program
            ORDER BY ortalama_puan DESC
            LIMIT %s
        """, (limit,))
        sonuc = cursor.fetchall()
        cursor.close()
        conn.close()
        return sonuc

    @staticmethod
    def en_cok_izlenen_turler():
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.tur_adi, SUM(p.izlenme_sayisi) as toplam_izlenme
            FROM Tur t
            JOIN ProgramTur pt ON t.tur_id = pt.tur_id
            JOIN Program p ON pt.program_id = p.program_id
            GROUP BY t.tur_id, t.tur_adi
            ORDER BY toplam_izlenme DESC
            LIMIT 10
        """)
        sonuc = cursor.fetchall()
        cursor.close()
        conn.close()
        return sonuc

    @staticmethod
    def en_aktif_kullanicilar(limit=10):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT k.kullanici_id, k.ad, k.soyad, SUM(i.izleme_suresi) as toplam_sure
            FROM Kullanici k
            JOIN IzlemeLog i ON k.kullanici_id = i.kullanici_id
            GROUP BY k.kullanici_id, k.ad, k.soyad
            ORDER BY toplam_sure DESC
            LIMIT %s
        """, (limit,))
        sonuc = cursor.fetchall()
        cursor.close()
        conn.close()
        return sonuc

    @staticmethod
    def son_7_gun_izlenenler():
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.program_adi, COUNT(*) as izlenme_sayisi
            FROM IzlemeLog i
            JOIN Program p ON i.program_id = p.program_id
            WHERE i.izleme_tarihi >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            GROUP BY p.program_id, p.program_adi
            ORDER BY izlenme_sayisi DESC
            LIMIT 10
        """)
        sonuc = cursor.fetchall()
        cursor.close()
        conn.close()
        return sonuc




class LoginEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filmio - Giriş Yap")
        self.setGeometry(400, 150, 450, 550)
        self.setFixedSize(450, 550)

        layout = QVBoxLayout()
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(15)

        logo = QLabel("🎬 FİLMİO")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignCenter)

        baslik = QLabel("Giriş Yap")
        baslik.setObjectName("baslik")
        baslik.setAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta adresi")

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("Şifre")
        self.sifre_input.setEchoMode(QLineEdit.Password)

        self.giris_btn = QPushButton("Giriş Yap")
        self.giris_btn.clicked.connect(self.giris_yap)
        self.giris_btn.setMinimumHeight(45)

        ayrac = QLabel("─────────── veya ───────────")
        ayrac.setAlignment(Qt.AlignCenter)
        ayrac.setStyleSheet("color: #555555; font-size: 12px;")

        self.kayit_btn = QPushButton("Yeni Hesap Oluştur")
        self.kayit_btn.setObjectName("ikincil")
        self.kayit_btn.clicked.connect(self.kayit_ac)
        self.kayit_btn.setMinimumHeight(45)

        layout.addWidget(logo)
        layout.addSpacing(10)
        layout.addWidget(baslik)
        layout.addSpacing(20)
        layout.addWidget(self.email_input)
        layout.addWidget(self.sifre_input)
        layout.addSpacing(5)
        layout.addWidget(self.giris_btn)
        layout.addWidget(ayrac)
        layout.addWidget(self.kayit_btn)
        layout.addStretch()

        self.setLayout(layout)

    def kayit_ac(self):
        self.kayit = KayitEkrani()
        self.kayit.show()
        self.close()

    def email_gecerli_mi(self, email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    def giris_yap(self):
        email = self.email_input.text().strip()
        sifre = self.sifre_input.text().strip()

        if email == "" or sifre == "":
            QMessageBox.warning(self, "Hata", "Boş alan bırakma")
            return

        if not self.email_gecerli_mi(email):
            QMessageBox.warning(self, "Hata", "Geçerli bir email giriniz.")
            return

        kullanici = AuthService.giris_yap(email, sifre)

        if kullanici:
            if isinstance(kullanici, Admin):
                self.admin = AdminPaneli(kullanici)
                self.admin.show()
                self.close()
            else:
                self.ana = KullaniciAnaSayfa(kullanici)
                self.ana.show()
                self.close()
        else:
            QMessageBox.warning(self, "Hata", "Email veya şifre hatalı, ya da hesabınız pasif.")

class KayitEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filmio - Kayıt Ol")
        self.setGeometry(250, 50, 620, 820)
        self.setMinimumSize(580, 750)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(70, 30, 70, 30)
        layout.setSpacing(10)

        logo = QLabel("🎬 FİLMİO")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignCenter)

        baslik = QLabel("Hesap Oluştur")
        baslik.setObjectName("baslik")
        baslik.setAlignment(Qt.AlignCenter)

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Ad")

        self.soyad_input = QLineEdit()
        self.soyad_input.setPlaceholderText("Soyad")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta adresi")

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("Şifre (min 6 karakter)")
        self.sifre_input.setEchoMode(QLineEdit.Password)

        self.sifre_tekrar_input = QLineEdit()
        self.sifre_tekrar_input.setPlaceholderText("Şifre tekrar")
        self.sifre_tekrar_input.setEchoMode(QLineEdit.Password)

        self.dogum_input = QLineEdit()
        self.dogum_input.setPlaceholderText("Doğum tarihi: YYYY-MM-DD")

        self.cinsiyet_input = QComboBox()
        self.cinsiyet_input.addItems(["Erkek", "Kadın", "Belirtmek istemiyorum"])

        self.ulke_input = QLineEdit()
        self.ulke_input.setPlaceholderText("Ülke")

        self.secim_label = QLabel("Favori Türler — tam 3 tür seçiniz (0/3)")
        self.secim_label.setStyleSheet("color: #AAAAAA; font-size: 12px; margin-top: 6px;")

        tur_frame = QFrame()
        tur_frame.setStyleSheet("""
            QFrame {
                background-color: #1F1F1F;
                border: 1px solid #444444;
                border-radius: 6px;
            }
        """)
        tur_grid = QGridLayout(tur_frame)
        tur_grid.setContentsMargins(12, 12, 12, 12)
        tur_grid.setSpacing(8)

        self.tur_checkboxlar = []
        self._tur_frame = tur_frame
        self._tur_grid = tur_grid
        self.turleri_yukle()

        self.kayit_btn = QPushButton("Kaydı Tamamla")
        self.kayit_btn.clicked.connect(self.kayit_ol)
        self.kayit_btn.setMinimumHeight(45)

        self.giris_btn = QPushButton("Zaten hesabın var mı? Giriş Yap")
        self.giris_btn.setObjectName("ikincil")
        self.giris_btn.clicked.connect(self.girise_don)
        self.giris_btn.setMinimumHeight(40)

        layout.addWidget(logo)
        layout.addWidget(baslik)
        layout.addSpacing(8)
        layout.addWidget(self.ad_input)
        layout.addWidget(self.soyad_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.sifre_input)
        layout.addWidget(self.sifre_tekrar_input)
        layout.addWidget(self.dogum_input)
        layout.addWidget(self.cinsiyet_input)
        layout.addWidget(self.ulke_input)
        layout.addWidget(self.secim_label)
        layout.addWidget(tur_frame)
        layout.addSpacing(8)
        layout.addWidget(self.kayit_btn)
        layout.addWidget(self.giris_btn)

        scroll.setWidget(container)

        outer = QVBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        self.setLayout(outer)

    def turleri_yukle(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("SELECT tur_id, tur_adi FROM Tur ORDER BY tur_adi")
        turler = cursor.fetchall()
        cursor.close()
        conn.close()

        for i, (tur_id, tur_adi) in enumerate(turler):
            cb = QCheckBox(tur_adi)
            cb.setStyleSheet("""
                QCheckBox {
                    color: #FFFFFF;
                    font-size: 13px;
                    spacing: 8px;
                    padding: 4px 6px;
                    background: transparent;
                    border: none;
                }
                QCheckBox:hover { color: #E50914; }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 4px;
                    border: 2px solid #555555;
                    background-color: #2A2A2A;
                }
                QCheckBox::indicator:checked {
                    background-color: #E50914;
                    border: 2px solid #E50914;
                }
                QCheckBox::indicator:hover {
                    border: 2px solid #E50914;
                }
            """)
            cb.stateChanged.connect(self._secim_guncelle)
            self.tur_checkboxlar.append((cb, tur_id))
            self._tur_grid.addWidget(cb, i // 2, i % 2)

    def _secim_guncelle(self):
        secilen = sum(1 for cb, _ in self.tur_checkboxlar if cb.isChecked())
        renk = "#E50914" if secilen == 3 else "#AAAAAA"
        self.secim_label.setText(f"Favori Türler — tam 3 tür seçiniz ({secilen}/3)")
        self.secim_label.setStyleSheet(f"color: {renk}; font-size: 12px; margin-top: 6px;")

        if secilen > 3:
            sender = self.sender()
            if isinstance(sender, QCheckBox) and sender.isChecked():
                sender.setChecked(False)

    def girise_don(self):
        self.login = LoginEkrani()
        self.login.show()
        self.close()

    def email_gecerli_mi(self, email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    def kayit_ol(self):
        ad = self.ad_input.text().strip()
        soyad = self.soyad_input.text().strip()
        email = self.email_input.text().strip()
        sifre = self.sifre_input.text().strip()
        sifre_tekrar = self.sifre_tekrar_input.text().strip()
        dogum_tarihi = self.dogum_input.text().strip()
        cinsiyet = self.cinsiyet_input.currentText()
        ulke = self.ulke_input.text().strip()

        if ad == "" or soyad == "" or email == "" or sifre == "" or sifre_tekrar == "" or dogum_tarihi == "" or ulke == "":
            QMessageBox.warning(self, "Hata", "Boş alan bırakmayınız.")
            return

        if not self.email_gecerli_mi(email):
            QMessageBox.warning(self, "Hata", "Geçerli bir e-mail giriniz.")
            return

        if sifre != sifre_tekrar:
            QMessageBox.warning(self, "Hata", "Şifreler aynı değil.")
            return

        if len(sifre) < 6:
            QMessageBox.warning(self, "Hata", "Şifre en az 6 karakter olmalıdır.")
            return

        try:
            dogum = datetime.strptime(dogum_tarihi, "%Y-%m-%d").date()
            if dogum >= datetime.today().date():
                QMessageBox.warning(self, "Hata", "Doğum tarihi bugünden büyük olamaz.")
                return
        except ValueError:
            QMessageBox.warning(self, "Hata", "Doğum tarihi formatı: YYYY-MM-DD")
            return

        secilen_tur_idler = [tur_id for cb, tur_id in self.tur_checkboxlar if cb.isChecked()]
        if len(secilen_tur_idler) != 3:
            QMessageBox.warning(self, "Hata", "Tam olarak 3 farklı tür seçmelisiniz.")
            return

        try:
            kullanici_id = AuthService.kayit_ol(
                ad, soyad, email, sifre, dogum_tarihi, cinsiyet, ulke, secilen_tur_idler
            )

            if kullanici_id is None:
                QMessageBox.warning(self, "Hata", "Bu e-mail zaten kayıtlı.")
                return

            oneriler = RecommendationService.kayit_sonrasi_oneriler(secilen_tur_idler)

            oneri_metni = "Kayıt başarılı! Seçtiğiniz türlere göre öneriler:\n\n"
            for o in oneriler:
                oneri_metni += f"• {o[1]} ({o[2]}) - Puan: {o[3]}\n"

            QMessageBox.information(self, "Hoş Geldiniz!", oneri_metni)

            self.login = LoginEkrani()
            self.login.show()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Veritabanı Hatası", str(e))

class KullaniciAnaSayfa(QWidget):
    def __init__(self, kullanici):
        super().__init__()
        self.kullanici = kullanici
        self.setWindowTitle("Filmio")
        self.setGeometry(150, 60, 1200, 750)
        self.setMinimumSize(1000, 650)

        ana_layout = QVBoxLayout()
        ana_layout.setContentsMargins(0, 0, 0, 0)
        ana_layout.setSpacing(0)

        navbar = QWidget()
        navbar.setFixedHeight(58)
        navbar.setStyleSheet("background-color: #000000;")
        nav_layout = QHBoxLayout(navbar)
        nav_layout.setContentsMargins(24, 0, 24, 0)
        nav_layout.setSpacing(0)

        logo = QLabel("🎬 FİLMİO")
        logo.setStyleSheet("font-size: 22px; font-weight: bold; color: #E50914; letter-spacing: 2px;")

        nav_layout.addWidget(logo)
        nav_layout.addSpacing(30)

        self.nav_btns = {}
        sekmeler = [
            ("🏠", "Ana Sayfa", 0),
            ("🎬", "İçerikler", 1),
            ("🎯", "Öneriler", 2),
            ("❤️", "Favoriler", 3),
            ("📋", "Geçmiş", 4),
            ("👤", "Profil", 5),
        ]
        for ikon, metin, idx in sekmeler:
            btn = QPushButton(f"{ikon}  {metin}")
            btn.setFixedHeight(58)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #AAAAAA;
                    border: none;
                    border-bottom: 3px solid transparent;
                    font-size: 13px;
                    padding: 0 16px;
                }
                QPushButton:hover { color: #FFFFFF; }
                QPushButton[active=true] {
                    color: #FFFFFF;
                    border-bottom: 3px solid #E50914;
                    font-weight: bold;
                }
            """)
            btn.clicked.connect(lambda checked, i=idx: self.sekme_gec(i))
            nav_layout.addWidget(btn)
            self.nav_btns[idx] = btn

        nav_layout.addStretch()

        kullanici_label = QLabel(f"👤  {kullanici.ad} {kullanici.soyad}")
        kullanici_label.setStyleSheet("color: #CCCCCC; font-size: 12px;")

        cikis_btn = QPushButton("Çıkış")
        cikis_btn.setFixedSize(70, 32)
        cikis_btn.setObjectName("ikincil")
        cikis_btn.clicked.connect(self.cikis_yap)

        nav_layout.addWidget(kullanici_label)
        nav_layout.addSpacing(12)
        nav_layout.addWidget(cikis_btn)

        self.stack = QStackedWidget()

        self.stack.addWidget(self._ana_sayfa_widget())
        self.icerik_sayfasi = IcerikListele(kullanici.kullanici_id)
        self.stack.addWidget(self.icerik_sayfasi)
        self.oneri_sayfasi = OneriSayfasi(kullanici.kullanici_id)
        self.stack.addWidget(self.oneri_sayfasi)
        self.favori_sayfasi = FavorilerSayfasi(kullanici.kullanici_id)
        self.stack.addWidget(self.favori_sayfasi)
        self.gecmis_sayfasi = IzlemeGecmisiSayfasi(kullanici.kullanici_id)
        self.stack.addWidget(self.gecmis_sayfasi)
        self.profil_sayfasi = ProfilSayfasi(kullanici)
        self.stack.addWidget(self.profil_sayfasi)

        ana_layout.addWidget(navbar)
        ana_layout.addWidget(self.stack)
        self.setLayout(ana_layout)

        self.sekme_gec(0)

    def _ana_sayfa_widget(self):
        """Ana sayfa hoş geldin ekranı"""
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        hosgeldin = QLabel(f"Hoş geldiniz, {self.kullanici.ad}! 👋")
        hosgeldin.setStyleSheet("font-size: 26px; font-weight: bold; color: #FFFFFF;")

        alt = QLabel("Ne izlemek istersiniz?")
        alt.setStyleSheet("font-size: 15px; color: #AAAAAA;")

        layout.addWidget(hosgeldin)
        layout.addWidget(alt)
        layout.addSpacing(20)

        kart_layout = QHBoxLayout()
        kart_layout.setSpacing(20)

        kartlar = [
            ("🎬", "Tüm İçerikler", "Film, dizi ve TV showları keşfet", 1),
            ("🎯", "Önerilen İçerikler", "Sana özel seçkiler", 2),
            ("❤️", "Favorilerim", "Kaydettiğin içerikler", 3),
            ("📋", "İzleme Geçmişi", "Daha önce izlediklerin", 4),
            ("👤", "Profilim", "Hesap bilgilerin", 5),
        ]

        for ikon, baslik, aciklama, idx in kartlar:
            kart = QFrame()
            kart.setFixedSize(190, 150)
            kart.setCursor(Qt.PointingHandCursor)
            kart.setStyleSheet("""
                QFrame {
                    background-color: #1F1F1F;
                    border-radius: 10px;
                    border: 1px solid #2A2A2A;
                }
                QFrame:hover { border: 2px solid #E50914; }
            """)
            kl = QVBoxLayout(kart)
            kl.setContentsMargins(16, 16, 16, 16)

            ikon_lbl = QLabel(ikon)
            ikon_lbl.setStyleSheet("font-size: 32px; background: transparent; border: none;")
            baslik_lbl = QLabel(baslik)
            baslik_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #FFFFFF; background: transparent; border: none;")
            baslik_lbl.setWordWrap(True)
            aciklama_lbl = QLabel(aciklama)
            aciklama_lbl.setStyleSheet("font-size: 11px; color: #888888; background: transparent; border: none;")
            aciklama_lbl.setWordWrap(True)

            kl.addWidget(ikon_lbl)
            kl.addWidget(baslik_lbl)
            kl.addWidget(aciklama_lbl)
            kl.addStretch()

            kart.mousePressEvent = lambda e, i=idx: self.sekme_gec(i)
            kart_layout.addWidget(kart)

        layout.addLayout(kart_layout)
        layout.addStretch()
        return w

    def sekme_gec(self, idx):
        if idx == 3:
            self.favori_sayfasi.favorileri_getir()
        elif idx == 4:
            self.gecmis_sayfasi.gecmisi_getir()

        self.stack.setCurrentIndex(idx)

        for i, btn in self.nav_btns.items():
            btn.setProperty("active", i == idx)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def cikis_yap(self):
        self.login = LoginEkrani()
        self.login.show()
        self.close()


class OneriSayfasi(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.setWindowTitle("Önerilen İçerikler")
        self.setGeometry(200, 100, 1000, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        baslik = QLabel("🎯  Sizin İçin Önerilen İçerikler")
        baslik.setObjectName("alt_baslik")
        layout.addWidget(baslik)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(15)

        scroll.setWidget(self.grid_widget)
        layout.addWidget(scroll)
        self.setLayout(layout)
        self.onerileri_getir()

    def onerileri_getir(self):
        oneriler = RecommendationService.kullanici_onerileri(self.kullanici_id)
        for i, o in enumerate(oneriler):
            kart = IcerikKarti(o[0], o[1], o[2], o[3], o[4], self.kullanici_id)
            self.grid_layout.addWidget(kart, i // 4, i % 4)


class IcerikKarti(QFrame):
    """Netflix tarzı içerik kartı"""
    TIP_RENK = {"Film": "#E50914", "Dizi": "#0080FF", "Tv Show": "#00A550"}

    def __init__(self, program_id, ad, tip, puan, izlenme, kullanici_id):
        super().__init__()
        self.program_id = program_id
        self.kullanici_id = kullanici_id
        self.ad = ad
        self.tip = tip

        self.setFixedSize(210, 260)
        self.setCursor(Qt.PointingHandCursor)

        renk = self.TIP_RENK.get(tip, "#555555")

        self.setStyleSheet(f"""
            IcerikKarti {{
                background-color: #1F1F1F;
                border-radius: 8px;
                border: 1px solid #2A2A2A;
            }}
            IcerikKarti:hover {{
                border: 2px solid #E50914;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(6)

        banner = QLabel()
        banner.setFixedHeight(120)
        banner.setAlignment(Qt.AlignCenter)
        banner.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {renk}, stop:1
            border-radius: 8px 8px 0 0;
            font-size: 36px;
        """)
        emoji = {"Film": "🎬", "Dizi": "📺", "Tv Show": "🎙️"}.get(tip, "🎞️")
        banner.setText(emoji)

        tip_label = QLabel(tip)
        tip_label.setAlignment(Qt.AlignCenter)
        tip_label.setFixedHeight(22)
        tip_label.setStyleSheet(f"""
            background-color: {renk};
            color: white;
            font-size: 11px;
            font-weight: bold;
            border-radius: 3px;
            padding: 2px 8px;
        """)

        ad_label = QLabel(ad)
        ad_label.setWordWrap(True)
        ad_label.setAlignment(Qt.AlignCenter)
        ad_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #FFFFFF; padding: 0 8px;")
        ad_label.setMaximumHeight(40)

        bilgi_layout = QHBoxLayout()
        bilgi_layout.setContentsMargins(8, 0, 8, 0)

        puan_label = QLabel(f"⭐ {puan}")
        puan_label.setStyleSheet("color: #FFD700; font-size: 11px;")

        izlenme_label = QLabel(f"👁 {izlenme:,}")
        izlenme_label.setStyleSheet("color: #AAAAAA; font-size: 11px;")

        bilgi_layout.addWidget(puan_label)
        bilgi_layout.addStretch()
        bilgi_layout.addWidget(izlenme_label)

        detay_btn = QPushButton("Detay")
        detay_btn.setFixedHeight(28)
        detay_btn.setStyleSheet("""
            QPushButton {
                background-color: #E50914;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
                margin: 0 8px;
            }
            QPushButton:hover { background-color: #F40612; }
        """)
        detay_btn.clicked.connect(self.detay_ac)

        layout.addWidget(banner)
        layout.addWidget(tip_label)
        layout.addWidget(ad_label)
        layout.addLayout(bilgi_layout)
        layout.addWidget(detay_btn)

    def detay_ac(self):
        self.detay = IcerikDetaySayfasi(self.kullanici_id, self.program_id)
        self.detay.show()

    def mouseDoubleClickEvent(self, event):
        self.detay_ac()


class IcerikListele(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.setWindowTitle("İçerikler")
        self.setGeometry(150, 80, 1100, 700)
        self.setMinimumSize(900, 600)

        ana_layout = QVBoxLayout()
        ana_layout.setContentsMargins(20, 15, 20, 15)
        ana_layout.setSpacing(12)

        baslik = QLabel("🎬  Tüm İçerikler")
        baslik.setObjectName("alt_baslik")
        ana_layout.addWidget(baslik)

        filtre_frame = QFrame()
        filtre_frame.setStyleSheet("QFrame { background-color: #1F1F1F; border-radius: 8px; padding: 4px; }")
        filtre_layout = QHBoxLayout(filtre_frame)
        filtre_layout.setSpacing(8)

        self.arama_input = QLineEdit()
        self.arama_input.setPlaceholderText("🔍  Program adı ara...")
        self.arama_input.returnPressed.connect(self.filtrele)

        self.tur_combo = QComboBox()
        self.tur_combo.addItem("Tüm Türler")
        self.turleri_yukle()

        self.tip_combo = QComboBox()
        self.tip_combo.addItems(["Hepsi", "Film", "Dizi", "Tv Show"])

        self.yil_input = QLineEdit()
        self.yil_input.setPlaceholderText("Min yıl")
        self.yil_input.setMaximumWidth(80)

        self.puan_input = QLineEdit()
        self.puan_input.setPlaceholderText("Min puan")
        self.puan_input.setMaximumWidth(80)

        self.siralama_combo = QComboBox()
        self.siralama_combo.addItems(["Varsayılan", "En Çok İzlenen", "En Yüksek Puan"])

        self.ara_btn = QPushButton("Filtrele")
        self.ara_btn.setFixedWidth(90)
        self.ara_btn.clicked.connect(self.filtrele)

        filtre_layout.addWidget(self.arama_input, 3)
        filtre_layout.addWidget(self.tur_combo, 2)
        filtre_layout.addWidget(self.tip_combo, 1)
        filtre_layout.addWidget(self.yil_input)
        filtre_layout.addWidget(self.puan_input)
        filtre_layout.addWidget(self.siralama_combo, 1)
        filtre_layout.addWidget(self.ara_btn)

        ana_layout.addWidget(filtre_frame)

        self.sonuc_label = QLabel("")
        self.sonuc_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        ana_layout.addWidget(self.sonuc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #141414; }")

        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background-color: #141414;")
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll.setWidget(self.grid_widget)
        ana_layout.addWidget(scroll)

        self.setLayout(ana_layout)
        self.program_id = None
        self.verileri_getir()
        self.program_id = None
        self.verileri_getir()

    def turleri_yukle(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("SELECT tur_id, tur_adi FROM Tur ORDER BY tur_adi")
        for row in cursor.fetchall():
            self.tur_combo.addItem(row[1], row[0])
        cursor.close()
        conn.close()

    def _grid_temizle(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _kartlari_goster(self, rows):
        self._grid_temizle()
        self.sonuc_label.setText(f"{len(rows)} içerik bulundu")
        sutun_sayisi = 5
        for i, row in enumerate(rows):
            kart = IcerikKarti(row[0], row[1], row[2], row[5], row[6], self.kullanici_id)
            self.grid_layout.addWidget(kart, i // sutun_sayisi, i % sutun_sayisi)

    def verileri_getir(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.program_id, p.program_adi, p.program_tipi,
                   p.bolum_sayisi, p.program_uzunlugu, p.ortalama_puan,
                   p.izlenme_sayisi,
                   GROUP_CONCAT(t.tur_adi SEPARATOR ', ') AS turler
            FROM Program p
            LEFT JOIN ProgramTur pt ON p.program_id = pt.program_id
            LEFT JOIN Tur t ON pt.tur_id = t.tur_id
            GROUP BY p.program_id, p.program_adi, p.program_tipi,
                     p.bolum_sayisi, p.program_uzunlugu, p.ortalama_puan, p.izlenme_sayisi
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        self._kartlari_goster(rows)

    def secildi(self, item):
        pass

    def detay_ac(self):
        pass

    def favori_toggle(self):
        pass

    def filtrele(self):
        arama = self.arama_input.text().strip()
        tip = self.tip_combo.currentText()
        tur_idx = self.tur_combo.currentIndex()
        tur_id = self.tur_combo.itemData(tur_idx) if tur_idx > 0 else None
        min_yil = self.yil_input.text().strip()
        min_puan = self.puan_input.text().strip()
        siralama = self.siralama_combo.currentText()

        conn = baglanti_olustur()
        cursor = conn.cursor()

        query = """
            SELECT p.program_id, p.program_adi, p.program_tipi,
                   p.bolum_sayisi, p.program_uzunlugu, p.ortalama_puan,
                   p.izlenme_sayisi,
                   GROUP_CONCAT(t.tur_adi SEPARATOR ', ') AS turler
            FROM Program p
            LEFT JOIN ProgramTur pt ON p.program_id = pt.program_id
            LEFT JOIN Tur t ON pt.tur_id = t.tur_id
            WHERE 1=1
        """
        params = []

        if arama:
            query += " AND p.program_adi LIKE %s"
            params.append(f"%{arama}%")
        if tip != "Hepsi":
            query += " AND p.program_tipi = %s"
            params.append(tip)
        if tur_id:
            query += " AND p.program_id IN (SELECT program_id FROM ProgramTur WHERE tur_id=%s)"
            params.append(tur_id)
        if min_yil.isdigit():
            query += " AND p.yayin_yili >= %s"
            params.append(int(min_yil))
        if min_puan:
            try:
                query += " AND p.ortalama_puan >= %s"
                params.append(float(min_puan))
            except ValueError:
                pass

        query += " GROUP BY p.program_id, p.program_adi, p.program_tipi, p.bolum_sayisi, p.program_uzunlugu, p.ortalama_puan, p.izlenme_sayisi"

        if siralama == "En Çok İzlenen":
            query += " ORDER BY p.izlenme_sayisi DESC"
        elif siralama == "En Yüksek Puan":
            query += " ORDER BY p.ortalama_puan DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        self._kartlari_goster(rows)


class FavorilerSayfasi(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.setWindowTitle("Favorilerim")
        self.setGeometry(200, 100, 1000, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        baslik = QLabel("❤️  Favori İçeriklerim")
        baslik.setObjectName("alt_baslik")

        filtre_layout = QHBoxLayout()
        self.tur_combo = QComboBox()
        self.tur_combo.addItem("Tüm Türler")
        self.turleri_getir()
        self.tur_combo.currentIndexChanged.connect(self.favorileri_getir)

        filtre_layout.addWidget(QLabel("Türe göre filtrele:"))
        filtre_layout.addWidget(self.tur_combo)
        filtre_layout.addStretch()

        self.sonuc_label = QLabel("")
        self.sonuc_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #141414; }")

        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background-color: #141414;")
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll.setWidget(self.grid_widget)

        layout.addWidget(baslik)
        layout.addLayout(filtre_layout)
        layout.addWidget(self.sonuc_label)
        layout.addWidget(scroll)
        self.setLayout(layout)
        self.favorileri_getir()

    def turleri_getir(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("SELECT tur_adi FROM Tur ORDER BY tur_adi")
        for row in cursor.fetchall():
            self.tur_combo.addItem(row[0])
        cursor.close()
        conn.close()

    def _grid_temizle(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def favorileri_getir(self):
        secilen_tur = self.tur_combo.currentText()
        conn = baglanti_olustur()
        cursor = conn.cursor()

        query = """
            SELECT p.program_id, p.program_adi, p.program_tipi,
                   p.bolum_sayisi, p.program_uzunlugu, p.ortalama_puan, p.izlenme_sayisi
            FROM Favori f
            INNER JOIN Program p ON f.program_id = p.program_id
            WHERE f.kullanici_id=%s
        """
        params = [self.kullanici_id]

        if secilen_tur != "Tüm Türler":
            query += " AND p.program_id IN (SELECT pt2.program_id FROM ProgramTur pt2 INNER JOIN Tur t2 ON pt2.tur_id = t2.tur_id WHERE t2.tur_adi=%s)"
            params.append(secilen_tur)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        self._grid_temizle()
        self.sonuc_label.setText(f"{len(rows)} favori içerik")

        sutun_sayisi = 5
        for i, row in enumerate(rows):
            kart = FavoriKarti(row[0], row[1], row[2], row[5], row[6], self.kullanici_id, self)
            self.grid_layout.addWidget(kart, i // sutun_sayisi, i % sutun_sayisi)

    def favoriden_cikar(self, program_id):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Favori WHERE kullanici_id=%s AND program_id=%s",
                      (self.kullanici_id, program_id))
        conn.commit()
        cursor.close()
        conn.close()
        self.favorileri_getir()


class FavoriKarti(IcerikKarti):
    """Favorilerden çıkar butonu olan kart"""
    def __init__(self, program_id, ad, tip, puan, izlenme, kullanici_id, favori_sayfa):
        super().__init__(program_id, ad, tip, puan, izlenme, kullanici_id)
        self.favori_sayfa = favori_sayfa

        cikar_btn = QPushButton("❌ Favoriden Çıkar")
        cikar_btn.setFixedHeight(26)
        cikar_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #AAAAAA;
                border: none;
                border-radius: 4px;
                font-size: 10px;
                margin: 0 8px;
            }
            QPushButton:hover { background-color: #E50914; color: white; }
        """)
        cikar_btn.clicked.connect(lambda: self.favori_sayfa.favoriden_cikar(self.program_id))
        self.layout().addWidget(cikar_btn)

class IzlemeGecmisiSayfasi(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()

        self.kullanici_id = kullanici_id

        self.setWindowTitle("İzleme Geçmişim")
        self.setGeometry(400, 250, 800, 400)

        layout = QVBoxLayout()

        self.liste = QListWidget()

        layout.addWidget(QLabel("İzleme Geçmişim"))
        layout.addWidget(self.liste)

        self.setLayout(layout)

        self.gecmisi_getir()

    def gecmisi_getir(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.program_adi,
                i.izleme_tarihi,
                i.bolum_no,
                i.izleme_suresi,
                i.verilen_puan,
                i.tamamlandi_mi
            FROM IzlemeLog i
            INNER JOIN Program p ON i.program_id = p.program_id
            WHERE i.kullanici_id=%s
            ORDER BY i.izleme_tarihi DESC
        """, (self.kullanici_id,))

        self.liste.clear()

        for row in cursor.fetchall():
            tamamlandi = "Evet" if row[5] else "Hayır"

            yazi = (
                f"İçerik: {row[0]} | "
                f"Tarih: {row[1]} | "
                f"Bölüm: {row[2]} | "
                f"Süre: {row[3]} dk | "
                f"Puan: {row[4]} | "
                f"Tamamlandı mı: {tamamlandi}"
            )

            self.liste.addItem(yazi)

        cursor.close()
        conn.close()

class ProfilSayfasi(QWidget):
    def __init__(self, kullanici):
        super().__init__()

        self.kullanici = kullanici

        self.setWindowTitle("Profilim")
        self.setGeometry(450, 250, 500, 550)

        layout = QVBoxLayout()

        self.bilgi_text = QTextEdit()
        self.bilgi_text.setReadOnly(True)

        layout.addWidget(QLabel("Profil Bilgileri"))
        layout.addWidget(self.bilgi_text)

        layout.addWidget(QLabel("--- Profil Güncelle ---"))

        self.yeni_ad = QLineEdit()
        self.yeni_ad.setPlaceholderText("Yeni ad (boş bırakılırsa değişmez)")

        self.yeni_soyad = QLineEdit()
        self.yeni_soyad.setPlaceholderText("Yeni soyad")

        self.yeni_ulke = QLineEdit()
        self.yeni_ulke.setPlaceholderText("Yeni ülke")

        self.yeni_sifre = QLineEdit()
        self.yeni_sifre.setPlaceholderText("Yeni şifre (min 6 karakter)")
        self.yeni_sifre.setEchoMode(QLineEdit.Password)

        self.guncelle_btn = QPushButton("Güncelle")
        self.guncelle_btn.clicked.connect(self.guncelle)

        layout.addWidget(self.yeni_ad)
        layout.addWidget(self.yeni_soyad)
        layout.addWidget(self.yeni_ulke)
        layout.addWidget(self.yeni_sifre)
        layout.addWidget(self.guncelle_btn)

        self.setLayout(layout)

        self.profil_getir()

    def profil_getir(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ad, soyad, email, dogum_tarihi, ulke
            FROM Kullanici
            WHERE kullanici_id=%s
        """, (self.kullanici.kullanici_id,))

        kullanici = cursor.fetchone()

        cursor.execute("""
            SELECT
                COALESCE(SUM(izleme_suresi), 0),
                COUNT(DISTINCT program_id),
                COALESCE(AVG(verilen_puan), 0)
            FROM IzlemeLog
            WHERE kullanici_id=%s
        """, (self.kullanici.kullanici_id,))

        istatistik = cursor.fetchone()

        cursor.execute("""
            SELECT t.tur_adi FROM KullaniciTur kt
            JOIN Tur t ON kt.tur_id = t.tur_id
            WHERE kt.kullanici_id=%s
        """, (self.kullanici.kullanici_id,))

        favori_turler = [row[0] for row in cursor.fetchall()]

        if kullanici:
            ad, soyad, email, dogum_tarihi, ulke = kullanici
            toplam_sure, izlenen_sayi, ort_puan = istatistik

            yazi = f"""Ad: {ad}
Soyad: {soyad}
E-mail: {email}
Doğum Tarihi: {dogum_tarihi}
Ülke: {ulke}
Favori Türler: {', '.join(favori_turler) if favori_turler else 'Belirtilmemiş'}

Toplam İzleme Süresi: {toplam_sure} dk
İzlenen İçerik Sayısı: {izlenen_sayi}
Verilen Ortalama Puan: {round(ort_puan, 2)}
"""
            self.bilgi_text.setText(yazi)

        cursor.close()
        conn.close()

    def guncelle(self):
        yeni_ad = self.yeni_ad.text().strip() or None
        yeni_soyad = self.yeni_soyad.text().strip() or None
        yeni_ulke = self.yeni_ulke.text().strip() or None
        yeni_sifre = self.yeni_sifre.text().strip() or None

        if yeni_sifre and len(yeni_sifre) < 6:
            QMessageBox.warning(self, "Hata", "Şifre en az 6 karakter olmalıdır.")
            return

        self.kullanici.profil_guncelle(yeni_ad, yeni_soyad, yeni_ulke, yeni_sifre)
        QMessageBox.information(self, "Başarılı", "Profil güncellendi.")
        self.profil_getir()

class IcerikDetaySayfasi(QWidget):
    ADMIN_EMAIL = "230501020@kocaelisaglik.edu.tr"

    def __init__(self, kullanici_id, program_id):
        super().__init__()

        self.kullanici_id = kullanici_id
        self.program_id = program_id
        self._is_admin = self._admin_mi_kontrol()

        self.setWindowTitle("İçerik Detay")
        self.setGeometry(400, 200, 500, 500)

        layout = QVBoxLayout()

        self.baslik = QLabel()
        self.detay_text = QTextEdit()
        self.detay_text.setReadOnly(True)

        self.izle_btn = QPushButton("İzle")
        self.izle_btn.clicked.connect(self.izle_ac)

        self.favori_btn = QPushButton("Favoriye Ekle / Çıkar")
        self.favori_btn.clicked.connect(self.favori_toggle)

        self.puan_input = QSpinBox()
        self.puan_input.setMinimum(1)
        self.puan_input.setMaximum(10)

        self.puan_btn = QPushButton("Puan Ver")
        self.puan_btn.clicked.connect(self.puan_ver)

        layout.addWidget(self.baslik)
        layout.addWidget(self.detay_text)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.izle_btn)
        btn_layout.addWidget(self.favori_btn)

        # Admin düzenleme butonu — sadece yetkili hesap için göster
        if self._is_admin:
            self.duzenle_btn = QPushButton("✏️ İçeriği Düzenle")
            self.duzenle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F5A623;
                    color: #000000;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #E09010; }
            """)
            self.duzenle_btn.clicked.connect(self.icerik_duzenle)
            btn_layout.addWidget(self.duzenle_btn)

        layout.addLayout(btn_layout)

        puan_layout = QHBoxLayout()
        puan_layout.addWidget(QLabel("Puan (1-10):"))
        puan_layout.addWidget(self.puan_input)
        puan_layout.addWidget(self.puan_btn)
        layout.addLayout(puan_layout)

        self.setLayout(layout)

        self.detay_getir()

    def _admin_mi_kontrol(self):
        """Giriş yapan kullanıcının admin emailine sahip olup olmadığını kontrol et"""
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM Kullanici WHERE kullanici_id=%s", (self.kullanici_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row is not None and row[0] == self.ADMIN_EMAIL

    def icerik_duzenle(self):
        """Admin için içerik düzenleme penceresini aç"""
        self.duzenle_pencere = AdminIcerikDuzenle(self.program_id, self)
        self.duzenle_pencere.show()

    def detay_getir(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.program_adi,
                p.aciklama,
                p.program_tipi,
                p.bolum_sayisi,
                p.program_uzunlugu,
                p.yayin_yili,
                p.ortalama_puan,
                p.izlenme_sayisi,
                GROUP_CONCAT(t.tur_adi SEPARATOR ', ') AS turler
            FROM Program p
            LEFT JOIN ProgramTur pt ON p.program_id = pt.program_id
            LEFT JOIN Tur t ON pt.tur_id = t.tur_id
            WHERE p.program_id = %s
            GROUP BY
                p.program_id, p.program_adi, p.aciklama, p.program_tipi,
                p.bolum_sayisi, p.program_uzunlugu, p.yayin_yili,
                p.ortalama_puan, p.izlenme_sayisi
        """, (self.program_id,))

        row = cursor.fetchone()

        if row:
            program_adi = row[0]
            aciklama = row[1] or ""
            program_tipi = row[2]
            bolum_sayisi = row[3]
            program_uzunlugu = row[4]
            yayin_yili = row[5]
            ortalama_puan = row[6]
            izlenme_sayisi = row[7]
            turler = row[8]

            self.program_adi = program_adi
            self.program_tipi = program_tipi
            self.bolum_sayisi = bolum_sayisi
            self.program_uzunlugu = program_uzunlugu

            self.baslik.setText(program_adi)

            cursor.execute("""
                SELECT verilen_puan, tamamlandi_mi, izlenen_bolum, kalinan_sure
                FROM KullaniciProgram
                WHERE kullanici_id=%s AND program_id=%s
            """, (self.kullanici_id, self.program_id))
            puan_row = cursor.fetchone()
            kullanici_puani = puan_row[0] if puan_row and puan_row[0] else "Henüz puanlanmadı"
            izleme_durumu = "Hayır"
            if puan_row:
                if puan_row[1]:
                    izleme_durumu = "Evet (Tamamlandı)"
                else:
                    izleme_durumu = f"Evet (Bölüm {puan_row[2]}, {puan_row[3]} dk'da kaldı)"

            cursor.execute("SELECT 1 FROM Favori WHERE kullanici_id=%s AND program_id=%s",
                          (self.kullanici_id, self.program_id))
            favori_durumu = "Evet" if cursor.fetchone() else "Hayır"

            bilgi = f"""Program Adı: {program_adi}
Açıklama: {aciklama}
Program Tipi: {program_tipi}
Türler: {turler}
Bölüm Sayısı: {bolum_sayisi}
Bölüm / Program Uzunluğu: {program_uzunlugu} dk
Yayın Yılı: {yayin_yili}
Ortalama Puan: {ortalama_puan}
Toplam İzlenme Sayısı: {izlenme_sayisi}
Daha Önce İzlendi mi: {izleme_durumu}
Kullanıcı Puanı: {kullanici_puani}
Favorilerde: {favori_durumu}
"""
            self.detay_text.setText(bilgi)

        cursor.close()
        conn.close()

    def favori_toggle(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Favori WHERE kullanici_id=%s AND program_id=%s",
                      (self.kullanici_id, self.program_id))
        if cursor.fetchone():
            cursor.execute("DELETE FROM Favori WHERE kullanici_id=%s AND program_id=%s",
                          (self.kullanici_id, self.program_id))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Favorilerden çıkarıldı.")
        else:
            cursor.execute("INSERT INTO Favori (kullanici_id, program_id) VALUES (%s, %s)",
                          (self.kullanici_id, self.program_id))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Favorilere eklendi.")
        cursor.close()
        conn.close()
        self.detay_getir()

    def puan_ver(self):
        """Sadece izlenmiş içerik puanlanabilir"""
        puan = self.puan_input.value()
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("SELECT kullanici_program_id FROM KullaniciProgram WHERE kullanici_id=%s AND program_id=%s",
                      (self.kullanici_id, self.program_id))
        kayit = cursor.fetchone()

        if not kayit:
            QMessageBox.warning(self, "Hata", "Sadece izlediğiniz içerikleri puanlayabilirsiniz.")
            cursor.close()
            conn.close()
            return

        cursor.execute("""
            UPDATE KullaniciProgram SET verilen_puan=%s
            WHERE kullanici_id=%s AND program_id=%s
        """, (puan, self.kullanici_id, self.program_id))

        cursor.execute("""
            UPDATE Program
            SET ortalama_puan = (
                SELECT AVG(verilen_puan)
                FROM KullaniciProgram
                WHERE program_id = %s AND verilen_puan IS NOT NULL
            )
            WHERE program_id = %s
        """, (self.program_id, self.program_id))

        conn.commit()
        cursor.close()
        conn.close()

        QMessageBox.information(self, "Başarılı", f"Puanınız ({puan}) kaydedildi.")
        self.detay_getir()

    def izle_ac(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT izlenen_bolum, kalinan_sure, tamamlandi_mi
            FROM KullaniciProgram
            WHERE kullanici_id=%s AND program_id=%s
        """, (self.kullanici_id, self.program_id))

        kayit = cursor.fetchone()

        baslangic_bolum = 1
        baslangic_sure = 0

        if kayit:
            izlenen_bolum, kalinan_sure, tamamlandi_mi = kayit

            if not tamamlandi_mi:
                cevap = QMessageBox.question(
                    self,
                    "Kaldığın Yerden Devam Et",
                    f"{izlenen_bolum}. bölüm {kalinan_sure}. dakikadan devam etmek ister misin?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if cevap == QMessageBox.Yes:
                    baslangic_bolum = izlenen_bolum
                    baslangic_sure = kalinan_sure

        cursor.close()
        conn.close()

        self.izleme = IzlemeEkrani(
            self.kullanici_id,
            self.program_id,
            self.program_adi,
            self.program_tipi,
            self.bolum_sayisi,
            self.program_uzunlugu,
            baslangic_bolum,
            baslangic_sure
        )
        self.izleme.show()


class AdminIcerikDuzenle(QWidget):
    """Admin için içerik detay düzenleme penceresi"""
    def __init__(self, program_id, detay_sayfasi=None):
        super().__init__()
        self.program_id = program_id
        self.detay_sayfasi = detay_sayfasi

        self.setWindowTitle("İçerik Düzenle (Admin)")
        self.setGeometry(450, 200, 480, 480)
        self.setFixedSize(480, 480)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        baslik = QLabel("✏️  İçerik Düzenle")
        baslik.setObjectName("alt_baslik")
        layout.addWidget(baslik)

        self.adi_input = QLineEdit()
        self.adi_input.setPlaceholderText("Program adı")

        self.aciklama_input = QTextEdit()
        self.aciklama_input.setPlaceholderText("Açıklama")
        self.aciklama_input.setMaximumHeight(80)

        self.tip_combo = QComboBox()
        self.tip_combo.addItems(["Film", "Dizi", "Tv Show"])

        self.bolum_input = QSpinBox()
        self.bolum_input.setMinimum(1)
        self.bolum_input.setMaximum(500)

        self.uzunluk_input = QSpinBox()
        self.uzunluk_input.setMinimum(1)
        self.uzunluk_input.setMaximum(500)

        self.yil_input = QSpinBox()
        self.yil_input.setMinimum(1900)
        self.yil_input.setMaximum(2100)

        layout.addWidget(QLabel("Program Adı:"))
        layout.addWidget(self.adi_input)
        layout.addWidget(QLabel("Açıklama:"))
        layout.addWidget(self.aciklama_input)
        layout.addWidget(QLabel("Tip:"))
        layout.addWidget(self.tip_combo)
        layout.addWidget(QLabel("Bölüm Sayısı:"))
        layout.addWidget(self.bolum_input)
        layout.addWidget(QLabel("Uzunluk (dk):"))
        layout.addWidget(self.uzunluk_input)
        layout.addWidget(QLabel("Yayın Yılı:"))
        layout.addWidget(self.yil_input)

        btn_layout = QHBoxLayout()
        kaydet_btn = QPushButton("💾 Kaydet")
        kaydet_btn.clicked.connect(self.kaydet)
        iptal_btn = QPushButton("İptal")
        iptal_btn.setObjectName("ikincil")
        iptal_btn.clicked.connect(self.close)
        btn_layout.addWidget(kaydet_btn)
        btn_layout.addWidget(iptal_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.mevcut_verileri_yukle()

    def mevcut_verileri_yukle(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT program_adi, aciklama, program_tipi, bolum_sayisi, program_uzunlugu, yayin_yili
            FROM Program WHERE program_id=%s
        """, (self.program_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            self.adi_input.setText(row[0] or "")
            self.aciklama_input.setPlainText(row[1] or "")
            idx = self.tip_combo.findText(row[2])
            if idx >= 0:
                self.tip_combo.setCurrentIndex(idx)
            self.bolum_input.setValue(row[3] or 1)
            self.uzunluk_input.setValue(row[4] or 1)
            self.yil_input.setValue(row[5] or 2024)

    def kaydet(self):
        adi = self.adi_input.text().strip()
        if not adi:
            QMessageBox.warning(self, "Hata", "Program adı boş olamaz.")
            return

        aciklama = self.aciklama_input.toPlainText().strip()
        tip = self.tip_combo.currentText()
        bolum = self.bolum_input.value()
        uzunluk = self.uzunluk_input.value()
        yil = self.yil_input.value()

        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Program
            SET program_adi=%s, aciklama=%s, program_tipi=%s,
                bolum_sayisi=%s, program_uzunlugu=%s, yayin_yili=%s
            WHERE program_id=%s
        """, (adi, aciklama, tip, bolum, uzunluk, yil, self.program_id))
        conn.commit()
        cursor.close()
        conn.close()

        QMessageBox.information(self, "Başarılı", "İçerik güncellendi.")

        # Detay sayfasını yenile
        if self.detay_sayfasi:
            self.detay_sayfasi.detay_getir()

        self.close()


class IzlemeEkrani(QWidget):
    def __init__(self, kullanici_id, program_id, program_adi, program_tipi, bolum_sayisi, program_uzunlugu, baslangic_bolum=1, baslangic_sure=0):
        super().__init__()

        self.kullanici_id = kullanici_id
        self.program_id = program_id
        self.program_adi = program_adi
        self.program_tipi = program_tipi
        self.bolum_sayisi = bolum_sayisi
        self.program_uzunlugu = program_uzunlugu

        self.setWindowTitle("İzleme Ekranı")
        self.setGeometry(450, 250, 400, 350)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"İçerik: {self.program_adi}"))
        layout.addWidget(QLabel(f"Tip: {self.program_tipi}"))

        self.bolum_input = QSpinBox()
        self.bolum_input.setMinimum(1)
        self.bolum_input.setMaximum(self.bolum_sayisi)

        self.sure_input = QSpinBox()
        self.sure_input.setMinimum(0)
        self.sure_input.setMaximum(self.program_uzunlugu)

        self.puan_input = QSpinBox()
        self.puan_input.setMinimum(1)
        self.puan_input.setMaximum(10)

        self.kaydet_btn = QPushButton("Kaldığım Yere Kaydet")
        self.kaydet_btn.clicked.connect(self.kaldigim_yere_kaydet)

        self.tamamla_btn = QPushButton("İzlemeyi Tamamla")
        self.tamamla_btn.clicked.connect(self.izlemeyi_tamamla)

        layout.addWidget(QLabel("Bölüm No:"))
        layout.addWidget(self.bolum_input)

        layout.addWidget(QLabel("Kaldığın Süre / İzleme Süresi:"))
        layout.addWidget(self.sure_input)

        layout.addWidget(QLabel("Puan:"))
        layout.addWidget(self.puan_input)

        layout.addWidget(self.kaydet_btn)
        layout.addWidget(self.tamamla_btn)

        self.bolum_input.setValue(baslangic_bolum)
        self.sure_input.setValue(baslangic_sure)

        self.setLayout(layout)

    def kaldigim_yere_kaydet(self):
        bolum_no = self.bolum_input.value()
        sure = self.sure_input.value()
        puan = self.puan_input.value()

        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT kullanici_program_id FROM KullaniciProgram
            WHERE kullanici_id=%s AND program_id=%s
        """, (self.kullanici_id, self.program_id))

        eski_kayit = cursor.fetchone()

        if eski_kayit:
            cursor.execute("""
                UPDATE KullaniciProgram
                SET izlenen_bolum=%s,
                    kalinan_sure=%s,
                    tamamlandi_mi=%s,
                    verilen_puan=%s
                WHERE kullanici_id=%s AND program_id=%s
            """, (
                bolum_no,
                sure,
                False,
                puan,
                self.kullanici_id,
                self.program_id
            ))
        else:
            cursor.execute("""
                INSERT INTO KullaniciProgram
                (kullanici_id, program_id, izlenen_bolum, kalinan_sure, tamamlandi_mi, verilen_puan)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                self.kullanici_id,
                self.program_id,
                bolum_no,
                sure,
                    False,
                puan
            ))

        cursor.execute("""
            INSERT INTO IzlemeLog
            (kullanici_id, program_id, bolum_no, izleme_suresi, verilen_puan, tamamlandi_mi)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            self.kullanici_id,
            self.program_id,
            bolum_no,
            sure,
            puan,
            False
        ))
        cursor.execute("""
            UPDATE Program
            SET ortalama_puan = (
                SELECT AVG(verilen_puan)
                FROM KullaniciProgram
                WHERE program_id = %s AND verilen_puan IS NOT NULL
            )
            WHERE program_id = %s
        """, (self.program_id, self.program_id))

        conn.commit()

        cursor.close()
        conn.close()

        QMessageBox.information(self, "Başarılı", "Kaldığın yer kaydedildi.")

    def izlemeyi_tamamla(self):
        bolum_no = self.bolum_input.value()
        sure = self.program_uzunlugu
        puan = self.puan_input.value()

        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT kullanici_program_id FROM KullaniciProgram
            WHERE kullanici_id=%s AND program_id=%s
        """, (self.kullanici_id, self.program_id))

        eski_kayit = cursor.fetchone()

        if eski_kayit:
            cursor.execute("""
                UPDATE KullaniciProgram
                SET izlenen_bolum=%s,
                    kalinan_sure=%s,
                    tamamlandi_mi=%s,
                    verilen_puan=%s
                WHERE kullanici_id=%s AND program_id=%s
            """, (
                bolum_no,
                sure,
                True,
                puan,
                self.kullanici_id,
                self.program_id
            ))
        else:
            cursor.execute("""
                INSERT INTO KullaniciProgram
                (kullanici_id, program_id, izlenen_bolum, kalinan_sure, tamamlandi_mi, verilen_puan)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                self.kullanici_id,
                self.program_id,
                bolum_no,
                sure,
                True,
                puan
            ))

        cursor.execute("""
            INSERT INTO IzlemeLog
            (kullanici_id, program_id, bolum_no, izleme_suresi, verilen_puan, tamamlandi_mi)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            self.kullanici_id,
            self.program_id,
            bolum_no,
            sure,
            puan,
            True
        ))

        cursor.execute("""
            UPDATE Program
            SET izlenme_sayisi = izlenme_sayisi + 1
            WHERE program_id = %s
        """, (self.program_id,))

        cursor.execute("""
            UPDATE Program
            SET ortalama_puan = (
                SELECT AVG(verilen_puan)
                FROM KullaniciProgram
                WHERE program_id = %s AND verilen_puan IS NOT NULL
            )
            WHERE program_id = %s
        """, (self.program_id, self.program_id))

        conn.commit()

        cursor.close()
        conn.close()

        QMessageBox.information(self, "Başarılı", "İzleme tamamlandı.")


class AdminPaneli(QWidget):
    def __init__(self, admin_kullanici=None):
        super().__init__()

        self.admin = admin_kullanici

        self.setWindowTitle("Admin Paneli")
        self.setGeometry(200, 100, 900, 700)

        layout = QVBoxLayout()

        self.sonuc = QTextEdit()
        self.sonuc.setReadOnly(True)

        layout.addWidget(QLabel("=== İÇERİK YÖNETİMİ ==="))

        self.program_adi_input = QLineEdit()
        self.program_adi_input.setPlaceholderText("Program adı")

        self.aciklama_input = QLineEdit()
        self.aciklama_input.setPlaceholderText("Açıklama")

        self.program_tipi_input = QComboBox()
        self.program_tipi_input.addItems(["Film", "Dizi", "Tv Show"])

        self.bolum_sayisi_input = QSpinBox()
        self.bolum_sayisi_input.setMinimum(1)
        self.bolum_sayisi_input.setMaximum(500)

        self.uzunluk_input = QSpinBox()
        self.uzunluk_input.setMinimum(1)
        self.uzunluk_input.setMaximum(500)

        self.yil_input = QSpinBox()
        self.yil_input.setMinimum(1900)
        self.yil_input.setMaximum(2100)
        self.yil_input.setValue(2024)

        self.tur_listesi_admin = QListWidget()
        self.tur_listesi_admin.setSelectionMode(QListWidget.MultiSelection)
        self.tur_listesi_admin.setMaximumHeight(100)
        self.admin_turleri_yukle()

        icerik_btn_layout = QHBoxLayout()
        self.icerik_ekle_btn = QPushButton("İçerik Ekle")
        self.icerik_ekle_btn.clicked.connect(self.icerik_ekle)

        self.program_id_guncelle_input = QLineEdit()
        self.program_id_guncelle_input.setPlaceholderText("Güncellenecek program ID")

        self.icerik_guncelle_btn = QPushButton("İçerik Güncelle")
        self.icerik_guncelle_btn.clicked.connect(self.icerik_guncelle)

        self.program_id_sil_input = QLineEdit()
        self.program_id_sil_input.setPlaceholderText("Silinecek program ID")

        self.icerik_sil_btn = QPushButton("İçerik Sil")
        self.icerik_sil_btn.clicked.connect(self.icerik_sil)

        icerik_btn_layout.addWidget(self.icerik_ekle_btn)
        icerik_btn_layout.addWidget(self.program_id_guncelle_input)
        icerik_btn_layout.addWidget(self.icerik_guncelle_btn)
        icerik_btn_layout.addWidget(self.program_id_sil_input)
        icerik_btn_layout.addWidget(self.icerik_sil_btn)

        layout.addWidget(self.program_adi_input)
        layout.addWidget(self.aciklama_input)
        layout.addWidget(self.program_tipi_input)
        layout.addWidget(QLabel("Bölüm Sayısı"))
        layout.addWidget(self.bolum_sayisi_input)
        layout.addWidget(QLabel("Program Uzunluğu (dk)"))
        layout.addWidget(self.uzunluk_input)
        layout.addWidget(QLabel("Yayın Yılı"))
        layout.addWidget(self.yil_input)
        layout.addWidget(QLabel("Türler (çoklu seçim):"))
        layout.addWidget(self.tur_listesi_admin)
        layout.addLayout(icerik_btn_layout)

        layout.addWidget(QLabel("=== TÜR YÖNETİMİ ==="))

        tur_layout = QHBoxLayout()
        self.tur_input = QLineEdit()
        self.tur_input.setPlaceholderText("Tür adı")

        self.tur_id_guncelle_input = QLineEdit()
        self.tur_id_guncelle_input.setPlaceholderText("Güncellenecek tür ID")

        self.tur_id_sil_input = QLineEdit()
        self.tur_id_sil_input.setPlaceholderText("Silinecek tür ID")

        self.tur_ekle_btn = QPushButton("Tür Ekle")
        self.tur_ekle_btn.clicked.connect(self.tur_ekle)

        self.tur_guncelle_btn = QPushButton("Tür Güncelle")
        self.tur_guncelle_btn.clicked.connect(self.tur_guncelle)

        self.tur_sil_btn = QPushButton("Tür Sil")
        self.tur_sil_btn.clicked.connect(self.tur_sil)

        tur_layout.addWidget(self.tur_input)
        tur_layout.addWidget(self.tur_ekle_btn)
        tur_layout.addWidget(self.tur_id_guncelle_input)
        tur_layout.addWidget(self.tur_guncelle_btn)
        tur_layout.addWidget(self.tur_id_sil_input)
        tur_layout.addWidget(self.tur_sil_btn)
        layout.addLayout(tur_layout)

        layout.addWidget(QLabel("=== KULLANICI YÖNETİMİ ==="))

        kullanici_layout = QHBoxLayout()
        self.kullanici_id_input = QLineEdit()
        self.kullanici_id_input.setPlaceholderText("Kullanıcı ID")

        self.kullanicilar_btn = QPushButton("Kullanıcıları Listele")
        self.kullanicilar_btn.clicked.connect(self.kullanicilari_listele)

        self.pasif_btn = QPushButton("Pasif Yap")
        self.pasif_btn.clicked.connect(self.kullanici_pasif)

        self.aktif_btn = QPushButton("Aktif Yap")
        self.aktif_btn.clicked.connect(self.kullanici_aktif)

        self.kullanici_detay_btn = QPushButton("Kullanıcı Detayı")
        self.kullanici_detay_btn.clicked.connect(self.kullanici_detay)

        kullanici_layout.addWidget(self.kullanici_id_input)
        kullanici_layout.addWidget(self.kullanicilar_btn)
        kullanici_layout.addWidget(self.pasif_btn)
        kullanici_layout.addWidget(self.aktif_btn)
        kullanici_layout.addWidget(self.kullanici_detay_btn)
        layout.addLayout(kullanici_layout)

        layout.addWidget(QLabel("=== RAPORLAMA ==="))

        rapor_layout = QHBoxLayout()
        self.encok_btn = QPushButton("En Çok İzlenen 10")
        self.encok_btn.clicked.connect(self.en_cok_izlenen)

        self.enpuan_btn = QPushButton("En Yüksek Puanlı 10")
        self.enpuan_btn.clicked.connect(self.en_yuksek_puanli)

        self.tur_rapor_btn = QPushButton("En Çok İzlenen Türler")
        self.tur_rapor_btn.clicked.connect(self.tur_raporu)

        self.aktif_kullanici_btn = QPushButton("En Aktif Kullanıcılar")
        self.aktif_kullanici_btn.clicked.connect(self.aktif_kullanicilar)

        self.son7gun_btn = QPushButton("Son 7 Gün")
        self.son7gun_btn.clicked.connect(self.son_7_gun)

        self.genel_istatistik_btn = QPushButton("Genel İstatistikler")
        self.genel_istatistik_btn.clicked.connect(self.genel_istatistikler)

        rapor_layout.addWidget(self.encok_btn)
        rapor_layout.addWidget(self.enpuan_btn)
        rapor_layout.addWidget(self.tur_rapor_btn)
        rapor_layout.addWidget(self.aktif_kullanici_btn)
        rapor_layout.addWidget(self.son7gun_btn)
        rapor_layout.addWidget(self.genel_istatistik_btn)
        layout.addLayout(rapor_layout)

        self.cikis_btn = QPushButton("Çıkış Yap")
        self.cikis_btn.clicked.connect(self.cikis_yap)

        layout.addWidget(self.sonuc)
        layout.addWidget(self.cikis_btn)

        self.setLayout(layout)

    def admin_turleri_yukle(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()
        cursor.execute("SELECT tur_id, tur_adi FROM Tur ORDER BY tur_adi")
        for row in cursor.fetchall():
            item = QListWidgetItem(f"{row[0]} - {row[1]}")
            item.setData(32, row[0])
            self.tur_listesi_admin.addItem(item)
        cursor.close()
        conn.close()

    def icerik_ekle(self):
        program_adi = self.program_adi_input.text().strip()
        aciklama = self.aciklama_input.text().strip()
        program_tipi = self.program_tipi_input.currentText()
        bolum_sayisi = self.bolum_sayisi_input.value()
        uzunluk = self.uzunluk_input.value()
        yil = self.yil_input.value()

        if program_adi == "":
            QMessageBox.warning(self, "Hata", "Program adı boş olamaz.")
            return

        secilen_turler = [item.data(32) for item in self.tur_listesi_admin.selectedItems()]

        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Program
            (program_adi, aciklama, program_tipi, bolum_sayisi, program_uzunlugu, yayin_yili)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (program_adi, aciklama, program_tipi, bolum_sayisi, uzunluk, yil))

        program_id = cursor.lastrowid

        for tur_id in secilen_turler:
            cursor.execute("INSERT INTO ProgramTur (program_id, tur_id) VALUES (%s, %s)",
                          (program_id, tur_id))

        conn.commit()
        cursor.close()
        conn.close()

        QMessageBox.information(self, "Başarılı", "İçerik eklendi.")

    def icerik_guncelle(self):
        program_id = self.program_id_guncelle_input.text().strip()
        program_adi = self.program_adi_input.text().strip()

        if not program_id or not program_adi:
            QMessageBox.warning(self, "Hata", "Program ID ve adı giriniz.")
            return

        aciklama = self.aciklama_input.text().strip()
        program_tipi = self.program_tipi_input.currentText()
        bolum_sayisi = self.bolum_sayisi_input.value()
        uzunluk = self.uzunluk_input.value()
        yil = self.yil_input.value()

        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Program
            SET program_adi=%s, aciklama=%s, program_tipi=%s,
                bolum_sayisi=%s, program_uzunlugu=%s, yayin_yili=%s
            WHERE program_id=%s
        """, (program_adi, aciklama, program_tipi, bolum_sayisi, uzunluk, yil, program_id))

        secilen_turler = [item.data(32) for item in self.tur_listesi_admin.selectedItems()]
        if secilen_turler:
            cursor.execute("DELETE FROM ProgramTur WHERE program_id=%s", (program_id,))
            for tur_id in secilen_turler:
                cursor.execute("INSERT INTO ProgramTur (program_id, tur_id) VALUES (%s, %s)",
                              (program_id, tur_id))

        conn.commit()
        cursor.close()
        conn.close()

        QMessageBox.information(self, "Başarılı", "İçerik güncellendi.")

    def icerik_sil(self):
        program_id = self.program_id_sil_input.text().strip()

        if program_id == "":
            QMessageBox.warning(self, "Hata", "Program ID gir.")
            return

        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Program WHERE program_id=%s", (program_id,))
        conn.commit()

        cursor.close()
        conn.close()

        QMessageBox.information(self, "Başarılı", "İçerik silindi.")

    def tur_ekle(self):
        tur_adi = self.tur_input.text().strip()

        if tur_adi == "":
            QMessageBox.warning(self, "Hata", "Tür adı boş olamaz.")
            return

        conn = baglanti_olustur()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO Tur (tur_adi) VALUES (%s)", (tur_adi,))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Tür eklendi.")
            self.tur_listesi_admin.clear()
            self.admin_turleri_yukle()
        except Exception as e:
            QMessageBox.warning(self, "Hata", str(e))

        cursor.close()
        conn.close()

    def tur_sil(self):
        tur_id = self.tur_id_sil_input.text().strip()

        if not tur_id:
            QMessageBox.warning(self, "Hata", "Tür ID giriniz.")
            return

        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM ProgramTur WHERE tur_id=%s", (tur_id,))
        sayi = cursor.fetchone()[0]

        if sayi > 0:
            QMessageBox.warning(self, "Hata", f"Bu türe bağlı {sayi} içerik var. Önce içerikleri güncelleyin.")
            cursor.close()
            conn.close()
            return

        cursor.execute("DELETE FROM Tur WHERE tur_id=%s", (tur_id,))
        conn.commit()
        cursor.close()
        conn.close()

        QMessageBox.information(self, "Başarılı", "Tür silindi.")
        self.tur_listesi_admin.clear()
        self.admin_turleri_yukle()

    def tur_guncelle(self):
        tur_id = self.tur_id_guncelle_input.text().strip()
        yeni_tur_adi = self.tur_input.text().strip()

        if not tur_id or not yeni_tur_adi:
            QMessageBox.warning(self, "Hata", "Tür ID ve yeni tür adını giriniz.")
            return

        conn = baglanti_olustur()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE Tur SET tur_adi=%s WHERE tur_id=%s", (yeni_tur_adi, tur_id))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Tür güncellendi.")
            self.tur_listesi_admin.clear()
            self.admin_turleri_yukle()
        except Exception as e:
            QMessageBox.warning(self, "Hata", str(e))

        cursor.close()
        conn.close()

    def kullanicilari_listele(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT k.kullanici_id, k.ad, k.soyad, k.email, k.ulke, k.aktif_mi, r.rol_adi
            FROM Kullanici k
            JOIN Rol r ON k.rol_id = r.rol_id
        """)

        yazi = "Kullanıcılar:\n\n"

        for row in cursor.fetchall():
            aktif = "Aktif" if row[5] else "Pasif"
            yazi += f"ID: {row[0]} | {row[1]} {row[2]} | {row[3]} | Ülke: {row[4]} | {aktif} | Rol: {row[6]}\n"

        self.sonuc.setText(yazi)

        cursor.close()
        conn.close()

    def kullanici_pasif(self):
        kullanici_id = self.kullanici_id_input.text().strip()
        if not kullanici_id:
            QMessageBox.warning(self, "Hata", "Kullanıcı ID giriniz.")
            return
        if self.admin:
            self.admin.kullanici_pasif_yap(int(kullanici_id))
        else:
            conn = baglanti_olustur()
            cursor = conn.cursor()
            cursor.execute("UPDATE Kullanici SET aktif_mi=FALSE WHERE kullanici_id=%s", (kullanici_id,))
            conn.commit()
            cursor.close()
            conn.close()
        QMessageBox.information(self, "Başarılı", "Kullanıcı pasif yapıldı.")

    def kullanici_aktif(self):
        kullanici_id = self.kullanici_id_input.text().strip()
        if not kullanici_id:
            QMessageBox.warning(self, "Hata", "Kullanıcı ID giriniz.")
            return
        if self.admin:
            self.admin.kullanici_aktif_yap(int(kullanici_id))
        else:
            conn = baglanti_olustur()
            cursor = conn.cursor()
            cursor.execute("UPDATE Kullanici SET aktif_mi=TRUE WHERE kullanici_id=%s", (kullanici_id,))
            conn.commit()
            cursor.close()
            conn.close()
        QMessageBox.information(self, "Başarılı", "Kullanıcı aktif yapıldı.")

    def kullanici_detay(self):
        kullanici_id = self.kullanici_id_input.text().strip()
        if not kullanici_id:
            QMessageBox.warning(self, "Hata", "Kullanıcı ID giriniz.")
            return

        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ad, soyad, email, dogum_tarihi, ulke, aktif_mi
            FROM Kullanici WHERE kullanici_id=%s
        """, (kullanici_id,))
        k = cursor.fetchone()

        if not k:
            QMessageBox.warning(self, "Hata", "Kullanıcı bulunamadı.")
            cursor.close()
            conn.close()
            return

        cursor.execute("""
            SELECT COALESCE(SUM(izleme_suresi), 0), COUNT(DISTINCT program_id)
            FROM IzlemeLog WHERE kullanici_id=%s
        """, (kullanici_id,))
        istatistik = cursor.fetchone()

        cursor.execute("""
            SELECT p.program_adi, i.izleme_tarihi, i.bolum_no, i.izleme_suresi, i.tamamlandi_mi
            FROM IzlemeLog i
            JOIN Program p ON i.program_id = p.program_id
            WHERE i.kullanici_id=%s
            ORDER BY i.izleme_tarihi DESC
            LIMIT 10
        """, (kullanici_id,))
        gecmis = cursor.fetchall()

        yazi = f"Kullanıcı: {k[0]} {k[1]} | {k[2]} | {k[4]} | {'Aktif' if k[5] else 'Pasif'}\n"
        yazi += f"Toplam İzleme: {istatistik[0]} dk | İzlenen İçerik: {istatistik[1]}\n\nSon İzlemeler:\n"
        for g in gecmis:
            yazi += f"  {g[0]} | {g[1]} | Bölüm: {g[2]} | {g[3]} dk | {'Tamamlandı' if g[4] else 'Devam ediyor'}\n"

        self.sonuc.setText(yazi)
        cursor.close()
        conn.close()

    def en_cok_izlenen(self):
        sonuclar = ReportService.en_cok_izlenen()
        yazi = "En Çok İzlenen 10 İçerik:\n\n"
        for row in sonuclar:
            yazi += f"ID: {row[0]} | {row[1]} | Tip: {row[2]} | İzlenme: {row[3]}\n"
        self.sonuc.setText(yazi)

    def en_yuksek_puanli(self):
        sonuclar = ReportService.en_yuksek_puanli()
        yazi = "En Yüksek Puanlı 10 İçerik:\n\n"
        for row in sonuclar:
            yazi += f"ID: {row[0]} | {row[1]} | Tip: {row[2]} | Puan: {row[3]}\n"
        self.sonuc.setText(yazi)

    def tur_raporu(self):
        sonuclar = ReportService.en_cok_izlenen_turler()
        yazi = "En Çok İzlenen Türler:\n\n"
        for row in sonuclar:
            yazi += f"Tür: {row[0]} | Toplam İzlenme: {row[1]}\n"
        self.sonuc.setText(yazi)

    def aktif_kullanicilar(self):
        sonuclar = ReportService.en_aktif_kullanicilar()
        yazi = "En Aktif Kullanıcılar:\n\n"
        for row in sonuclar:
            yazi += f"ID: {row[0]} | {row[1]} {row[2]} | Toplam İzleme: {row[3]} dk\n"
        self.sonuc.setText(yazi)

    def son_7_gun(self):
        sonuclar = ReportService.son_7_gun_izlenenler()
        yazi = "Son 7 Günde İzlenen İçerikler:\n\n"
        for row in sonuclar:
            yazi += f"{row[0]} | İzlenme: {row[1]}\n"
        self.sonuc.setText(yazi)

    def genel_istatistikler(self):
        conn = baglanti_olustur()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Kullanici WHERE rol_id=1")
        toplam_kullanici = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(izlenme_sayisi) FROM Program")
        toplam_izlenme = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM KullaniciProgram WHERE verilen_puan IS NOT NULL")
        toplam_puan = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        yazi = f"""Genel İstatistikler:

Toplam Kullanıcı Sayısı: {toplam_kullanici}
Toplam İzlenme Sayısı: {toplam_izlenme}
Toplam Verilen Puan: {toplam_puan}
"""
        self.sonuc.setText(yazi)

    def cikis_yap(self):
        self.login = LoginEkrani()
        self.login.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(NETFLIX_STYLE)
    window = LoginEkrani()
    window.show()
    sys.exit(app.exec_())

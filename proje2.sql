CREATE DATABASE IF NOT EXISTS netflix_proje;
USE netflix_proje;

CREATE TABLE IF NOT EXISTS Rol (
    rol_id INT AUTO_INCREMENT PRIMARY KEY,
    rol_adi VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Program (
    program_id INT AUTO_INCREMENT PRIMARY KEY,
    program_adi VARCHAR(255) NOT NULL,
    aciklama TEXT,
    program_tipi VARCHAR(50) NOT NULL,
    bolum_sayisi INT DEFAULT 1,
    program_uzunlugu INT DEFAULT 120,
    yayin_yili INT DEFAULT 2024,
    ortalama_puan FLOAT DEFAULT 0,
    izlenme_sayisi INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Tur (
    tur_id INT AUTO_INCREMENT PRIMARY KEY,
    tur_adi VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS ProgramTur (
    program_id INT,
    tur_id INT,
    PRIMARY KEY (program_id, tur_id),
    FOREIGN KEY (program_id) REFERENCES Program(program_id) ON DELETE CASCADE,
    FOREIGN KEY (tur_id) REFERENCES Tur(tur_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Kullanici (
    kullanici_id INT AUTO_INCREMENT PRIMARY KEY,
    rol_id INT NOT NULL DEFAULT 1,
    ad VARCHAR(100) NOT NULL,
    soyad VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    sifre VARCHAR(255) NOT NULL,
    dogum_tarihi DATE,
    cinsiyet VARCHAR(20),
    ulke VARCHAR(100),
    aktif_mi BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (rol_id) REFERENCES Rol(rol_id)
);

CREATE TABLE IF NOT EXISTS KullaniciTur (
    kullanici_id INT,
    tur_id INT,
    PRIMARY KEY (kullanici_id, tur_id),
    FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    FOREIGN KEY (tur_id) REFERENCES Tur(tur_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Bolum (
    bolum_id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    bolum_no INT NOT NULL,
    bolum_adi VARCHAR(255),
    bolum_suresi INT DEFAULT 45,
    FOREIGN KEY (program_id) REFERENCES Program(program_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Favori (
    kullanici_id INT,
    program_id INT,
    PRIMARY KEY (kullanici_id, program_id),
    FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES Program(program_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KullaniciProgram (
    kullanici_program_id INT AUTO_INCREMENT PRIMARY KEY,
    kullanici_id INT NOT NULL,
    program_id INT NOT NULL,
    izlenen_bolum INT DEFAULT 1,
    kalinan_sure INT DEFAULT 0,
    tamamlandi_mi BOOLEAN DEFAULT FALSE,
    verilen_puan INT CHECK (verilen_puan BETWEEN 1 AND 10),
    FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES Program(program_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS IzlemeLog (
    izleme_id INT AUTO_INCREMENT PRIMARY KEY,
    kullanici_id INT,
    program_id INT,
    bolum_no INT DEFAULT 1,
    izleme_suresi INT DEFAULT 0,
    verilen_puan INT CHECK (verilen_puan BETWEEN 1 AND 10),
    tamamlandi_mi BOOLEAN DEFAULT FALSE,
    izleme_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES Program(program_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS OturumLog (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    kullanici_id INT,
    giris_zamani DATETIME DEFAULT CURRENT_TIMESTAMP,
    cikis_zamani DATETIME,
    FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE
);


INSERT IGNORE INTO Rol (rol_adi) VALUES ('kullanici'), ('admin');

INSERT IGNORE INTO Tur (tur_adi) VALUES
('Aksiyon'), ('Komedi'), ('Drama'), ('Korku'), ('Bilim Kurgu'),
('Romantik'), ('Belgesel'), ('Animasyon'), ('Suç'), ('Gerilim');

INSERT IGNORE INTO Kullanici (rol_id, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, ulke, aktif_mi)
VALUES (2, 'Admin', 'User', 'admin@test.com', '123456', '1990-01-01', 'Erkek', 'Türkiye', TRUE);

INSERT IGNORE INTO Kullanici (rol_id, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, ulke, aktif_mi)
VALUES (2, 'Batuhan', 'Uzuner', '230501020@kocaelisaglik.edu.tr', '123456', '2001-01-01', 'Erkek', 'Türkiye', TRUE);

INSERT IGNORE INTO Kullanici (rol_id, ad, soyad, email, sifre, dogum_tarihi, cinsiyet, ulke, aktif_mi)
VALUES (1, 'Test', 'Kullanici', 'test@test.com', '123456', '1995-05-15', 'Kadın', 'Türkiye', TRUE);

INSERT IGNORE INTO KullaniciTur (kullanici_id, tur_id)
SELECT k.kullanici_id, t.tur_id FROM Kullanici k, Tur t
WHERE k.email = 'test@test.com' AND t.tur_adi IN ('Drama', 'Aksiyon ve Macera', 'Bilim Kurgu ve Fantastik Yapımlar');


INSERT IGNORE INTO Tur (tur_adi) VALUES
('Aksiyon ve Macera'),
('Bilim Kurgu ve Fantastik Yapımlar'),
('Romantik'),
('Belgesel'),
('Bilim ve Doğa'),
('Çocuk ve Aile'),
('Korku'),
('Anime'),
('Reality Program');

INSERT IGNORE INTO Program (program_adi, aciklama, program_tipi, bolum_sayisi, program_uzunlugu, yayin_yili, ortalama_puan, izlenme_sayisi) VALUES
('Recep İvedik 6', 'Türk komedi filmi', 'Film', 1, 110, 2019, 6.2, 8500),
('Assassin''s Creed', 'Video oyunundan uyarlanan aksiyon filmi', 'Film', 1, 115, 2016, 5.7, 12000),
('Alaca Karanlık', 'Vampir temalı romantik film', 'Film', 1, 122, 2008, 5.2, 15000),
('Yüzüklerin Efendisi İki Kule', 'Orta Dünya destanının ikinci filmi', 'Film', 1, 179, 2002, 8.7, 25000),
('Maske', 'Jim Carrey''nin komedi filmi', 'Film', 1, 101, 1994, 6.9, 9500),
('Kara Şövalye', 'Batman''in Joker ile mücadelesi', 'Film', 1, 152, 2008, 9.0, 30000),
('Sherlock Holmes', 'Ünlü dedektifin maceraları', 'Film', 1, 128, 2009, 7.6, 14000),
('Yüzüklerin Efendisi Kralın Dönüşü', 'Orta Dünya destanının final filmi', 'Film', 1, 201, 2003, 8.9, 28000),
('Transformers Kayıp Çağ', 'Robotların dünya savaşı', 'Film', 1, 165, 2014, 5.6, 11000),
('Başlangıç', 'Rüya içinde rüya konsepti', 'Film', 1, 148, 2010, 8.8, 22000),
('Interstellar', 'Uzay ve zaman yolculuğu', 'Film', 1, 169, 2014, 8.6, 24000),
('Harry Potter Ölüm Yadigarları', 'Harry Potter serisinin finali', 'Film', 1, 130, 2011, 8.1, 19000),
('Jurassic World', 'Dinozorların geri dönüşü', 'Film', 1, 124, 2015, 7.0, 16000),
('Fantastik Canavarlar', 'Harry Potter evreninden spin-off', 'Film', 1, 133, 2016, 7.3, 13000),
('Ninja Kaplumbağalar', 'Mutant kaplumbağaların maceraları', 'Film', 1, 101, 2014, 5.8, 8000),
('Kuşlarla Dans', 'Kuşların göç hikayesi belgeseli', 'Film', 1, 98, 2001, 7.9, 3500),
('Mission Blue', 'Okyanus koruma belgeseli', 'Film', 1, 94, 2014, 8.0, 2800),
('Mercan Peşinde', 'Mercan resifleri belgeseli', 'Film', 1, 89, 2017, 8.1, 3200),
('Dream Big', 'Mühendislik belgeseli', 'Film', 1, 42, 2017, 6.8, 1500),
('Ay''daki Son Adam', 'Neil Armstrong belgeseli', 'Film', 1, 93, 2018, 7.3, 4200),
('Plastik Okyanus', 'Plastik kirliliği belgeseli', 'Film', 1, 100, 2016, 8.0, 3800),
('Rakamlarla Tahmin', 'İstatistik ve tahmin belgeseli', 'Film', 1, 75, 2018, 6.5, 2100),
('Ben Efsaneyim', 'Zombi apokalipsi filmi', 'Film', 1, 101, 2007, 7.2, 14500),
('Arif V 216', 'Türk bilim kurgu komedisi', 'Film', 1, 125, 2018, 7.3, 9800),
('PK', 'Hint bilim kurgu komedisi', 'Film', 1, 153, 2014, 8.1, 11200),
('Örümcek Adam', 'Peter Parker''ın hikayesi', 'Film', 1, 121, 2002, 7.3, 18000),
('Jurassic Park', 'Dinozor parkı filmi', 'Film', 1, 127, 1993, 8.1, 21000),
('Frankenstein', 'Klasik korku filmi', 'Film', 1, 94, 2015, 6.1, 7500),
('Gezegenimiz', 'Dünya belgeseli', 'Film', 1, 83, 2019, 9.3, 5600),
('72 Sevimli Hayvan', 'Hayvan belgeseli', 'Film', 1, 75, 2013, 7.8, 2900),
('Kuşçular', 'Kuş gözlemcileri belgeseli', 'Film', 1, 82, 2019, 7.2, 1800),
('Marsta Keşif', 'Mars keşif belgeseli', 'Film', 1, 88, 2016, 7.5, 3400),
('Pandemic', 'Salgın hastalık belgeseli', 'Film', 1, 95, 2020, 6.6, 8900),
('Pokemon', 'Pokemon macerası', 'Film', 1, 75, 1998, 6.0, 7200),
('Şirinler', 'Mavi cüceler filmi', 'Film', 1, 103, 2011, 5.4, 6800),
('Charlie''nin Çikolata Fabrikası', 'Willy Wonka''nın fabrikası', 'Film', 1, 115, 2005, 6.7, 9100),
('Alvin ve Sincaplar', 'Konuşan sincaplar', 'Film', 1, 92, 2007, 5.3, 5900),
('Scooby-Doo', 'Gizemli olayları çözen köpek', 'Film', 1, 86, 2002, 5.1, 6200),
('Kung Fu Panda', 'Kung fu yapan panda', 'Film', 1, 92, 2008, 7.6, 12500),
('Mr. Bean Tatilde', 'Mr. Bean''in tatil maceraları', 'Film', 1, 89, 2007, 6.4, 8700),
('Shrek', 'Yeşil dev''in hikayesi', 'Film', 1, 90, 2001, 7.8, 15500),
('Mega Zeka', 'Süper zeki bebek', 'Film', 1, 96, 2010, 6.4, 5400),
('Bizi Hatırla', 'Duygusal Türk filmi', 'Film', 1, 105, 2018, 6.9, 4800),
('Delibal', 'Romantik Türk filmi', 'Film', 1, 114, 2015, 7.5, 7300),
('Kardeşim Benim', 'Komedi drama Türk filmi', 'Film', 1, 111, 2016, 7.2, 6100),
('Dangal', 'Hint güreş filmi', 'Film', 1, 161, 2016, 8.4, 9500),
('Yerçekimi', 'Uzayda hayatta kalma', 'Film', 1, 91, 2013, 7.7, 13200),
('Jaws', 'Köpekbalığı korku filmi', 'Film', 1, 124, 1975, 8.0, 17800),
('Da Vinci Şifresi', 'Dan Brown romanından uyarlama', 'Film', 1, 149, 2006, 6.6, 14300);

INSERT IGNORE INTO Program (program_adi, aciklama, program_tipi, bolum_sayisi, program_uzunlugu, yayin_yili, ortalama_puan, izlenme_sayisi) VALUES
('Marvel Iron Fist', 'Marvel süper kahraman dizisi', 'Dizi', 23, 50, 2017, 6.4, 8900),
('Ejderhalar', 'Ejderha eğitimi dizisi', 'Dizi', 118, 22, 2012, 7.9, 6700),
('Diriliş Ertuğrul', 'Osmanlı tarihi dizisi', 'Dizi', 150, 120, 2014, 8.9, 25000),
('Trol Avcıları: Arcadia Hikayeleri', 'Animasyon macera dizisi', 'Dizi', 13, 24, 2016, 8.1, 5200),
('How I Met Your Mother', 'Romantik komedi dizisi', 'Dizi', 208, 22, 2005, 8.3, 19500),
('Leyla ile Mecnun', 'Türk absürt komedi dizisi', 'Dizi', 143, 40, 2011, 9.1, 12800),
('Beni Böyle Sev', 'Türk romantik dram dizisi', 'Dizi', 14, 120, 2013, 7.8, 8400),
('Patron Bebek Yine İş Başında', 'Animasyon komedi dizisi', 'Dizi', 50, 23, 2018, 6.2, 4100),
('Atiye', 'Türk gizem dizisi', 'Dizi', 24, 45, 2019, 6.8, 9200),
('Maşa ve Koca Ayı', 'Çocuk animasyon dizisi', 'Dizi', 104, 7, 2009, 7.2, 11500),
('Sünger Bob', 'Deniz altı komedi dizisi', 'Dizi', 268, 11, 1999, 8.1, 18700),
('Stranger Things', 'Bilim kurgu korku dizisi', 'Dizi', 34, 50, 2016, 8.7, 28000),
('The Originals', 'Vampir drama dizisi', 'Dizi', 92, 42, 2013, 8.2, 14600),
('Angry Birds', 'Kızgın kuşlar animasyon dizisi', 'Dizi', 104, 3, 2013, 5.7, 3800),
('Criminal', 'Suç gerilim dizisi', 'Dizi', 12, 45, 2019, 7.6, 7900),
('Beyblade', 'Anime aksiyon dizisi', 'Dizi', 51, 23, 2001, 6.5, 8200),
('Sonic X', 'Sonic animasyon dizisi', 'Dizi', 78, 22, 2003, 6.4, 7100),
('Kung Fu Panda Muhteşem Sırlar', 'Kung Fu Panda spin-off', 'Dizi', 26, 23, 2011, 7.2, 4900),
('The Blacklist', 'Suç gerilim dizisi', 'Dizi', 174, 43, 2013, 8.0, 16800);

INSERT IGNORE INTO Program (program_adi, aciklama, program_tipi, bolum_sayisi, program_uzunlugu, yayin_yili, ortalama_puan, izlenme_sayisi) VALUES
('Dünyanın En Sıra Dışı Evleri', 'Mimari reality show', 'Tv Show', 10, 45, 2020, 7.8, 3500),
('Car Masters', 'Araba restorasyonu reality show', 'Tv Show', 24, 45, 2018, 7.5, 4200),
('Büyük Tasarımlar', 'Tasarım reality show', 'Tv Show', 12, 50, 2019, 8.1, 3800),
('Basketball or Nothing', 'Basketbol belgesel dizisi', 'Tv Show', 6, 40, 2019, 7.4, 2100),
('The Big Family Cooking', 'Aile yemek yarışması', 'Tv Show', 8, 50, 2020, 6.9, 2800),
('Sıradışı Kulübeler', 'Kulübe yapımı reality show', 'Tv Show', 16, 42, 2017, 7.6, 3200);



INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Recep İvedik 6' AND t.tur_adi IN ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Assassin''s Creed' AND t.tur_adi IN ('Aksiyon ve Macera', 'Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Alaca Karanlık' AND t.tur_adi IN ('Aksiyon ve Macera', 'Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Yüzüklerin Efendisi İki Kule' AND t.tur_adi IN ('Aksiyon ve Macera', 'Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Maske' AND t.tur_adi IN ('Aksiyon ve Macera', 'Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Kara Şövalye' AND t.tur_adi IN ('Aksiyon ve Macera', 'Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Sherlock Holmes' AND t.tur_adi IN ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Yüzüklerin Efendisi Kralın Dönüşü' AND t.tur_adi IN ('Aksiyon ve Macera', 'Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Transformers Kayıp Çağ' AND t.tur_adi IN ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Başlangıç' AND t.tur_adi IN ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Interstellar' AND t.tur_adi IN ('Aksiyon ve Macera', 'Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Harry Potter Ölüm Yadigarları' AND t.tur_adi IN ('Aksiyon ve Macera', 'Bilim Kurgu ve Fantastik Yapımlar', 'Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Jurassic World' AND t.tur_adi IN ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Fantastik Canavarlar' AND t.tur_adi IN ('Aksiyon ve Macera', 'Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Ninja Kaplumbağalar' AND t.tur_adi IN ('Aksiyon ve Macera', 'Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi IN ('Kuşlarla Dans', 'Mission Blue', 'Mercan Peşinde', 'Dream Big', 'Ay''daki Son Adam', 'Plastik Okyanus', 'Rakamlarla Tahmin')
AND t.tur_adi = 'Belgesel';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Ben Efsaneyim' AND t.tur_adi IN ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Arif V 216' AND t.tur_adi IN ('Bilim Kurgu ve Fantastik Yapımlar', 'Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'PK' AND t.tur_adi IN ('Bilim Kurgu ve Fantastik Yapımlar', 'Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Örümcek Adam' AND t.tur_adi IN ('Aksiyon ve Macera', 'Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Jurassic Park' AND t.tur_adi IN ('Bilim Kurgu ve Fantastik Yapımlar', 'Aksiyon');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Frankenstein' AND t.tur_adi IN ('Bilim Kurgu ve Fantastik Yapımlar', 'Aksiyon', 'Korku');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi IN ('Gezegenimiz', '72 Sevimli Hayvan', 'Kuşçular', 'Marsta Keşif', 'Pandemic')
AND t.tur_adi IN ('Belgesel', 'Bilim ve Doğa');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi IN ('Pokemon', 'Alvin ve Sincaplar', 'Scooby-Doo', 'Mr. Bean Tatilde')
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Şirinler' AND t.tur_adi IN ('Çocuk ve Aile', 'Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Charlie''nin Çikolata Fabrikası' AND t.tur_adi IN ('Çocuk ve Aile', 'Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Kung Fu Panda' AND t.tur_adi IN ('Çocuk ve Aile', 'Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Shrek' AND t.tur_adi IN ('Çocuk ve Aile', 'Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Mega Zeka' AND t.tur_adi IN ('Çocuk ve Aile', 'Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Bizi Hatırla' AND t.tur_adi = 'Drama';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Delibal' AND t.tur_adi IN ('Drama', 'Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Kardeşim Benim' AND t.tur_adi IN ('Drama', 'Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Dangal' AND t.tur_adi = 'Drama';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Yerçekimi' AND t.tur_adi IN ('Bilim Kurgu', 'Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Jaws' AND t.tur_adi = 'Gerilim';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Da Vinci Şifresi' AND t.tur_adi = 'Gerilim';


INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Marvel Iron Fist' AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Ejderhalar' AND t.tur_adi IN ('Çocuk ve Aile', 'Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Diriliş Ertuğrul' AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Trol Avcıları: Arcadia Hikayeleri' AND t.tur_adi IN ('Çocuk ve Aile', 'Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'How I Met Your Mother' AND t.tur_adi = 'Romantik';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Leyla ile Mecnun' AND t.tur_adi = 'Romantik';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Beni Böyle Sev' AND t.tur_adi IN ('Drama', 'Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Patron Bebek Yine İş Başında' AND t.tur_adi IN ('Çocuk ve Aile', 'Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Atiye' AND t.tur_adi IN ('Aksiyon ve Macera', 'Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Maşa ve Koca Ayı' AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Sünger Bob' AND t.tur_adi IN ('Çocuk ve Aile', 'Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Stranger Things' AND t.tur_adi IN ('Aksiyon ve Macera', 'Korku');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'The Originals' AND t.tur_adi IN ('Drama', 'Korku');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Angry Birds' AND t.tur_adi IN ('Çocuk ve Aile', 'Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Criminal' AND t.tur_adi = 'Gerilim';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Beyblade' AND t.tur_adi IN ('Anime', 'Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Sonic X' AND t.tur_adi IN ('Anime', 'Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'Kung Fu Panda Muhteşem Sırlar' AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi = 'The Blacklist' AND t.tur_adi IN ('Aksiyon ve Macera', 'Gerilim');


INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id FROM Program p, Tur t
WHERE p.program_adi IN ('Dünyanın En Sıra Dışı Evleri', 'Car Masters', 'Büyük Tasarımlar', 'Basketball or Nothing', 'The Big Family Cooking', 'Sıradışı Kulübeler')
AND t.tur_adi = 'Reality Program';

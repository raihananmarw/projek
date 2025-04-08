-- Membuat database
CREATE DATABASE arsip_arka;

-- Menggunakan database
USE arsip_arka;

-- Tabel untuk surat masuk
CREATE TABLE surat_masuk (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_surat VARCHAR(100) NOT NULL,
    tanggal_masuk DATE NOT NULL,
    pengirim VARCHAR(100) NOT NULL,
    perihal TEXT NOT NULL
);

-- Tabel untuk surat keluar
CREATE TABLE surat_keluar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_surat VARCHAR(100) NOT NULL,
    tanggal_keluar DATE NOT NULL,
    penerima VARCHAR(100) NOT NULL,
    perihal TEXT NOT NULL
);

-- Tabel untuk pengguna (opsional untuk login)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Menambahkan pengguna default (username: admin, password: admin123)
INSERT INTO users (username, password) VALUES ('admin', MD5('admin123'));
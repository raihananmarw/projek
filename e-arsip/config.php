<?php
// File: config.php

// Konfigurasi database
$host = 'localhost';
$username = 'root';
$password = '';
$database = 'arsip_arka';

// Membuat koneksi ke database
$conn = mysqli_connect($host, $username, $password, $database);

// Periksa koneksi
if (!$conn) {
    die("Koneksi ke database gagal: " . mysqli_connect_error());
}

?>
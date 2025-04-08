<?php
session_start();
include 'config.php';

// Periksa apakah pengguna sudah login
if (!isset($_SESSION['logged_in'])) {
    header('Location: login.php');
    exit;
}

$username = $_SESSION['username'];
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-ARSIP ARIA KAMUNING</title>
    <link rel="stylesheet" href="css/index.css">
</head>
<body>
    <?php include 'header.php'; ?>

    <main>
        <?php
        // Tentukan halaman berdasarkan parameter "page"
        if (isset($_GET['page'])) {
            $page = $_GET['page'];
            switch ($page) {
                case 'dashboard':
                    include 'dashboard.php';
                    break;
                case 'surat_masuk':
                    include 'surat_masuk.php';
                    break;
                case 'laporan':
                    include 'laporan.php';
                    break;
                default:
                    echo "<h2>Halaman tidak ditemukan</h2>";
                    break;
            }
        } else {
            // Halaman default
            include 'dashboard.php';
        }
        ?>
    </main>

    <?php include 'footer.php'; ?>
</body>
</html>
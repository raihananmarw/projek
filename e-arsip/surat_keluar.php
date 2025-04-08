<?php
session_start();
include 'config.php'; // Load konfigurasi database

// Periksa apakah pengguna sudah login
if (!isset($_SESSION['logged_in'])) {
    header('Location: login.php');
    exit;
}

// Fungsi untuk menambah surat
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['add_surat'])) {
    $tanggal = $_POST['tanggal'];
    $pengirim = $_POST['pengirim'];
    $perihal = $_POST['perihal'];

    // Upload file
    $file = $_FILES['file'];
    $fileName = $file['name'];
    $fileTmpName = $file['tmp_name'];
    $filePath = "uploads/" . basename($fileName);

    // Pindahkan file ke folder uploads
    if (move_uploaded_file($fileTmpName, $filePath)) {
        $query = "INSERT INTO surat_masuk (tanggal_keluar, pengirim, perihal, file_path) VALUES ('$tanggal', '$pengirim', '$perihal', '$filePath')";
        mysqli_query($conn, $query);
    }
}

// Fungsi untuk menghapus surat
if (isset($_GET['delete_id'])) {
    $id = $_GET['delete_id'];

    // Hapus file terkait
    $result = mysqli_query($conn, "SELECT file_path FROM surat_keluar WHERE id = $id");
    $row = mysqli_fetch_assoc($result);
    if (file_exists($row['file_path'])) {
        unlink($row['file_path']);
    }

    // Hapus dari database
    mysqli_query($conn, "DELETE FROM surat_keluar WHERE id = $id");
    header("Location: surat_keluar.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Surat Keluar</title>
    <link rel="stylesheet" href="css/index.css">
    <link rel="stylesheet" href="css/main.css">
</head>
<body>
    <?php include 'header.php'; ?>

    <main>
    <h2>Surat Keluar</h2>

    <!-- Form Tambahkan Surat -->
    <form method="POST" enctype="multipart/form-data">
        <label for="tanggal">Tanggal:</label>
        <input type="date" name="tanggal" required>

        <label for="pengirim">Pengirim:</label>
        <input type="text" name="pengirim" required>

        <label for="perihal">Perihal:</label>
        <input type="text" name="perihal" required>

        <label for="file">File (doc, xlsx, pdf):</label>
        <input type="file" name="file" accept=".doc,.xlsx,.pdf" required>

        <button type="submit" name="add_surat">Tambahkan Surat</button>
    </form>

    <!-- Tabel Surat Masuk -->
    <table>
        <thead>
            <tr>
                <th>No</th>
                <th>Tanggal</th>
                <th>Pengirim</th>
                <th>Perihal</th>
                <th>File</th>
                <th>Aksi</th>
            </tr>
        </thead>
        <tbody>
            <?php
            // Ambil data dari tabel surat_masuk
            $result = mysqli_query($conn, "SELECT * FROM surat_masuk");
            $no = 1;
            while ($row = mysqli_fetch_assoc($result)) {
                echo "<tr>";
                echo "<td>" . $no++ . "</td>";
                echo "<td>" . htmlspecialchars($row['tanggal_keluar']) . "</td>";
                echo "<td>" . htmlspecialchars($row['pengirim']) . "</td>";
                echo "<td>" . htmlspecialchars($row['perihal']) . "</td>";
                echo "<td><a href='" . $row['file_path'] . "' target='_blank'>Download</a></td>";
                echo "<td><a href='?delete_id=" . $row['id'] . "' onclick='return confirm(\"Yakin ingin menghapus surat ini?\");'>Hapus</a></td>";
                echo "</tr>";
            }
            ?>
        </tbody>
    </table>
</main>

<?php include 'footer.php'; ?>
</body>
</html>
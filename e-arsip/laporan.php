<?php
// Mulai sesi dan koneksi database
session_start();
include 'config.php';

// Default query tanpa filter
$query = "SELECT * FROM surat_masuk";

// Jika filter tanggal diterapkan
if (isset($_GET['start_date']) && isset($_GET['end_date'])) {
    $start_date = $_GET['start_date'];
    $end_date = $_GET['end_date'];

    // Pastikan tanggal valid
    if (!empty($start_date) && !empty($end_date)) {
        $query = "SELECT * FROM surat_masuk WHERE tanggal_masuk BETWEEN '$start_date' AND '$end_date'";
    }
}

// Format Date
if (!empty($start_date) && !empty($end_date)) {
    // Validasi format tanggal
    if (DateTime::createFromFormat('Y-m-d', $start_date) && DateTime::createFromFormat('Y-m-d', $end_date)) {
        $query = "SELECT * FROM surat_masuk WHERE tanggal_masuk BETWEEN '$start_date' AND '$end_date'";
    } else {
        die("Format tanggal tidak valid.");
    }
}


$result = mysqli_query($conn, $query);

if (!$result) {
    die("Query gagal: " . mysqli_error($conn));
}

?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laporan surat</title>
    <link rel="stylesheet" href="css/index.css">
</head>
<body>
    <?php include 'header.php'; ?>

<main>
<h2>Laporan Surat</h2>

<form method="GET" action="laporan.php">
    <label for="start_date">Tanggal Awal:</label>
    <input type="date" name="start_date" id="start_date" required>

    <label for="end_date">Tanggal Akhir:</label>
    <input type="date" name="end_date" id="end_date" required>

    <button type="submit">Filter</button>
</form>

<table border="1">
<thead>
        <tr>
            <th>No</th>
            <th>Tanggal</th>
            <th>Pengirim</th>
            <th>Penerima</th>
            <th>Perihal</th>
            <th>File</th>
            <th>Tipe Surat</th>
        </tr>
    </thead>
    <tbody>
    <?php
        if ($result && mysqli_num_rows($result) > 0) {
            $no = 1;
            while ($row = mysqli_fetch_assoc($result)) {
                echo "<tr>";
                echo "<td>" . $no++ . "</td>";
                echo "<td>" . htmlspecialchars($row['tanggal_masuk']) . "</td>";
                echo "<td>" . htmlspecialchars($row['pengirim']) . "</td>";
                echo "<td>" . htmlspecialchars($row['penerima']) . "</td>";
                echo "<td>" . htmlspecialchars($row['perihal']) . "</td>";
                echo "<td><a href='" . htmlspecialchars($row['file_path']) . "' target='_blank'>Download</a></td>";
                echo "<td>" . htmlspecialchars($row['tipe_surat']) . "</td>";
                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='5'>Tidak ada data ditemukan.</td></tr>";
        }
        
        ?>
    </tbody>
</table>
</main>

<?php include 'footer.php'; ?>
</body>
</html>
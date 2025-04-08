<?php 

if (!isset($_SESSION['logged_in'])) {
    header('Location: index.php');
    exit;
}

$username = $_SESSION['username'];
?>

<main>
    <h2>Selamat Datang, <?php echo htmlspecialchars($username); ?>!</h2>
    <p>Ini adalah dashboard utama aplikasi E-Arsip. Anda dapat mengelola surat masuk, surat keluar, dan melihat laporan dari menu navigasi di atas.</p>
    <div class="stats">
        <div class="stat-item">
            <h3>Total Surat Masuk</h3>
            <p>
                <?php
                $result = mysqli_query($conn, "SELECT COUNT(*) AS total FROM surat_masuk WHERE tipe_surat ='masuk'");
                $data = mysqli_fetch_assoc($result);
                echo $data['total'];
                ?>
            </p>
        </div>
        <div class="stat-item">
            <h3>Total Surat Keluar</h3>
            <p>
                <?php
                $result = mysqli_query($conn, "SELECT COUNT(*) AS total FROM surat_masuk WHERE tipe_surat ='keluar'");
                $data = mysqli_fetch_assoc($result);
                echo $data['total'];
                ?>
            </p>
        </div>
    </div>
</main>

<?php include 'footer.php'; ?>
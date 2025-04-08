<?php
session_start();
include 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 $username = mysqli_real_escape_string($conn, $_POST['username']);
 $password = mysqli_real_escape_string($conn, $_POST['password']);
 $konfirmasi_password = mysqli_real_escape_string($conn, $_POST['konfirmasi_password']);

 if ($password !== $konfirmasi_password) {
 $error_daftar = 'Password tidak cocok!';
 } else {
 $query = "INSERT INTO users (username, password) VALUES ('$username', MD5('$password'))";
 $result = mysqli_query($conn, $query);
 if ($result) {
 $success_daftar = 'Akun berhasil dibuat!';
 } else {
 $error_daftar = 'Gagal membuat akun!';
 }
 }
}
?>

<!DOCTYPE html>
<html>
<head>
  <title>Buat Akun</title>
  <link rel="stylesheet" href="css/daftar.css">
</head>
<body>
  <div class="container">
    <h2>Buat Akun</h2>
    <?php if (isset($error_daftar)) { echo '<p class="error">' . $error_daftar . '</p>'; } ?>
    <?php if (isset($success_daftar)) { echo '<p class="success">' . $success_daftar . '</p>'; } ?>
    <form method="POST">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" required>
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" required>
      <label for="konfirmasi_password">Konfirmasi Password:</label>
      <input type="password" id="konfirmasi_password" name="konfirmasi_password" required>
      <button type="submit">Buat Akun</button>
      <p>Sudah punya akun? <a href="login.php">Login</a></p>
    </form>
  </div>
</body>
</html>
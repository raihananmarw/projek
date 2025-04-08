<?php
session_start();
include 'config.php';

// Proses login
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $_POST['aksi'] === 'login') {
 $username = mysqli_real_escape_string($conn, $_POST['username']);
 $password = mysqli_real_escape_string($conn, $_POST['password']);
 $query = "SELECT * FROM users WHERE username = '$username' AND password = MD5('$password')";
 $result = mysqli_query($conn, $query);
 if (mysqli_num_rows($result) === 1) {
 $_SESSION['logged_in'] = true;
 $_SESSION['username'] = $username;
 header('Location: index.php');
 exit;
 } else {
 $error = 'Username atau password salah!';
 }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Login - E-Arsip Aria Kamuning</title>
 <link rel="stylesheet" href="css/login.css">
</head>
<body>
 <div class="login-container">
 <h2>Login</h2>
 <?php if (isset($error)) { echo '<p style="color: red;">' . $error . '</p>'; } ?>
 <form method="POST">
 <label for="username">Username:</label>
 <input type="text" id="username" name="username" required><br>
 <label for="password">Password:</label>
 <input type="password" id="password" name="password" required><br>
 <button type="submit" name="aksi" value="login">Login</button>
 <p>Belum punya akun? <a href="daftar.php">Buat Akun</a></p>
 </form>
 </div>
</body>
</html>
<?php
$db = new mysqli('localhost', 'root', '1234', 'web_canciones');

if ($db->connect_error) {
    die('Error de conexión: ' . $db->connect_error);
}

$email_posted = trim($_POST['f_email']);
$password_posted = trim($_POST['f_password']);

$query = $db->prepare("SELECT id, contraseña FROM tUsuarios WHERE email = ?");
$query->bind_param("s", $email_posted);
$query->execute();
$result = $query->get_result();

if ($result->num_rows > 0) {
    $only_row = $result->fetch_assoc();

    if (password_verify($password_posted, $only_row['contraseña'])) {
        session_start();
        $_SESSION['user_id'] = $only_row['id'];
        header('Location: main.php');
        exit;
    } else {
        echo '<p>Contraseña incorrecta</p>';
    }
} else {
    echo '<p>Usuario no encontrado con ese email</p>';
}

$db->close();
?>

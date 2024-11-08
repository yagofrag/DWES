<?php
// Conexión a la base de datos
$db = new mysqli('localhost', 'usuario', 'contraseña', 'mysitedb');

// Comprobar conexión
if ($db->connect_error) {
    die("Error de conexión: " . $db->connect_error);
}

// Validar datos del formulario
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = trim($_POST['email']);
    $password = trim($_POST['password']);
    $confirm_password = trim($_POST['confirm_password']);

    // Verificar campos vacíos
    if (empty($email) || empty($password) || empty($confirm_password)) {
        echo "Todos los campos son obligatorios.";
        exit;
    }

    // Verificar si las contraseñas coinciden
    if ($password !== $confirm_password) {
        echo "Las contraseñas no coinciden.";
        exit;
    }

    // Comprobar si el correo ya existe en la base de datos
    $query = $db->prepare("SELECT id FROM tUsuarios WHERE email = ?");
    $query->bind_param("s", $email);
    $query->execute();
    $result = $query->get_result();

    if ($result->num_rows > 0) {
        echo "El correo electrónico ya está registrado.";
        exit;
    }

    // Cifrar la contraseña
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Insertar el nuevo usuario en la base de datos
    $insert = $db->prepare("INSERT INTO tUsuarios (email, password) VALUES (?, ?)");
    $insert->bind_param("ss", $email, $hashed_password);

    if ($insert->execute()) {
        // Redirigir a la página principal
        header("Location: index.php");
        exit;
    } else {
        echo "Error al registrar el usuario.";
    }
}

// Cerrar la conexión
$db->close();
?>

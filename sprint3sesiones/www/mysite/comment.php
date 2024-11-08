<?php
session_start();
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
?>

<html>
<body>
<?php
// Verificar si el usuario está logueado
if (!isset($_SESSION['user_id'])) {
    echo '<p>Debes iniciar sesión para comentar.</p>';
    echo "<a href='/login.html'>Iniciar sesión</a>";
    exit;
}

$usuario_id = $_SESSION['user_id'];
$juego_id = mysqli_real_escape_string($db, $_POST['juego_id']);
$comentario = mysqli_real_escape_string($db, $_POST['new_comment']);

// Preparar la consulta para insertar el comentario
$query = "INSERT INTO tComentarios (comentario, juego_id, usuario_id) VALUES ('$comentario', $juego_id, $usuario_id)";

// Ejecutar la consulta e informar del resultado
if (mysqli_query($db, $query)) {
    echo "<p>Nuevo comentario con ID " . mysqli_insert_id($db) . " añadido</p>";
} else {
    echo "<p>Error: " . mysqli_error($db) . "</p>";
}

// Enlace para volver al detalle del juego
echo "<a href='/detail.php?id=".$juego_id."'>Volver</a>";

// Cerrar conexión
mysqli_close($db);
?>
</body>
</html>

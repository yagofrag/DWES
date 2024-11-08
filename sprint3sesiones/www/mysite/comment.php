
<?php
// Conectar a la base de datos
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
?>
<html>
<body>
<?php
// Recoger datos del formulario
$juego_id = $_POST['juego_id'];
$comentario = $_POST['new_comment'];

// Escapar las variables para prevenir inyección de SQL
$juego_id = mysqli_real_escape_string($db, $juego_id);
$comentario = mysqli_real_escape_string($db, $comentario);

// Preparar la consulta
$query = "INSERT INTO tComentarios(comentario, juego_id, usuario_id)
          VALUES ('$comentario', $juego_id, NULL)";

// Ejecutar la consulta
if (mysqli_query($db, $query)) {
    echo "<p>Nuevo comentario ";
    echo mysqli_insert_id($db);
    echo " añadido</p>";
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




<?php
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
?>
<html>
<body>
<?php
session_start();
$user_id_a_insertar = 'NULL';
if (!empty($_SESSION['user_id'])) {
    $user_id_a_insertar = $_SESSION['user_id'];
}

$juego_id = mysqli_real_escape_string($db, $_POST['juego_id']);
$comentario = mysqli_real_escape_string($db, $_POST['new_comment']);

$query = "INSERT INTO tComentarios (comentario, juego_id, usuario_id) 
          VALUES ('".$comentario."', ".$juego_id.", ".$user_id_a_insertar.")";
          
if (mysqli_query($db, $query)) {
    echo "<p>Nuevo comentario " . mysqli_insert_id($db) . " añadido</p>";
} else {
    echo "<p>Error: " . mysqli_error($db) . "</p>";
}

echo "<a href='/detail.php?id=".$juego_id."'>Volver</a>";
mysqli_close($db);
?>
</body>
</html>

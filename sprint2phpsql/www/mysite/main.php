<?php
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
?>
<html>
<body>
<h1>Conexión establecida</h1>
<?php
// Lanzar una query
$query = 'SELECT * FROM tJuegos';
$result = mysqli_query($db, $query) or die('Query error');

// Recorrer el resultado
while ($row = mysqli_fetch_array($result)) {
 




  echo '<div>';
    echo '<h2>' . $row['nombre'] . '</h2>';
    if (@getimagesize($row['url_imagen'])) { // Comprobar si la imagen existe
        echo '<img src="' . $row['url_imagen'] . '" alt="' . $row['nombre'] . '" width="200">';
    } else {
        echo '<p>Imagen no disponible</p>'; // Mostrar un mensaje si la imagen no se carga
    }
    echo '<p>Descripción: ' . $row['descripcion'] . '</p>';
    echo '<p>Género: ' . $row['genero'] . '</p>';
    echo '<a href="detail.php?id=' . $row['id'] . '">Ver Detalles</a>';
    echo '</div><hr>';
}
mysqli_close($db);

?>
</body>
</html>

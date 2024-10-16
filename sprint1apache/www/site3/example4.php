<html>
<body>
<h1>Jubilación</h1>
<?php

$X = 7;


$edad = isset($_GET['edad']) ? intval($_GET['edad']) : 0; // Edad por defecto 0 si no se proporciona

function edad_en_X_años($edad, $X) {
    return $edad + $X; 
}

function mensaje($edad_futura, $jubilacion = 65) {
    if ($edad_futura >= $jubilacion) {
        return "En ". 65-($edad_futura-7) .  " años tendrás edad de jubilación."; // Mensaje si ya estás jubilado
    } else {
        return "¡Disfruta de tu tiempo!"; // Mensaje si no estás jubilado
    }
}

?>
<table border="1">
<tr>
<th>Edad Actual</th>
<th>Info</th>
</tr>
<?php
// Generar la lista de edades desde la edad actual hasta 65
for ($i = $edad; $i <= 65; $i++) {
    $edad_futura = edad_en_X_años($i, $X); // Calcular la edad futura
    echo "<tr>";
    echo "<td>".$i."</td>";
    echo "<td>".mensaje($edad_futura)."</td>"; // Llamar a la función de mensaje
    echo "</tr>";
}
?>
</table>
</body>
</html>

<html>
<body>
<h1>Calculadora</h1>
<p>Introduce dos números y selecciona la operación deseada:</p>
<form action="calculadora.php" method="post">
    <label for="numero1">Número 1:</label>
    <input type="number" id="numero1" name="numero1" step="any" required><br><br>
    <label for="numero2">Número 2:</label>
    <input type="number" id="numero2" name="numero2" step="any" required><br><br>
    <label for="operacion">Operación:</label>
    <select id="operacion" name="operacion">
        <option value="suma">Suma</option>
        <option value="resta">Resta</option>
        <option value="multiplicacion">Multiplicación</option>
        <option value="division">División</option>
    </select><br><br>
    <input type="submit" value="Calcular">
</form>

<p>Resultado:</p>
<p>
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $numero1 = $_POST["numero1"];
    $numero2 = $_POST["numero2"];
    $operacion = $_POST["operacion"];
    $resultado = "";

    switch ($operacion) {
        case "suma":
            $resultado = $numero1 + $numero2;
            echo "La suma de $numero1 y $numero2 es: $resultado";
            break;
        case "resta":
            $resultado = $numero1 - $numero2;
            echo "La resta de $numero1 y $numero2 es: $resultado";
            break;
        case "multiplicacion":
            $resultado = $numero1 * $numero2;
            echo "La multiplicación de $numero1 y $numero2 es: $resultado";
            break;
        case "division":
            if ($numero2 != 0) {
                $resultado = $numero1 / $numero2;
                echo "La división de $numero1 entre $numero2 es: $resultado";
            } else {
                echo "Error: No se puede dividir por cero.";
            }
            break;
        default:
            echo "Operación no válida.";
    }
}
?>
</p>
</body>
</html>

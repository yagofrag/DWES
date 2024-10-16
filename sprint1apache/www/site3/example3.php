<html>
<body>
<h1>Jubilación</h1>
<?php
$edad = isset($_GET['edad']) ? intval($_GET['edad']) : 0;
function edad_en_10_años($edad) {
return $edad + 10;
}
if (edad_en_10_años($edad) > 65) {
echo "En 10 años tendrás edad de jubilación";
} else {
echo "¡Disfruta de tu tiempo!";
}
?>
</body>
</html>

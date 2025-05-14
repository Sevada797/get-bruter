<?php 
$a = $_GET["a"] ?? "";
$b = $_GET["b"] ?? "";
$c = $_GET["c"] ?? "";


var_dump($_GET);
echo "<br>reflecting once param a value: " . $a."<br>";
echo "reflecting twice param b value: " . $b . " " . $b;
setcookie("testcookie", $c, 0, "/");




?>

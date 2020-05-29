<?php
$data = $_POST["data"];
$write = "$data";
file_put_contents('fileContainer.php', $write);
//$fp = fopen('fileContainer.php', 'a');//opens file in append mode
//echo "File appended successfully";
//fwrite($fp, $write);
//fclose($fp);
file_put_contents('sendRequest.php', "");
?>
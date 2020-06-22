<?php
$data = $_POST["data"];
$write = "$data";
if ($data == "OKE") {
    $output = shell_exec("python python/test.py");
    file_put_contents('status.php', $write);
    file_put_contents('dataContainer.php', "");
} else {
//file_put_contents('dataContainer.php', $write);
    $fp = fopen('dataContainer.php', 'a');//opens file in append mode
//echo "File appended successfully";
    fwrite($fp, $write);
//fclose($fp);
}

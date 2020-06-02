<?php
$data = $_POST["data"];
$write = "$data";
if ($data == "OKE") {
    file_put_contents('status.php', $write);
} else {
//file_put_contents('dataContainer.php', $write);
    $fp = fopen('dataContainer.php', 'a');//opens file in append mode
//echo "File appended successfully";
    fwrite($fp, $write);
//fclose($fp);
}

file_put_contents('sendRequest.php', "");


//$data = $_POST["data"];
//$write = "$data";
//file_put_contents('dataContainer.php', $write);
//
//file_put_contents('sendRequest.php', "");
?>
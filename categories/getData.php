<?php
$data = $_POST["data"];
$write = "$data";
if ($data == "OKE") {
    file_put_contents('status.php', $write);
} else {
    $fp = fopen('dataContainer.php', 'a');//opens file in append mode
    fwrite($fp, $write);
}

file_put_contents('sendRequest.php', "");

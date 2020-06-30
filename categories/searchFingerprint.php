<?php

include "database\connect.php";
$data = $_POST["data"];
$write = "$data";

if ($data == "OKE") {
    $output = shell_exec("python python/fingerprint.py");
    $write = "$output";
    file_put_contents('dataContainer.php', "");
    file_put_contents('matchResult.php', $write);

} else {
    file_put_contents('sendRequest.php', "");
    $fp = fopen('dataContainer.php', 'a');//opens file in append mode
    fwrite($fp, $write);
}


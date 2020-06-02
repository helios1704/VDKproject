<?php
include "database\connect.php";
$data = $_POST["data"];
$write = "$data";

if ($data == "OKE") {
    //file_put_contents('status.php', $write);
    file_put_contents('matchResult.php', "0-0");
    //file_put_contents('dataContainer.php', $write);
    //while ($data = file_get_contents("status.php") == "") ;
    shell_exec("python python/convertToImage.py");
    shell_exec("python python/extractMinutiae1.py");
    $output = shell_exec("python python/matchFingerprint.py");
    $write = "$output";
    file_put_contents('matchResult.php', $write);
    date_default_timezone_set('Asia/Ho_Chi_Minh');
    $user_id = (int)substr($output, 2);
    $now = date("Y/m/d H:i:s");
    $sql = "INSERT INTO histories(user_id, time) VALUES ($user_id, '$now')";
    $statement = $conn->prepare($sql);
    $statement->execute();
    //file_put_contents('sendRequest.php', "");
    file_put_contents('dataContainer.php', "");
} else {
//file_put_contents('dataContainer.php', $write);
    $fp = fopen('dataContainer.php', 'a');//opens file in append mode
//echo "File appended successfully";
    fwrite($fp, $write);
//fclose($fp);
}

//file_put_contents('status.php', "");

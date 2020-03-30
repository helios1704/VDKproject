<?php
$servername = "127.0.0.1";
$dbname = "vdkproject";

try {
    $conn = new PDO("mysql:host=$servername; dbname=$dbname", "root", "");
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "Connection successfully " ;
    $conn->exec("set names utf8");  //Tiếng Việt
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
    die;
}

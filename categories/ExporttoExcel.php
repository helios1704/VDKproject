<?php
include "database/connect.php";
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
$sql_query = "SELECT histories.*, users.name FROM histories LEFT JOIN users ON histories.user_id = users.id ORDER BY histories.id DESC";
$statement = $conn->prepare($sql_query);
$statement->setFetchMode(PDO::FETCH_ASSOC);
$statement->execute();
$row = $statement->fetchAll();

$tab = "\t";
$file_ending = "xls";
//header info for browser
header("Content-Type: application/xls");
header("Content-Disposition: attachment; filename=histories.xls");
header("Pragma: no-cache");
header("Expires: 0");
$schema_insert = "";
$schema_insert = "ID" . $tab . "USER ID" . $tab . "NAME" . $tab . "TIME"."\n";
echo $schema_insert;
$schema_insert = "";
foreach ($row as $k => $v) {
    $v['user_id'] == 0 ? $v['name'] = "Anonymous" : 1;
    $id = $v['id'];
    $user_id = $v['user_id'];
    $name = $v['name'];
    $time = $v['time'];
    $schema_insert .= "$id" . $tab;
    $schema_insert .= "$user_id" . $tab;
    $schema_insert .= "$name" . $tab;
    $schema_insert .= "$time" . $tab;
    $schema_insert .= "\n";
    echo $schema_insert;
    $schema_insert = "";
}
//$schema_insert = str_replace($tab . "$", "", $schema_insert);
//$schema_insert = preg_replace("/\r\n|\n\r|\n|\r/", " ", $schema_insert);
//$schema_insert .= "\t";
print(trim($schema_insert));
print "\n";



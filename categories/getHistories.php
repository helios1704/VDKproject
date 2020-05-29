<?php
include "database/connect.php";
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
$sql_query = "SELECT histories.*, users.name FROM histories LEFT JOIN users ON histories.user_id = users.id";
$statement = $conn->prepare($sql_query);
$statement->setFetchMode(PDO::FETCH_ASSOC);
$statement->execute();
$row = $statement->fetchAll();
//$userData = array();

foreach ($row as $k => $v) {
    $v['user_id'] == 0 ? $v['name'] = "Anonymous" : 1;
    $userData[] = array(
        'id' => $v['id'],
        'user_id' => $v['user_id'],
        'name' => $v['name'],
        'time' => date("H:i:s d/m/Y", strtotime($v['time'])),
        'action' => '<button style="padding: 4px 4px" type="button" name="edit" id="' . $v["id"] . '" class="btn btn-warning btn-xs edit">Edit</button>|' .
            '<button style="padding: 4px 4px" type="button" name="delete" id="' . $v["id"] . '" class="btn btn-danger btn-xs delete" >Delete</button>',
    );
}
$output = array(
    "data" => $userData
);
echo json_encode($output);
<?php
include "database/connect.php";
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
$sql_query = "SELECT * FROM users";
$statement = $conn->prepare($sql_query);
$statement->setFetchMode(PDO::FETCH_ASSOC);
$statement->execute();
$row = $statement->fetchAll();

foreach ($row as $k => $v) {
    if ($v['gender'] == 1) {
        $gender = "Male";
    }
    if ($v['gender'] == 2) {
        $gender = "Female";
    }
    if ($v['gender'] == 3) {
        $gender = "Another";
    }
    $userData[] = array(
        'id' => $v['id'],
        'name' => $v['name'],
        'birthday' => date("d/m/Y", strtotime($v['birthday'])),
        'gender' => $gender,
        'created_at' => date("H:i:s d/m/Y", strtotime($v['created_at'])),
        'action' => '<button style="padding: 4px 4px" type="button" name="delete" id="' . $v["id"] . '" class="btn btn-danger btn-xs delete" >Delete</button>',
//        'action' => '<button style="padding: 4px 4px" type="button" name="edit" id="' . $v["id"] . '" class="btn btn-warning btn-xs edit">Edit</button>|' .
//            '<button style="padding: 4px 4px" type="button" name="delete" id="' . $v["id"] . '" class="btn btn-danger btn-xs delete" >Delete</button>',
    );
}
$output = array(
    "data" => $userData
);
//print_r($output);
echo json_encode($output);
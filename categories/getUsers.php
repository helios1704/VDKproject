<?php
include "database/connect.php";
$sql_query = "SELECT * FROM users";
$statement = $conn->prepare($sql_query);
$statement->setFetchMode(PDO::FETCH_ASSOC);
$statement->execute();
$row = $statement->fetchAll();
$userData = array();
foreach ($row as $k => $v) {
    $empRows = array();
    $empRows[]=  $v['id'];
    $empRows[]=  $v['name'];
    $empRows[]=  date("d/m/Y", strtotime($v['birthday']));
    if ($v['gender'] == 1)  {
        $empRows[]="Male";
    }
    if ($v['gender'] == 2)  {
        $empRows[]="Female";
    }
    if ($v['gender'] == 3)  {
        $empRows[]="Another";
    }
    $empRows[]=  $v['fingerprint'];
    $empRows[]=  $v['created_at'];
    $empRows[]=  $v['updated_at'];
    $empRows[] = '<button style="padding: 4px 4px" type="button" name="edit" id="'.$v["id"].'" class="btn btn-warning btn-xs edit">Edit</button>';
    $empRows[] = '<button style="padding: 4px 4px" type="button" name="delete" id="'.$v["id"].'" class="btn btn-danger btn-xs delete" >Delete</button>';
    $userData[] = $empRows;
}
$output = array(
    "draw"				=>	intval($_POST["draw"]),
    "data"    			=> 	$userData
);
echo json_encode($output);
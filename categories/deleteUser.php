<?php
include "database/connect.php";
if(isset($_POST['empId'])) {
    $empId = $_POST['empId'];
    $sql = "DELETE FROM users WHERE id = $empId";
    $statement = $conn->prepare($sql);
    $statement->execute();
}

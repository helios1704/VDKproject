<?php
include "database/connect.php";
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
if(isset($_POST['empId'])) {
    $empId = $_POST['empId'];
    $sql = "DELETE FROM users WHERE id = $empId";
    $statement = $conn->prepare($sql);
    $statement->execute();
}

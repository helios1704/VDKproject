<?php
include "database/connect.php";
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
if (isset($_POST['empId'])) {
    $empId = $_POST['empId'];
    $sql = "DELETE FROM histories WHERE user_id = $empId";
    $statement = $conn->prepare($sql);
    $statement->execute();
    $sql1 = "DELETE FROM users WHERE id = $empId";
    $statement = $conn->prepare($sql1);
    $statement->execute();
}

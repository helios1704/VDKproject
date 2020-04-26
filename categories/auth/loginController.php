<?php
session_start();
include "../database/connect.php";
if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = md5($_POST['password']);
    $query = "SELECT * FROM admins WHERE username='$username' AND password='$password'";
    $statement = $conn->prepare($query);
    $statement->setFetchMode(PDO::FETCH_ASSOC);
    $statement->execute();
    $row = $statement->fetchAll();
    if ($row != null) {
        $_SESSION['username'] = $username;
     //   print_r($_SESSION) ;
        header("Location: ../index.php");
    }
    else {
        header("Location: login.php");
    }
}
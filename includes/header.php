<?php session_start();
?>

<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="stylesheet" href="../assets/css/bootstrap.css">

    <!-- <script src="../assets/js/bootstrap.js"></script> -->
    <!--    <script src="../assets/js/jquery.min.js"></script>-->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/dt-1.10.16/datatables.min.css"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/v/dt/dt-1.10.16/datatables.min.js"></script>
    <title>Document</title>
</head>
<body>
<div class="container">
    <div class="d-flex" style="margin-bottom: 15px">
        <img class="" src="../assets/img/logo.png">
        <h1>Microprocessor Project</h1>
    </div>
    <div class="topnav d-flex">
        <div style="width: 80%">
            <ul class="">
                <li><a href="index.php" class="<?php echo($_SERVER['PHP_SELF'] == "/VDKproject/categories/index.php" ? "active" : ""); ?>">Home</a></li>
                <li><a href="users.php" class="<?php echo($_SERVER['PHP_SELF'] == "/VDKproject/categories/users.php" ? "active" : ""); ?>">Users</a></li>
                <li><a href="createUser.php" class="<?php echo($_SERVER['PHP_SELF'] == "/VDKproject/categories/createUser.php" ? "active" : ""); ?>">Create User</a></li>
                <li><a href="searchuser.php" class="<?php echo($_SERVER['PHP_SELF'] == "/VDKproject/categories/searchuser.php" ? "active" : ""); ?>">Search User</a></li>
            </ul>
        </div>
        <div style="width: 20%" class="admin">
            <ul class="">
                <li><a href="#">Admin: <?php if(isset($_SESSION['username']))echo $_SESSION['username']?></a></li>
                <li><a href="../categories/auth/logout.php" >Logout</a></li>
            </ul>
        </div>
    </div>
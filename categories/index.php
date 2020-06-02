<?php
//die($_SERVER['PHP_SELF']);
include "../includes/header.php";
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
?>
<img src="../assets/img/dut.png" style="width: 100%; height:495px">
<?php include "../includes/footer.php"; ?>

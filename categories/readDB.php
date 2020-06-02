<?php include "database/connect.php";
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
$file = "";
if (isset($_GET['file'])) {
    $file = $_GET['file'];
}
$sql = "SELECT * FROM users WHERE fingerprint='$file'";
$statement = $conn->prepare($sql);

$statement->execute();
$data = $statement->fetch(PDO::FETCH_ASSOC);

file_put_contents('temp.php', "");
file_put_contents('dataContainer.php', "");
file_put_contents('sendRequest.php', "");

?>
<div class="container"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<link rel="stylesheet" href="../assets/css/bootstrap.css">
<link rel="stylesheet" href="../assets/css/searchUser.css">
<div>
    <form>
        <table class="frame" cellpadding="0" cellspacing="1">
            <tr>
                <td style="height: 40%; background-color:#4CAF50; padding: 5px;">
                    <h5 style="text-align: center"><b>User Data</b></h5>
                </td>
            </tr>
            <tr>
                <td bgcolor="#f9f9f9">
                    <table class="data" cellpadding="15" cellspacing="0">
                        <tr class="">
                            <td style="width: 20%">ID</td>
                            <td style="width: 20%;font-weight:bold">:</td>
                            <td style="width: 30%"><?php
                                if ($data['id'] != null) echo $data['id'];
                                else echo "--------" ?></td>
                        </tr>
                        <tr bgcolor="#f2f2f2">
                            <td>Name</td>
                            <td style="font-weight:bold">:</td>
                            <td><?php
                                if ($data['id'] != null) echo $data['name'];
                                else echo "--------"; ?>
                            </td>
                        </tr>
                        <tr>
                            <td>Gender</td>
                            <td style="font-weight:bold">:</td>
                            <td><?php if ($data['id'] != null) {
                                    if ($data['gender'] == 1) echo "Male";
                                    elseif ($data['gender'] == 2) echo "Female";
                                    else echo "Another";
                                } else echo "--------"; ?></td>
                        </tr>
                        <tr bgcolor="#f2f2f2">
                            <td>Birthday</td>
                            <td style="font-weight:bold">:</td>
                            <td><?php if ($data['id'] != null) {
                                    $t = strtotime($data['birthday']);
                                    echo date('d/m/Y', $t);
                                } else echo "--------"; ?>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </form>
</div>
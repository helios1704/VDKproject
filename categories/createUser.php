<?php
include "../includes/header.php";
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
include "database/connect.php";
?>

<?php if (isset($_GET['request'])) {
    $request = $_GET['request'];
    $write = "<?php $" . "request='" . $request . "'; " . "echo $" . "request;" . " ?>";
    file_put_contents('sendRequest.php', $write);
}

$fingerImage = file_get_contents("fileContainer.php");
date_default_timezone_set('Asia/Ho_Chi_Minh');
if (isset($_POST['submit'])) {
    $name = $_POST['name'];
    $gender = $_POST['gender'];
    $birthday = $_POST['birthday'];
    $created_at = date("Y/m/d H:i:s");
    $sql = "INSERT INTO users(name, birthday, gender, fingerprint, created_at) VALUES ('$name', '$birthday', $gender, '$fingerImage','$created_at')";
    $statement = $conn->prepare($sql);
    $statement->execute();
    file_put_contents('temp.php', "");
    file_put_contents('fileContainer.php', "");
    file_put_contents('sendRequest.php', "");
    header("Location: users.php");
}
?>

<script>
    $(document).ready(function () {
        setInterval(function () {

        setInterval(function () {
            $("#command2").load("temp.php");
        }, 500);
        $("#btnRequest").click(function () {
            $.ajax({
                type: 'get',
                url: 'createUser.php',
                data: {request: 'create'},
                success: function (data) {
                    alert("SI");
                    $("#command").html("Put your finger on sensor!");
                }
            });
        });
    });
</script>
<link rel="stylesheet" href="../assets/css/createUser.css">

<form action="" method="post">
    <div class="container-sm" style="width: 75%; margin-top: 20px">
        <label for="name"><b>Name</b></label>
        <input type="text" placeholder="Enter Name" name="name" required>

        <label for="birthday"><b>Birthday</b></label>
        <input type="date" placeholder="" name="birthday" required>

        <label for="gender" style="margin-right: 10px; margin-top: 5px"><b>Gender</b></label>

        <div class="custom-control custom-radio custom-control-inline">
            <input type="radio" class="custom-control-input" id="Male" name="gender" value="1" checked>
            <label class="custom-control-label" for="Male">Male</label>
        </div>
        <div class="custom-control custom-radio custom-control-inline">
            <input type="radio" class="custom-control-input" id="Female" name="gender" value="2">
            <label class="custom-control-label" for="Female">Female</label>
        </div>
        <div class="custom-control custom-radio custom-control-inline">
            <input type="radio" class="custom-control-input" id="Another" name="gender" value="3">
            <label class="custom-control-label" for="Another">Another</label>
        </div>
        <br>
        <label for="fingerprint" class="text-danger" style="margin-right: 20px"><b>Push this button to insert your fingerprint</b></label>
        <button type="button" class="btn btn-danger" id="btnRequest">Bấm</button>
        <br>
        <b><label for="" id="command" class="text-warning"></label></b>
        <b><label for="" id="command2" class="text-warning"></label></b>
        <br>
        <button type="submit" class="registerbtn" name="submit">Create</button>
    </div>
</form>

<?php include "../includes/footer.php"; ?>

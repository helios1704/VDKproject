<?php
include "../includes/header.php";
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
include "database/connect.php";
?>

<?php
if (isset($_GET['request'])) {
    $request = $_GET['request'];
    $write = "<?php $" . "request='" . $request . "'; " . "echo $" . "request;" . " ?>";
    file_put_contents('sendRequest.php', $write);
    while ($data = file_get_contents("status.php") != "OKE") ;
    $output = shell_exec("python python/convertToImage.py");
    file_put_contents('dataContainer.php', "");
    file_put_contents('status.php', "");
    file_put_contents('sendRequest.php', "");
}
date_default_timezone_set('Asia/Ho_Chi_Minh');
if (isset($_POST['submit'])) {
    $name = $_POST['name'];
    $gender = $_POST['gender'];
    $birthday = $_POST['birthday'];
    $created_at = date("Y/m/d H:i:s");
    $sql = "INSERT INTO users(name, birthday, gender, created_at) VALUES ('$name', '$birthday', $gender,'$created_at')";
    $statement = $conn->prepare($sql);
    $statement->execute();

    $sql = "SELECT max(id) as id FROM users";
    $statement = $conn->prepare($sql);
    $statement->setFetchMode(PDO::FETCH_ASSOC);
    $statement->execute();
    $row = $statement->fetchAll();
    $write = (int)$row[0]['id'];
    file_put_contents('fingerprintTemp/id_temp.txt', "$write");
    $output = shell_exec("python python/extractMinutiae.py");
    header("Location: users.php");
}
?>

<script>
    $(document).ready(function () {
        $("#btnRequest").click(function () {
            $("#command").html("Place your finger on the sensor!");
            $.ajax({
                type: 'get',
                url: 'createUser.php',
                data: {request: 'create'},
                success: function (data) {
                    d = new Date();
                    alert("Oke - DONE!");
                    $("#command").html("");
                    $("#fingerprint_data").attr("hidden", false);
                    $("#fingerprint_img").attr("src", "fingerprintTemp/temp.jpg?" + d.getTime());
                }
            });
        });
    });
</script>
<link rel="stylesheet" href="../assets/css/createUser.css">
<div class="d-flex" style="margin-top: 30px">
    <div class="" id="fingerprint_data" hidden>
        <img src='' id='fingerprint_img'>
    </div>
    <div class="container">
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
                <label for="fingerprint" class="text-danger" style="margin-right: 20px"><b>Click this button to insert
                        your fingerprint</b></label>
                <button type="button" class="btn btn-danger" id="btnRequest">Click!</button>
                <br>
                <b><label for="" id="command" class="text-warning"></label></b>
                <br>
                <button type="submit" class="registerbtn" name="submit">Create</button>
            </div>
        </form>
    </div>
</div>

<?php include "../includes/footer.php"; ?>

<?php include "../includes/header.php";
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
} ?>

<?php if (isset($_GET['request'])) {
    file_put_contents('matchResult.php', "0-0");
    $request = $_GET['request'];
    $write = "<?php $" . "request='" . $request . "'; " . "echo $" . "request;" . " ?>";
    file_put_contents('sendRequest.php', $write);
    $user_id = file_get_contents('matchResult.php');
    while (substr($user_id, 0, 1) != "1" && substr($user_id, 0, 1) != "2") {
        $user_id = file_get_contents('matchResult.php');
    }
}

?>
    <script>
        $(document).ready(function () {
            $("#btnRequest").click(function () {
                setInterval(function () {
                    //alert("DONE!");
                    $("#show_user_data").load("readDB.php");
                }, 50);
                $("#command").html("Place your finger on the sensor!");
                $.ajax({
                    type: 'get',
                    url: 'searchUser.php',
                    data: {request: 'search'},
                    success: function (data) {
                        // if ($("#user_id").text() == "--------") {
                            $("#command").html("");
                        // } else {
                        //
                        //     $("#command").html("Anonymous");
                        // }
                    }
                });
            });
        });
    </script>
    <link rel="stylesheet" href="../assets/css/searchUser.css">
    <div id="show_user_data" class="container-sm" style="width: 60%; margin-top: 20px">
        <form>
            <table class="frame" cellpadding="0" cellspacing="1">
                <tr>
                    <td style="height: 40%; background-color:#4CAF50;padding: 5px;">
                        <h5 style="text-align: center"><b>User Data</b></h5>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="#f9f9f9">
                        <table class="data" cellpadding="15" cellspacing="0">
                            <tr class="">
                                <td style="width:20%">ID</td>
                                <td style="width:20%; font-weight:bold">:</td>
                                <td style="width:30%" id="user_id">--------</td>
                            </tr>
                            <tr bgcolor="#f2f2f2">
                                <td>Name</td>
                                <td style="font-weight:bold">:</td>
                                <td>--------</td>
                            </tr>
                            <tr>
                                <td>Gender</td>
                                <td style="font-weight:bold">:</td>
                                <td>--------</td>
                            </tr>
                            <tr bgcolor="#f2f2f2">
                                <td>Birthday</td>
                                <td style="font-weight:bold">:</td>
                                <td>--------</td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </form>
    </div>
    <div style="margin-top: 10px">
        <button style=" margin: 0 25%; width: 50%" type="button" class="btn btn-success"
                id="btnRequest">Click this button to insert
            your fingerprint
        </button>
        <div id="toggle" style="margin: 0 25%; text-align: center">
            <b><label for="" id="command" class="text-warning"></label></b>
        </div>
    </div>

<?php include "../includes/footer.php"; ?>
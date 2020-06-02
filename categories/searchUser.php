<?php include "../includes/header.php";
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
} ?>

<?php if (isset($_GET['request'])) {
    $request = $_GET['request'];
    $write = "<?php $" . "request='" . $request . "'; " . "echo $" . "request;" . " ?>";
    file_put_contents('sendRequest.php', $write);
} ?>
    <script>
        $(document).ready(function () {
            $("#getFile").load("dataContainer.php");
            setInterval(function () {
                $("#getFile").load("dataContainer.php");
            }, 500);

            setInterval(function () {
                $("#command2").load("temp.php");
            }, 500);
            $("#btnRequest").click(function () {

                $.ajax({
                    type: 'get',
                    url: 'searchUser.php',
                    data: {request: 'search'},
                    success: function (data) {
                        // alert("SI");
                        $("#toggle").attr("hidden", false);
                        $("#command").html("Put your finger on sensor!");
                    }
                });
            });
        });
    </script>
    <link rel="stylesheet" href="../assets/css/searchUser.css">
    <p id="getFile" hidden></p>
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
                                <td style="width:30%">--------</td>
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
                id="btnRequest">Click button to insert Fingerprint
        </button>
        <div id="toggle" hidden style="margin: 0 25%; text-align: center">
            <b><label for="" id="command" class="text-warning"></label></b>
        </div>
    </div>
    <script>
        var myVar = setInterval(myTimer, 500);
        var myVar1 = setInterval(myTimer1, 500);
        var oldID = "";
        clearInterval(myVar1);

        function myTimer() {
            var getFile = document.getElementById("getFile").innerHTML;
            oldID = getFile;
            if (getFile != "") {
                myVar1 = setInterval(myTimer1, 500);
                showUser(getFile);
                clearInterval(myVar);
            }
        }

        function myTimer1() {
            var getFile = document.getElementById("getFile").innerHTML;
            if (oldID != getFile) {
                myVar = setInterval(myTimer, 500);
                clearInterval(myVar1);
            }
        }

        function showUser(str) {
            if (str == "") {
                document.getElementById("show_user_data").innerHTML = "";
                return;
            } else {
                if (window.XMLHttpRequest) {
                    // code for IE7+, Firefox, Chrome, Opera, Safari
                    xmlhttp = new XMLHttpRequest();
                } else {
                    // code for IE6, IE5
                    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
                }
                xmlhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        document.getElementById("show_user_data").innerHTML = this.responseText;
                        $("#toggle").attr("hidden", true);
                    }
                };
                xmlhttp.open("GET", "readDB.php?file=" + str, true);
                xmlhttp.send();
            }
        }
    </script>

<?php include "../includes/footer.php"; ?>
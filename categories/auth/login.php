<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="../../assets/css/login.css">
    <link rel="stylesheet" href="../../assets/css/bootstrap.css">
</head>
<body>
<div class="container" style="width: 25%; height: 30%; margin-top: 10%">
    <h3 style="text-align: center; margin-bottom: 30px">Login Form</h3>
    <form action="loginController.php" method="post">
        <div class="container">
            <label for="uname" style="padding-top:20px "><b>Username</b></label>
            <input type="text" placeholder="Enter Username" name="username" required>

            <label for="psw"><b>Password</b></label>
            <input type="password" placeholder="Enter Password" name="password" required>

            <button type="submit" style="margin-bottom: 20px">Login</button>
        </div>
    </form>
</div>
</body>
</html>


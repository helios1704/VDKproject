<?php
//escapeshellcmd('/usr/custom/test.py');
//$output = shell_exec("python python/test.py");
//$output = shell_exec("python python/toImage.py");
//file_put_contents("sendRequest.php","create");
//while ($data = file_get_contents("fileContainer.php") == "");
//$output = shell_exec("python python/convertToImage.py");
//$output = shell_exec("python python/extractMinutiae1.py");
//$output = shell_exec("python python/matchFingerprint.py");
//file_put_contents("fileContainer.php","");
//file_put_contents("sendRequest.php","");

$output = shell_exec("python python/test1.py tranvansi");
echo $output;

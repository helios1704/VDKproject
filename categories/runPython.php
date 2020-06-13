<?php
//$output = shell_exec("python python/convertToImage.py");
shell_exec("python python/extractMinutiae1.py");
$output = shell_exec("python python/matchFingerprint.py");
echo $output;

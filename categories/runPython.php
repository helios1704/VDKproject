<?php
////$command = escapeshellcmd('/usr/custom/test.py');
$output = shell_exec("python python/toImage.py");
echo $output;

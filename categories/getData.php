<?php
$data=$_POST["data"];
$Write="<?php echo '$data' ?>";
$Write1="<?php die(''); ?>";
file_put_contents('fileContainer.php',$Write);
file_put_contents('sendRequest.php',$Write1);
?>
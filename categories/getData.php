<?php
$data = $_POST["data"];
$Write = "$data";
$Write1 = "<?php die(''); ?>";
file_put_contents('fileContainer.php', $Write);
file_put_contents('sendRequest.php', "");
?>
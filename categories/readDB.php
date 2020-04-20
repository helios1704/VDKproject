<?php include "../includes/header.php"; ?>

<?php
include "database/connect.php";
$sql_query = "SELECT * FROM users";
$statement = $conn->prepare($sql_query);
$statement->setFetchMode(PDO::FETCH_ASSOC);
$statement->execute();
$row = $statement->fetchAll();
?>
<div class="container-sm" style="width: 90%; margin-top: 20px">
    <table class="table table-striped">
        <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Birthday</th>
            <th scope="col">Gender</th>
            <th scope="col">Fingerprint Image</th>
        </tr>
        </thead>
        <tbody>
        <?php foreach ($row as $k => $v) { ?>
            <tr>
                <th><?php echo $v['id']; ?></th>
                <td><?php echo $v['name']; ?></td>
                <td><?php echo $v['birthday']; ?></td>
                <td>@<?php echo $v['gender']; ?></td>
                <td>@<?php echo $v['fingerprint']; ?></td>
            </tr>
        <?php } ?>
        </tbody>
    </table>
</div>
<?php include "../includes/footer.php"; ?>

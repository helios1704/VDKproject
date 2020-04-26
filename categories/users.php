<?php
include "../includes/header.php";
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
include "database/connect.php";
$sql_query = "SELECT * FROM users";
$statement = $conn->prepare($sql_query);
$statement->setFetchMode(PDO::FETCH_ASSOC);
$statement->execute();
$row = $statement->fetchAll();
?>
<div class="container-sm" style="width:100%; margin-top: 20px">
    <table id="userTable" class="table table-striped">
        <thead>
        <tr>
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Birthday</th>
            <th scope="col">Gender</th>
            <th scope="col">Fingerprint Image</th>
            <th scope="col">Created_at</th>
            <th scope="col">Updated_at</th>
            <th scope="col">Action</th>
        </tr>
        </thead>
        <tbody>
        <?php foreach ($row as $k => $v) { ?>
            <tr>
                <th><?php echo $v['id']; ?></th>
                <td><?php echo $v['name']; ?></td>
                <td><?php echo date("d/m/Y", strtotime($v['birthday'])) ?></td>
                <td><?php if ($v['gender'] == 1) echo "Male";
                    elseif ($v['gender'] == 2) echo "Female";
                    else echo "Another"; ?></td>
                <td><?php echo $v['fingerprint']; ?></td>
                <td><?php echo $v['created_at']; ?></td>

                <td><?php echo $v['updated_at']; ?></td>
                <td>
                    <button style="padding: 4px 4px" type="button" name="edit" id="<?php echo $v["id"] ?>"
                            class="btn btn-success edit">
                        Edit
                    </button>
                    |
                    <button style="padding: 4px 4px" type="button" name="delete" id="<?php echo $v["id"] ?>"
                            class="btn btn-warning delete">
                        Delete
                    </button>
                </td>
            </tr>
        <?php } ?>
        </tbody>
    </table>
</div>
<script>
    $(document).ready(function () {
        setInterval(function () {
            table.ajax.reload();
        }, 30000);


        $('#userTable').DataTable({
            pageLength: 7,
            bLengthChange: false,
            order: [[0, "desc"]],
        });

        $("#userTable").on('click', '.delete', function (e) {
            e.preventDefault();
            var empId = $(this).attr("id");
            if (confirm("Are you sure you want to delete this employee?")) {
                $.ajax({
                    url: "deleteUser.php",
                    method: "POST",
                    data: {empId: empId},
                    dataType: 'json',
                    success: function (data) {
                        $('#userTable').DataTable().ajax.reload();
                    }
                })
            } else {
                return false;
            }
        });

    });
</script>
<?php include "../includes/footer.php"; ?>

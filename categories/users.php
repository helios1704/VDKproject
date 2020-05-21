<?php
include "../includes/header.php";
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
?>
<div class="container-sm" style="width:100%; margin-top: 20px">
    <table id="userTable" class="table table-striped">
        <thead>
        <tr>
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Birthday</th>
            <th scope="col">Gender</th>
            <th scope="col">Created_at</th>
            <th scope="col">Action</th>
        </tr>
        </thead>
    </table>
</div>
<script>
    $(document).ready(function () {
        table = $('#userTable').DataTable({
            pageLength: 7,
            bLengthChange: false,
            order: [[0, "desc"]],
            serverMethod: 'post',
            ajax: {
                'url': 'getUsers.php'
            },
            columns: [
                {data: 'id'},
                {data: 'name'},
                {data: 'birthday'},
                {data: 'gender'},
                {data: 'created_at'},
                {data: 'action'},
            ]
        });

        $("#userTable").on('click', '.delete', function (e) {
            e.preventDefault();
            var empId = $(this).attr("id");
            if (confirm("Are you sure you want to delete this user?")) {
                $.ajax({
                    url: "deleteUser.php",
                    method: "POST",
                    data: {empId: empId},
                    success: function (data) {
                        table.ajax.reload();
                    },
                    error: function (data) {
                    }
                })
            } else {
                return false;
            }
        });
    });
</script>
<?php include "../includes/footer.php"; ?>

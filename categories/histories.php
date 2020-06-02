<?php
include "../includes/header.php";
if (!isset($_SESSION['username'])) {
    header("Location: auth/login.php");
}
?>
<div class="container-sm" style="width:100%; margin-top: 20px">
    <table id="historyTable" class="table table-striped">
        <thead>
        <tr>
            <th scope="col">ID</th>
            <th scope="col">User ID</th>
            <th scope="col">Name</th>
            <th scope="col">Time</th>
        </tr>
        </thead>
    </table>
</div>
<script>
    $(document).ready(function () {
        table = $('#historyTable').DataTable({
            pageLength: 10,
            bLengthChange: false,
            order: [[0, "desc"]],
            serverMethod: 'post',
            ajax: {
                'url': 'getHistories.php'
            },
            columns: [
                {data: 'id'},
                {data: 'user_id'},
                {data: 'name'},
                {data: 'time'},
            ]
        });
    });
</script>
<?php include "../includes/footer.php"; ?>

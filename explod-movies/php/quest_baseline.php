<?php
session_start();
$_SESSION['baseline2'] = $_POST['Q2'];
$_SESSION['baseline3'] = $_POST['Q3'];
$_SESSION['baseline4'] = $_POST['Q4'];
$_SESSION['baseline5'] = $_POST['Q5'];


header('Location: ../php/manage_request_schema.php');
?>
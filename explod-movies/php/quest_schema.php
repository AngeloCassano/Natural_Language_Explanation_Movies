<?php
session_start();
$_SESSION['schema2'] = $_POST['Q2'];
$_SESSION['schema3'] = $_POST['Q3'];
$_SESSION['schema4'] = $_POST['Q4'];
$_SESSION['schema5'] = $_POST['Q5'];


header('Location: ../php/manage_request_primolivello.php');
?>
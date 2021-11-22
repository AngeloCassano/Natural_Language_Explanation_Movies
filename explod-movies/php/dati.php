<?php
session_start();

$_SESSION['age'] = $_POST['age'];
$_SESSION['gender']= $_POST['gender'];
$_SESSION['education']= $_POST['education'];
$_SESSION['interestMovies'] = $_POST['interestMovies'];
$_SESSION['recsysUsed']= $_POST['recsysUsed'];


header('Location: ../html/preferenze_film_popolari_utente.html');
?>
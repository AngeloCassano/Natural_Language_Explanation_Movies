<?php
session_start();
$_SESSION['primolivello2'] = $_POST['Q2'];
$_SESSION['primolivello3'] = $_POST['Q3'];
$_SESSION['primolivello4'] = $_POST['Q4'];
$_SESSION['primolivello5'] = $_POST['Q5'];


$header = "age; gender; education; interestMovies; recsysUsed; film_piaciuti; film_raccomandati; baseline; motivation_baseline; convincing_baseline; discover_information_baseline; trust_baseline; schema; motivation_schema; convincing_schema; discover_information_schema; trust_schema; primolivello; motivation_primolivello; convincing_primolivello; discover_information_primolivello; trust_primolivello ";

$text = $_SESSION['age']."; ".$_SESSION['gender']."; ".$_SESSION['education']."; ".$_SESSION['interestMovies']."; ".$_SESSION['recsysUsed']."; ".$_SESSION['film_piaciuti']."; ".$_SESSION['film_raccomandati']."; baseline; ".$_SESSION['baseline2']."; ".$_SESSION['baseline3']."; ".$_SESSION['baseline4']."; ".$_SESSION['baseline5']."; schema; ".$_SESSION['schema2']."; ".$_SESSION['schema3']."; ".$_SESSION['schema4']."; ".$_SESSION['schema5']."; primolivello; ".$_SESSION['primolivello2']."; ".$_SESSION['primolivello3']."; ".$_SESSION['primolivello4']."; ".$_SESSION['primolivello5'] ;

if(file_put_contents('dati_sessione_raccolti.csv', $text.PHP_EOL , FILE_APPEND | LOCK_EX)){

    session_destroy();
    header('Location: ../php/goodbye.php');
}


?>
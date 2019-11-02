<?php

include("config.php");

if(strpos(urldecode($_SERVER['QUERY_STRING']), '_') !== FALSE  ||  strpos(urldecode($_SERVER['QUERY_STRING']), '`') !== FALSE){
    // avoid querying sqlite_master ;)
    die("[+] Hacking attempt!!!!!11!\n");
}


foreach($_GET as $sql_column => $search_term)
{
    list($table, $column) = explode(':', $sql_column, 2);

    $stm = $dbh->prepare('SELECT `'. $column .'` FROM `'. $table .'` WHERE `'. $column .'` LIKE ? || "%"');
    $stm->bindValue(1, $search_term);
    $stm->execute();
    $res =$stm->fetchAll(PDO::FETCH_COLUMN);

    die(json_encode($res));
}


?>
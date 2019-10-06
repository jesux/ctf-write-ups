<?php
session_start();



if ($_GET['source']){
    highlight_file(__FILE__);
    exit();
}


class casino_debug {
    public $var = "path";
    public function __wakeup(){
        var_dump($_SESSION);
        echo file_get_contents($_SESSION[$this->var]);
    }
}


if (!empty($_GET['action']) && $_GET['action'] == "debug") {
    echo base64_decode($_COOKIE['debug']);
    unserialize(base64_decode($_COOKIE['debug']));
    exit();
}


if (!empty($_GET['action']) && $_GET['action'] == "bet" && !empty($_POST['bet']) && !empty($_POST['guess'])) {
    if (strpos($_POST['bet'], "/") !== false) {
        echo "HACK ATTEMPT!!!eleven!!1!";
        exit();
    }
    $_SESSION['path'] = __FILE__;
    $_SESSION['bet'] = md5($_POST['guess'], TRUE) . "/". $_POST['bet'];

    // Unfair :(
    if (rand() === $_POST['guess']) {
        echo "You win:" . file_get_contents("secret.php");
    }
    else {
        echo "You lose :)";
    }
}  
?>
<html>
<head>
<title>Moon Casino (under construction)</title>
<style>
    body{
        background: url(moon.jpg) no-repeat center center fixed;
    }
</style>
</head>
<body>
<!-- index.php?source=go --!>
</body>
</html>
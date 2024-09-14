<?php
class User {
    public $name;
    public $isLoggedIn;
}
$user = new User();
$user->name = "Carlos";
$user->isLoggedIn = true;
// Serialize Object User
$serializedUser = serialize($user);
echo "Serialized User: " . $serializedUser;
?>
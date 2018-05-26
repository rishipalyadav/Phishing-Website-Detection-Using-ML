<?php
$website="hello";
header("Access-Control-Allow-Origin: *");
$website = $_POST['url'];
// echo $website;
$html = file_get_contents($website);
// echo $html;
$bytes=file_put_contents('markup.txt', $html);
$a=exec('/Users/rishi/anaconda/bin/python test.py '.$website.' 2>&1 ');

echo $a;
?>

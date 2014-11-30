<html>
 <head>
  <title>A simple poem</title>
 </head>
 <body>
<?php 

$command = escapeshellcmd('python3 ./poem.py');
$output = shell_exec($command);
echo $output;

?>
 </body>
</html>

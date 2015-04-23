<html>
 <head>
  <title>A simple poem</title>
<link rel="stylesheet" type="text/css" href="twinkle-twinkle.css" />
 </head>
 <body>
<div id="poem">
<?php 

$command = escapeshellcmd('python3 ./poem.py normal');
$output = shell_exec($command);
echo $output;

?>
</div>
 </body>
</html>

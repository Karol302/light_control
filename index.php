
<html>
 <head>
 <meta name="viewport" content="width=device-width" />
 <title>LED Control</title>
 </head>
         <body>
         LED Control:
         <form method="get" action="index.php">
                 <input type="submit" value="ON" name="on">
                 <input type="submit" value="OFF" name="off">
     </form>

<?php
     if (isset($_GET['on']))
     {
     exec("sudo python /home/pi/deslab_project/relay_ON.py");
     shell_exec("sudo python /home/pi/deslab_project/relay_ON.py");
     }
     if (isset($_GET['off']))
     {
     exec("sudo python /home/pi/deslab_project/relay_OFF.py");
     }
?>

   </body>
</html>

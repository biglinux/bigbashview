echo '
<html>
    <head>
        <meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
        <title>BigBashView 2 Demos</title>
        <script src="/content$./javascript_html_tips/jquery.min.js" type="text/javascript"></script>
        <script type="text/javascript">
            $(document).ready(function(){ 
                
                //Do not redirect links with noredirect class
                $(".noredirect").click(function(e){
                    e.preventDefault();
                    $.get($(this).attr("href"));
                });
                
            });
        </script>
    </head>
    <body>
    <h1>Available demos</h1>
'
for x in *
do
    if [ -d $x ] && [ -f $x/execute_demo ]
    then
        echo "<a class='noredirect' href='/execute background\$./run.sh $x'>$x</a><br/>"
    fi
done

echo '
    </body>
</html>
'

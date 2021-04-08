<!DOCTYPE html>

<?php
ksort($_SERVER, SORT_STRING | SORT_FLAG_CASE); 
$shib_attrs = array();   
$others_attrs = array();

foreach($_SERVER as $attr=>$value)
    if(preg_match('/.*[a-z]|(shib|SHIB|Shib).*/', $attr))
        $shib_attrs[$attr] = $value;
    else $others_attrs[$attr] = $value;
?>

<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <link rel="icon" href="../../favicon.ico">
        <title>Shibboleth SP Attributes</title>
        <!-- Bootstrap core CSS -->
        <link href="/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body>
        <div class="container">
            <h1>Available SAML2 SP Attributes <small>Table with values</small></h1>
            <h3>Shibboleth SP Attributes</h3>
            <table class="table table-hover table-striped">
                <thead>
                    <tr>
                        <th scope="col">Attribute</th>
                        <th scope="col">Value</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach($shib_attrs as $attribute=>$value){ ?>
                    <tr>
                        <td>
                            <?php print($attribute); ?>
                        </td>
                        <td>
                            <i>
                                <?php 
                                $value = str_replace(";","<br>\n", $value);
                                print($value); 
                                ?>
                            </i>
                        </td>
                    </tr>
                    <?php } ?>
                </tbody>
            </table>
            <br>
            <h3>Other Session Attributes</h3>
            <table class="table table-hover table-striped">
                <thead>
                    <tr>
                        <th scope="col">Attribute</th>
                        <th scope="col">Value</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach($others_attrs as $attribute=>$value){ ?>
                    <tr>
                        <td>
                            <?php print($attribute); ?>
                        </td>
                        <td>
                            <i><?php print($value); ?></i>
                        </td>
                    </tr>
                    <?php } ?>
                </tbody>
            </table>
        </div>
    </body>
</html>

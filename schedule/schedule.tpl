<!DOCTYPE html>
<html lang="en">
  <head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <meta name="description" content="FOSSASIA 2016 Schedule">
    <meta name="author" content="FOSSASIA">
    <link rel="icon" href="favicon.ico">

    <title>FOSSASIA 2016 Schedule</title>

    <!-- Bootstrap core CSS -->
    <!-- Latest compiled and minified CSS -->
    <link rel="shortcut icon" href="../fossasia.ico" type="image/x-icon" />
    <link href="../css/bootstrap.min.css" rel="stylesheet" type="text/css" media="all"/>
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:400,600,300' rel='stylesheet' type='text/css'>  
    
    <link rel="stylesheet" href="../css/schedule.css">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>

    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button 
            type="button" 
            class="navbar-toggle collapsed"
            data-toggle="collapse"
            data-target="#navbar"
            aria-expanded="false">
            <span>Menu</span>
          </button>
          <a class="navbar-brand" href="//2016.fossasia.org">
            <img alt="Logo" class="logo logo-dark" src="../img/fossasia-dark.png">
          </a>
        </div>
        <div class="collapse navbar-collapse" id="navbar">
          <ul class="nav navbar-nav">
            {{#days}}
            <li class="dropdown">
              <a 
                href="#" 
                class="dropdown-toggle"
                data-toggle="dropdown"
                role="button"
                aria-haspopup="true"
                aria-expanded="false">
              {{caption}} 
              <span class="caret"></span>
              </a>
              <ul class="dropdown-menu">
                {{#tracks}}
                <li><a href="#{{slug}}">{{title}}</a></li>
                {{/tracks}}
              </ul>
            {{/days}}
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div id="session-list" class="container">

      {{#tracks}}
      <div class="row">
      <div class="col-md-12">

        <a class="anchor" id="{{slug}}"></a>
        <h3 class="track-title">{{title}}</h3>
        <h5>{{date}}</h5>

        <ul class="list-group session-list">
          {{#sessions}}
          <li class="list-group-item" data-session-id="{{uniqid}}">
            <div class="row"
              data-toggle="collapse"
              data-target="#desc-{{uniqid}}"
              aria-expanded="false"
              aria-controls="desc-{{uniqid}}">

            <div class="col-xs-2 col-md-1">
              <span class="time-alert session-start label label-primary">
                {{start}}
              </span>
            </div>

            <div class="col-xs-10 col-md-11">
              <div class="clearfix">
                <h4 class="session-title">
                  {{title}}
                </h4>
                <p class="session-location">
                  {{location}}
                </p>
              </div>
              <p>
                <span class="session-speakers">{{speakers}}</span>
              </p>
              <p>
                <span class="session-type">{{type}}</span>
              </p>
              <div class="collapse" id="desc-{{uniqid}}">
                <p>
                  <span class="session-description">{{description}}</span>
                </p>
              </div>

            </div><!-- /.row -->
          </li><!-- /.list-group-item -->
          {{/sessions}}
        </ul>
      </div><!-- /.col-md-12 -->
      </div><!-- /.row -->
      {{/tracks}}

    </div><!-- /#session-list -->

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" 
      integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" 
      crossorigin="anonymous"></script>
    <script type="text/javascript">
      // var ts = new Date().valueOf() // cache breaker
      // document.write('<script src="./main.js?t=' + ts + '"><\/script>')
    </script>
  </body>
</html>

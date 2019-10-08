#!/bin/bash


bcc_header () {
  echo '
  <body>
  <head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="/usr/share/bigbashview/bcc/css/base.css">
    <link rel="stylesheet" type="text/css" href="/usr/share/bigbashview/bcc/materialize/css/materialize.css">
    <script src="/usr/share/bigbashview/bcc/materialize/js/jquery.js"></script>
    <script src="/usr/share/bigbashview/bcc/materialize/js/materialize.js"></script>
    <script src="/usr/share/bigbashview/bcc/js/big.js"></script>
  </head>'
  echo '<title>' "$bcc_title" '</title>'

  # Header start
  ##############
  echo '
    <div id="header">'
      if [ "$bcc_logo" != "no" ]; then
        echo '<div id="header-logo">
          <img src='"$bcc_logo"'>
        </div>'
      fi
  # Title
  echo '<div id="header-title">'
    echo "$bcc_title"
    echo '<div id="header-subtitle">'
    echo "$bcc_description"
  echo '</div></div>'

  # header-right
  echo '
    <div id="header-right">'
          if [ "$bcc_about" = "yes" ]; then
              echo '<a href="#dialog-modal"><img src="/usr/share/bigbashview/bcc/images/about.png" id="rotate-over"></a>'
          fi
     echo '</div>
  </div>'
  ############
  # Header end


if [ "$bcc_about" = "yes" ]; then

# About dialog start
####################
echo '<div id="dialog-modal">
          <div id="dialog-modal-top">
                <div id="dialog-modal-top-left">'
                    echo $"Information"
                echo '</div><div id="dialog-modal-top-right">'
                    echo '<a href=#><img src="/usr/share/bigbashview/bcc/images/close.png"></a>'
                echo '</div>
          </div>
          <div id="dialog-modal-body">
            <div id="dialog-modal-body-left">'
            echo $"License: "
            echo '<br>'
            echo $"Created by:"
            echo '<br>'
            echo $"Date:"
            echo '<br>'
            echo $"Code URL:"
            echo '<br>'
            echo $"Project URL:"
            echo '</div>
            <div id="dialog-modal-body-right">'
              echo "$bcc_about_license"
              echo '<br>'
              echo "$bcc_about_by"
              echo '<br>'
              echo "$bcc_about_release_date"
              echo '<br>'
              echo "$bcc_about_url_code"
              echo '<br>'
              echo "$bcc_about_url_project"
            echo '</div>'
          echo '</div>'
echo '</div>'

fi
##################
# About dialog end
# Content start
###############
echo '<div id="content">'
}

import os
from bbv.globaldata import LOGO, APP_VERSION

# Import gettext module
import gettext
lang_translations = gettext.translation(
    'bigbashview',
    localedir='/usr/share/locale',
    fallback=True
)
lang_translations.install()

# define _ shortcut for translations
_ = lang_translations.gettext

TITLE = _('Bem-vindo ao BigBashView')
HOST_TEXT = _('Nome do Host')
DE_TEXT = _('Ambiente de Trabalho')
URL = 'https://github.com/biglinux/bigbashview'
HOST = os.uname()[1]
DE = os.environ.get('XDG_CURRENT_DESKTOP')

HTML = '''
<html>
    <head>
        <title>%s</title>
        <style>
        html, body{
            margin: 0;
            background: #2b303b;
        }
        .git{
            width: 32px;
            padding: 5px;
            fill: #788090;
        }
        .instruction{
            width: 100%%;
            height: auto;
            position: absolute;
            z-index: 1;
            bottom: 20px;
            font-size: 0.8em;
            color: #798191;
            text-align: center;
            font-family: Lato, sans-serif;
            font-weight: 300;
        }
        .instruction a{
            color: #2b303b;
        }
        .instruction a:hover{
            color: #788093;
        }
        .card{
            width: 320px;
            height: 0px;
            background: #FFF;
            position: absolute;
            z-index: 2;
            top: 58%%;
            margin-top: 0px;
            left: 50%%;
            margin-left: -160px;
            box-shadow: 5px 5px 10px 2px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            border-radius: 15px;
            opacity: 1;
            filter: alpha(opacity=100);
            -webkit-animation: card 2s forwards;
            -webkit-animation-iteration-count: 1;
            -webkit-animation-delay: 0s;
            -webkit-animation: card 2s forwards;
            animation: card 2s forwards;
            -webkit-animation-iteration-count: 1;
            animation-iteration-count: 1;
            -webkit-animation-delay: 0s;
            animation-delay: 0s;
            -webkit-transition-timing-function: ease-in-out;
            transition-timing-function: ease-in-out;
            box-sizing: border-box;
            -moz-box-sizing: border-box;
            -webkit-box-sizing: border-box;
            border-left: 0px solid red;
        }
        @-webkit-keyframes card{
            0%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 1px;
                margin-top: 0px;
                border-left: 0px solid #FFF;
                background: #444a59;
            }
            60%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 1px;
                margin-top: 0px;
                border-left: 320px solid #FFF;
                background: #444a59;
            }
            61%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 1px;
                margin-top: 0px;
                border-left: 0px solid #FFF;
                background: #FFF;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 450px;
                margin-top: -210px;
            }
        }
        @keyframes card{
            0%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 1px;
                margin-top: 0px;
                border-left: 0px solid #FFF;
                background: #444a59;
            }
            60%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 1px;
                margin-top: 0px;
                border-left: 320px solid #FFF;
                background: #444a59;
            }
            61%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 1px;
                margin-top: 0px;
                border-left: 0px solid #FFF;
                background: #FFF;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 350px;
                margin-top: -225px;
            }
        }
        .avatar{
            width: 110px;
            height: 82px;
            background: url(%s) no-repeat center center #FFF;
            background-size: 90%%;
            background-position-y: 5px;
            background-position-x: 6px;
            border-radius: 7px;
            position: absolute;
            z-index: 5;
            top: 100px;
            left: 50%%;
            margin-left: -55px;
            box-sizing: border-box;
            -moz-box-sizing: border-box;
            -webkit-box-sizing: border-box;
            opacity: 0;
            filter: alpha(opacity=0);
            -webkit-animation: avatar 1.5s forwards;
            -webkit-animation-iteration-count: 1;
            -webkit-animation-delay: 1s;
            -webkit-animation: avatar 1.5s forwards;
            animation: avatar 1.5s forwards;
            -webkit-animation-iteration-count: 1;
            animation-iteration-count: 1;
            -webkit-animation-delay: 1s;
            animation-delay: 1s;
            -webkit-transition-timing-function: ease-in-out;
            transition-timing-function: ease-in-out;
            margin-top: -110px;
        }
        @-webkit-keyframes avatar{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                top: 1000px;
            }
            50%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 125px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 125px;
            }
        }
        @keyframes avatar{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                top: 1000px;
            }
            50%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 125px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 125px;
            }
        }
        .cover{
            width: 0px;
            height: 0px;
            background: #4568DC;
            background: -webkit-linear-gradient(to right, #B06AB3, #4568DC);
            background: linear-gradient(to right, #B06AB3, #4568DC);
            position: absolute;
            top: 50%%;
            left: 50%%;
            opacity: 0;
            filter: alpha(opacity=0);
            -webkit-animation: cover 1s forwards;
            -webkit-animation-iteration-count: 1;
            -webkit-animation-delay: 1.5s;
            -webkit-animation: cover 1s forwards;
            animation: cover 1s forwards;
            -webkit-animation-iteration-count: 1;
            animation-iteration-count: 1;
            -webkit-animation-delay: 1.5s;
            animation-delay: 1.5s;
            -webkit-transition-timing-function: ease-in-out;
            transition-timing-function: ease-in-out;
            border-radius: 100%%;
        }
        @-webkit-keyframes cover{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                top: 40%%;
                left: 50%%;
                width: 0px;
                height: 0px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 20%%;
                margin-top: -150px;
                left: 50%%;
                margin-left: -250px;
                width: 500px;
                height: 400px;
            }
        }
        @keyframes cover{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                top: 40%%;
                left: 50%%;
                width: 0px;
                height: 0px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 20%%;
                margin-top: -150px;
                left: 50%%;
                margin-left: -250px;
                width: 500px;
                height: 400px;
            }
        }
        .userinfomain{
            width: 320px;
            height: 290px;
            background: #FFF;
            position: absolute;
            top: 53px;
            left: 0;
            z-index: 2;
        }
        h1, h2, h3, h4, h5, h6{
            margin: 0;
            padding: 0;
            font-family: Lato, sans-serif;
        }
        h1{
            text-align: center;
            font-size: 1.7em;
            letter-spacing: -0.02em;
            font-weight: 700;
            color: #2b303b;
            opacity: 0;
            filter: alpha(opacity=0);
            z-index: 2;
            position: absolute;
            margin-top: -25px;
            width: 100%%;
            -webkit-animation: heading1 0.6s forwards;
            -webkit-animation-iteration-count: 1;
            -webkit-animation-delay: 1.8s;
            -webkit-animation: heading1 1s forwards;
            animation: heading1 1s forwards;
            -webkit-animation-iteration-count: 1;
            animation-iteration-count: 1;
            -webkit-animation-delay: 1.8s;
            animation-delay: 1.8s;
            -webkit-transition-timing-function: ease-in-out;
            transition-timing-function: ease-in-out;
        }
        @-webkit-keyframes heading1{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                top: 120px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 65px;
            }
            }

            @keyframes heading1{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                top: 120px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 65px;
            }
        }
        h2{
            text-align: center;
            font-size: 1em;
            font-weight: 600;
            color: #999;
            opacity: 0;
            filter: alpha(opacity=0);
            z-index: 2;
            position: absolute;
            width: 100%%;
            margin-top: -20px;
            -webkit-animation: heading2 0.6s forwards;
            -webkit-animation-iteration-count: 1;
            -webkit-animation-delay: 2.2s;
            -webkit-animation: heading2 0.6s forwards;
            animation: heading2 0.6s forwards;
            -webkit-animation-iteration-count: 1;
            animation-iteration-count: 1;
            -webkit-animation-delay: 2.2s;
            animation-delay: 2.2s;
            -webkit-transition-timing-function: ease-in-out;
            transition-timing-function: ease-in-out;
        }
        @-webkit-keyframes heading2{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                top: 160px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 98px;
            }
            }

            @keyframes heading2{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                top: 160px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                top: 98px;
            }
        }
        .divider{
            width: 0px;
            height: 1px;
            background: #EAEAEA;
            position: relative;
            top: 160px;
            left: 50%%;
            z-index: 4;
            opacity: 0;
            filter: alpha(opacity=0);
            -webkit-animation: divider 1s forwards;
            -webkit-animation-iteration-count: 1;
            -webkit-animation-delay: 2.4s;
            -webkit-animation: divider 1s forwards;
            animation: divider 1s forwards;
            -webkit-animation-iteration-count: 1;
            animation-iteration-count: 1;
            -webkit-animation-delay: 2.4s;
            animation-delay: 2.4s;
            -webkit-transition-timing-function: ease-in-out;
            transition-timing-function: ease-in-out;
        }
        @-webkit-keyframes divider{
            0%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 0px;
                left: 50%%;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                left: 50%%;
                margin-left: -160px;
            }
        }
        @keyframes divider{
            0%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 0px;
                left: 50%%;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                left: 50%%;
                margin-left: -160px;
            }
        }
        .socialinfo{
            width: 240px;
            position: absolute;
            bottom: -20px;
            left: 40px;
            z-index: 3;
            opacity: 0;
            top: 172px;
            filter: alpha(opacity=0);
            -webkit-animation: socialinfo 0.6s forwards;
            -webkit-animation-iteration-count: 1;
            -webkit-animation-delay: 1s;
            -webkit-animation: socialinfo 0.6s forwards;
            animation: socialinfo 0.6s forwards;
            -webkit-animation-iteration-count: 1;
            animation-iteration-count: 1;
            -webkit-animation-delay: 1s;
            animation-delay: 1s;
            -webkit-transition-timing-function: ease-in-out;
            transition-timing-function: ease-in-out;
            height: 182px;
        }
        @-webkit-keyframes socialinfo{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                bottom: -20px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                bottom: 17px;
            }
        }
        @keyframes socialinfo{
            0%%{
                opacity: 0;
                filter: alpha(opacity=0);
                bottom: -20px;
            }
            100%%{
                opacity: 1;
                filter: alpha(opacity=100);
                bottom: 17px;
            }
        }
        .socialone, .socialtwo{
            margin-bottom: 10px;
            opacity: 0;
            filter: alpha(opacity=0);
            text-align: center;
            -webkit-animation: socialinfo 0.6s forwards;
            animation: socialinfo 0.6s forwards;
        }
        .socialone{
            left: 0;
            -webkit-animation-delay: 2.4s;
            animation-delay: 2.4s;
        }
        .socialtwo{
            left: 93px;
            -webkit-animation-delay: 2.6s;
            animation-delay: 2.6s;
        }
        .socialtext, .socialheading{
            font-family: Lato, sans-serif;
        }
        .socialtext{
            font-family: Lato, sans-serif;
            font-weight: 700;
            font-size: 1.2em;
            color: #798191;
        }
        .socialheading{
            font-family: Lato, sans-serif;
            font-weight: 300;
            font-size: 0.9em;
            color: #999;
            display: block;
        }
        </style>
    </head>
    <body>
        <div>
            <div class="card">
                <div class="avatar"></div>
                <div class="cover"></div>
                <div class="userinfomain">
                    <h1>BigBashView<h1>
                    <h2>%s<h2>
                </div>
                <div class="divider"></div>
                <div class="socialinfo">
                    <div class="socialone">
                        <span class="socialheading">%s</span>
                        <span class="socialtext">%s</span><br />
                    </div>
                    <div class="socialtwo">
                        <span class="socialheading">%s</span>
                        <span class="socialtext">%s</span><br />
                    </div>
                    <div class="socialtwo">
                        <div class="instruction">
                            <svg class="git" viewBox="0 0 496 512"><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg><br>
                            <a href="#!" style='text-decoration:none'
                               onclick="_run('xdg-open %s')">
                                https://github.com/biglinux/bigbashview
                            </a>
                        </div>
                    </div>
                </div>


            </div>

        </div>
    </body>
</html>
''' % (TITLE, LOGO, APP_VERSION, HOST_TEXT, HOST, DE_TEXT, DE, URL)

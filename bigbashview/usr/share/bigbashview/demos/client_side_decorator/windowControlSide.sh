#!/usr/bin/env bash

# Execute command to obtain left-side button configuration
buttonsLeft=$(kreadconfig6 --group "org.kde.kdecoration2" --key "ButtonsOnLeft" --file "$HOME/.config/kwinrc")

# Execute command to obtain right-side button configuration
buttonsRight=$(kreadconfig6 --group "org.kde.kdecoration2" --key "ButtonsOnRight" --file "$HOME/.config/kwinrc")

minimizeButton="
                <a id=\"minimize-btn\" onclick=\"windowControl.minimize()\">
                    <div class=\"window-control-btn-box\">
                        <div class=\"window-control-btn\">
                            <img class=\"window-control-btn-img\" src=\"$(geticons --no-fallbacks window-minimize-symbolic | head -n1)\">
                        </div>
                    </div>
                </a>
"

maximizeButton="
                <a id=\"maximize-btn\" onclick=\"windowControl.maximize()\">
                    <div class=\"window-control-btn-box\">
                        <div id=\"maximize-btn-image\" class=\"window-control-btn\">
                            <!-- This icon is managed by javascript to change from maximize and restore -->
                        </div>
                    </div>
                </a>
"

closeButton="
                <a id=\"close-btn\" onclick=\"windowControl.close()\">
                    <div class=\"window-control-btn-box\">
                        <div class=\"window-control-btn\">
                            <img class=\"window-control-btn-img\" src=\"$(geticons --no-fallbacks window-close-symbolic | head -n1)\">
                        </div>
                    </div>
                </a>
"

if [[ "$buttonsLeft" =~ [XAI] ]]; then

    echo '<div id="window-controls-left" class="window-controls no-drag">'

    # Iterate over each character in the left-side configuration string
    for (( i=0; i<${#buttonsLeft}; i++ )); do
    char=${buttonsLeft:$i:1} # Extract the current character
    
    # Check the character and print its function if it's X, I, or A
    case $char in
        X) echo "$closeButton" ;;
        A) echo "$maximizeButton" ;;
        I) echo "$minimizeButton" ;;
    esac
    done

    echo "</div>"
fi

if [[ "$buttonsRight" =~ [XAI] ]]; then
    echo '<div id="window-controls-right" class="window-controls no-drag">'
    # Iterate over each character in the right-side configuration string
    for (( i=0; i<${#buttonsRight}; i++ )); do
    char=${buttonsRight:$i:1} # Extract the current character
    
    # Check the character and print its function if it's X, I, or A
    case $char in
        X) echo "$closeButton" ;;
        A) echo "$maximizeButton" ;;
        I) echo "$minimizeButton" ;;
    esac
    done

    echo '</div>'
fi

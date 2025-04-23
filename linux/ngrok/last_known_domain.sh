#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source $script_dir/.env
domain=$(cat $script_dir/$last_known_domain_filename)
echo "The contents: $domain"

#Timestamps vars
year_month_date=$(date +"%Y%m%d")
year_month=$(date +"%Y%m")
timestamp=$(date +%b' '%d' '%T)

current_domain=$(curl http://127.0.0.1:4040/api/tunnels --silent | jq '.tunnels | .[] | .public_url' | tr -d '"')

if [ "$current_domain" == "" ]; then
    echo "$timestamp: WARNING: ngrok is NOT running...Attempting to start" >> $script_dir/logs/ngrok-restart-$(date +"%Y-%m-%d").log

    sudo systemctl restart ngrok

    #Fetch new url/domain after restart
    current_domain=$(curl http://127.0.0.1:4040/api/tunnels --silent | jq '.tunnels | .[] | .public_url' | tr -d '"')

    # Test for internet connection
    wget -q --spider http://google.com

    if [ $? -eq 0 ]; then
        echo "$timestamp: Sending new domain: $current_domain to replace older one: $domain"  >> $script_dir/logs/ngrok-restart-$(date +"%Y-%m-%d").log
        echo "$timestamp: $current_domain > $script_dir/$last_known_domain_filename"  >> $script_dir/logs/ngrok-restart-$(date +"%Y-%m-%d").log
        echo $current_domain > $script_dir/$last_known_domain_filename
        echo "$timestamp: $venv $script_dir/send_last_know_domain.py $current_domain"  >> $script_dir/logs/ngrok-restart-$(date +"%Y-%m-%d").log
        log_domain_cmd="echo $current_domain > ~/ngrok/convent-$(date +"%Y-%m-%d").log"
        ssh -l kkiragu chelwoodplace.com "${log_domain_cmd}"
    else
        echo "$timestamp: Internet Down, try in the next iteration"  >> $script_dir/logs/ngrok-restart-$(date +"%Y-%m-%d").log
    fi
else
    # domains don't match, so send new current domain'
    if [ "$current_domain" != "$domain" ]; then
        # Test for internet connection
        wget -q --spider http://google.com

        if [ $? -eq 0 ]; then
            #send email
            echo "$timestamp: Sending new domain: $current_domain to replace older one: $domain"  >> $script_dir/logs/ngrok-restart-$(date +"%Y-%m-%d").log
            echo "$timestamp: $current_domain > $script_dir/$last_known_domain_filename"  >> $script_dir/logs/ngrok-restart-$(date +"%Y-%m-%d").log
            echo $current_domain > $script_dir/$last_known_domain_filename
            echo "$timestamp: $venv $script_dir/send_last_know_domain.py $current_domain"  >> $script_dir/logs/ngrok-restart-$(date +"%Y-%m-%d").log
            log_domain_cmd="echo $current_domain > ~/ngrok/convent-$(date +"%Y-%m-%d").log"
            ssh -l kkiragu chelwoodplace.com "${log_domain_cmd}"
        else
            echo "$timestamp: Internet Down, try in the next iteration"  >> $script_dir/logs/ngrok-restart-$(date +"%Y-%m-%d").log
        fi
    fi
fi

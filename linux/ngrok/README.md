# Install ngrok
1. Follow instructions at: https://ngrok.com/downloads/linux
   ```
   curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
   | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
   && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
   | sudo tee /etc/apt/sources.list.d/ngrok.list \
   && sudo apt update \
   && sudo apt install ngrok
   ```
2.

# Create ngrok service

Create an ngrok.service:

```
sudo cat ngrok.sample.service > /etc/systemd/system/ngrok.service
```

Create ngrok.yml:
```
mkdir /opt/ngrok
sudo cat ngrok.sample.yml > /opt/ngrok/ngrok.yml
```

NB: Remember to add ngrok add token to ngrok.yml file above

Enable and start services:
```
systemctl enable ngrok.service
systemctl start ngrok.service
```

## Notification of ngrok Domain Change via Email

Create a crontab as non-root (e.g. under your own user account):

```
# Check ngrok domain every 20 minutes and email if changed
*/20 * * * * ~/Documents/tech/git/helpers/linux/ngrok/last_known_domain.sh
```

Create an `.env` in dir where `last_known_domain.sh` is located with following details (if using sendgrid to send email):
```
last_known_domain_filename=.ngrok.domain
host=work-pc
export SENDGRID_API_KEY='sendgrid_api_key_to_enable_email'
venv=/home/username/.venv/imagesearch/bin/python
export DOMAIN_EMAIL_ADDRESS_FILE=/..pathToEmailList/domain_email_list.csv
export DOMAIN_EMAIL_TEMPLATE_ID='d-temp-id'
```

OR if only using ssh to send the new domain:
```
last_known_domain_filename=.ngrok.domain
host=work-pc
```

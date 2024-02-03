from mailchimp_marketing import Client

mailchimp = Client()
mailchimp.set_config({
  "api_key": "",
  "server":"us11"
})

response = mailchimp.ping.get()
print(response)
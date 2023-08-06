# postbode-python
A Postbode API wrapper for Python. 
www.postbode.nu is a Dutch web application for digitally sending and receiving postal mail and automation of postal services. This package is a set of python wrappers build around the API of this services.

## Getting started
For starters you will need a account and a api token.

_Account creation_

Go to http://app.postbode.nu and follow registration proces.

_API token_

After registration go to personal settings -> API and request a token.

_Sandbox mode_

For testing the api it is usefull to set the mailbox in sandbox mode. A dev mode sort of speak that will prefent any request to be send to production.

_further reading_

http://api.postbode.nu for more information about the letter and mailbox options

Now you are set to go.

## Examples

__Instantiate and authenticate with the client__
```python
from postbode.client import Client

client = Client('YOUR_API_TOKEN')
```

__Get available mailboxes__
```python
from postbode.client import Client

client.get_mailboxes()
```

__Get letters of mailbox__
```python
client.get_letters('MAILBOX_ID')
```

__Send letter__
```python
from postbode.client import Client

client.send_letter('MAILBOX_ID', 'Filename', './file.pdf','NL', False, 'FC', 'simplex', 'inkjet', True )
```

__Send letters__
```python
letters = ('./letter1.pdf','./letter2.pdf','./letter3.pdf')
client.send_letters(2522, 2, 'NL', False, 'FC', 'simplex', 'inkjet', True, *letters)
```




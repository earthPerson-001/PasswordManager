#!/bin/sh

rm master_key.db \
   encrypted_passwords.db \
	&& \
echo "deleted master_key.db and encrypted_passwords.db" \
	|| echo  "Couldn't delete master_key.db and encrypted_passwords.db" 

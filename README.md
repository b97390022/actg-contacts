# actg-contacts

actg-contacts a Python Discord Bot to search contacts of ACTGenomics.

[![Docker Build](https://github.com/b97390022/actg-contacts/actions/workflows/basic.yml/badge.svg)](https://github.com/b97390022/actg-contacts/actions/workflows/basic.yml)

## Create Confin.json
Please place the config.json file into the actg-contacts folder and replace the corresponding values.

```json
{
    "env": "producion",
    "ldap_server": "ldap_server",
    "ldap_user": "ldap_user",
    "ldap_password": "ldap_password",
    "discord_token": "discord_token"
}
```

## Usage

```bash
git clone https://github.com/b97390022/actg-contacts.git
cd actg-contacts

docker compose up -d
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
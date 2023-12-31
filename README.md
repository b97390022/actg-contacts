# actg-contacts

actg-contacts a Python Discord Bot to search contacts of ACTGenomics✨.

[![Docker Build](https://github.com/b97390022/actg-contacts/actions/workflows/basic.yml/badge.svg)](https://github.com/b97390022/actg-contacts/actions/workflows/basic.yml)

# Datasource
- LDAP
- Excel file (//tp-fs01/Public/公司通訊錄與座位表/* 通訊錄 *.xlsx)

## Create Confin.json
Please place the config.json file into the actg-contacts folder and replace the corresponding values.

```json
{
    "env": "producion",
    "ldap_server": "ldap_server",
    "ldap_user": "ldap_user",
    "ldap_password": "ldap_password",
    "discord_token": "discord_token",
    "smb_user": "sub_user",
    "smb_password": "smb_password"
}
```

## Usage

```bash
git clone https://github.com/b97390022/actg-contacts.git
cd actg-contacts

docker compose up -d
```


## Development

#### Init environment
```bash
poetry install
```

#### Install pre-commit hooks
```bash
pre-commit install
```

#### Make sure that you install the extensions for better experience:
- linter: Pylint [https://marketplace.visualstudio.com/items?itemName=ms-python.pylint]
- formatter: black [https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter&ssr=false#review-details]

#### Poetry scripts
```bash
poetry run prepare
poetry run audit
poetry run lint
poetry run build:load
poetry run build:push
poetry run start
poetry run test
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

# Takina v1.1.0
A simple multipurpose bot for Discord. Also the very cutest Discord bot. Sakanaaa <3

For a list of features and other information please visit: https://takina.orangc.net.

## Selfhosting
Before proceeding, I am assuming that you have a running MongoDB database. The majority of Takina's functionality depends on a MongoDB instance being available. A guide on selfhosting MongoDB with Docker is available [here](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/), you can also consider using [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database) or use the MongoDB server made in the docker compose file.

#### On NixOS

*Assuming that you have `git` installed.*

- `git clone https://github.com/orangci/takina && cd takina`
- Set all the required environment variables in the `.env` file. You can find a list of what those are in the `.env.example` file. You can leave most of them as their defaults, but you at a minimum must set the `TOKEN` (Discord bot token), `HASDB=yes`, and  `MONGO` (your MongoDB URI.)
- Run `nix-shell`; You may need to run `nix-shell` twice if the first time doesn't start the bot up.

In the future, this will be managed with a proper flake.

#### With Docker

##### Manually

*Assuming you have `git` and `docker` installed.*

- `git clone https://github.com/orangci/takina && cd takina`
- Set all the required environment variables in the `.env` file. You can find a list of what those are in the `.env.example` file. You can leave most of them as their defaults, but you at a minimum must set the `TOKEN` (Discord bot token), `HASDB=yes`, and  `MONGO` (your MongoDB URI.)
- `docker build --tag 'takina' .`
- `docker run 'takina'`

##### Docker Compose

*Assuming you have `git` and `docker` installed.*

- `git clone https://github.com/orangci/takina && cd takina`
- Set all the required environment variables in the `docker-compose.yml` file. You can find a list of what those are in the `docker-compose.yml` file, which has all the ENV's you need.
- `docker compose up -d`

## Contributing
Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Legal
- [License: GNU AGPLv3](./LICENSE)
- [Terms of Service](https://orangc.net/takina/tos.html)
- [Privacy Policy](https://orangc.net/takina/privacy.html)

## Specifications
- This project follows the [Semantic Versioning 2.0.0](https://semver.org/) specification as of 14.04.2025.
- This project follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification as of 01.10.2024.
<!-- note to self: count takina loc with: `git ls-files | grep '\.py$' | xargs wc -l | tail -n 1`, 9,839 as of 14.04.2025 -->
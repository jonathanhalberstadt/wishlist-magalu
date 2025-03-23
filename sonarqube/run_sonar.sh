#!/bin/bash

if [ -z "$SONAR_LOGIN" ]; then
  echo "Erro: A variável de ambiente SONAR_LOGIN não está definida."
  exit 1
fi

docker container run --rm --network=host \
  -e SONAR_HOST_URL="http://localhost:9000" \
  -v "$HOME/projetos/wishlist-magalu:/usr/src" \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=wishlist-magalu \
  -Dsonar.sources=/usr/src \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login="$SONAR_LOGIN"

docker network create internship2024-kalimatcash-$CI_COMMIT_TAG
docker run -d --network=internship2024-kalimatcash-$CI_COMMIT_TAG --name=internship2024-kalimatcash-pgtest-$CI_COMMIT_TAG -e POSTGRES_USER=internship2024 -e POSTGRES_PASSWORD=internship2024123 -e POSTGRES_DB=postgres postgres 
docker run    --network=internship2024-kalimatcash-$CI_COMMIT_TAG --rm -e SQL_USER=internship2024 -e SQL_HOST=internship2024-kalimatcash-pgtest-$CI_COMMIT_TAG -e SQL_PASSWORD=internship2024123 docker.et3.co/internship2024.kalimatcash sh runtests.sh 
docker rm -f internship2024-kalimatcash-pgtest-$CI_COMMIT_TAG
docker network rm internship2024-kalimatcash-$CI_COMMIT_TAG
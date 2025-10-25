#!/usr/bin/env bash
BASE_URL=http://127.0.0.1:8000

echo "Not found"
curl -s $BASE_URL/company/0 | jq .

echo "Existing"
curl -s $BASE_URL/company/1 | jq .
curl -s $BASE_URL/company/2 | jq .

echo "Not found"
curl -s $BASE_URL/company/3 | jq .

echo "Fail to update"
curl -s $BASE_URL/company/3 -X PUT -d '{"id": "3", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Update"
curl -s $BASE_URL/company/2 -X PUT -d '{"id": "2", "name": "Updated 2"}' -H "Content-Type: application/json" | jq .

echo "Create new"
curl -s $BASE_URL/company -d '{"name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Fail to update"
curl -s $BASE_URL/company/3 -X PUT -d '{"id": "7", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Update"
curl -s $BASE_URL/company/3 -X PUT -d '{"id": "3", "name": "NCorp"}' -H "Content-Type: application/json" | jq .

echo "Delete new"
curl -s -X DELETE $BASE_URL/company/3

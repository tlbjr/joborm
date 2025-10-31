#!/usr/bin/env bash
BASE_URL=http://127.0.0.1:8000

echo "Not found"
curl -s $BASE_URL/company/5804cabc-11f9-43b0-a2b2-d6a966bdcf33 | jq .

echo "Not a UUID"
curl -s $BASE_URL/company/xyz | jq .

#echo "Existing"
#curl -s $BASE_URL/company/1 | jq .
#curl -s $BASE_URL/company/2 | jq .
#echo "Not found"
#curl -s $BASE_URL/company/0 | jq .
#echo "Fail to update"
#curl -s $BASE_URL/company/1 -X PUT -d '{"id": "3", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Create new"
curl -s $BASE_URL/company -d '{"name": "New Corp", "github": "gh"}' -H "Content-Type: application/json" | jq . | tee /tmp/test_new_company.json
NEW_ID=`jq -r .id /tmp/test_new_company.json`

echo "Fail to update (Not a UUID)"
curl -s $BASE_URL/company/7 -X PUT -d '{"id": "7", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Fail to update (Non-matching)"
curl -s $BASE_URL/company/$NEW_ID -X PUT -d '{"id": "5804cabc-11f9-43b0-a2b2-d6a966bdcf33", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Fail to update (Not found)"
curl -s $BASE_URL/company/5804cabc-11f9-43b0-a2b2-d6a966bdcf33 -X PUT -d '{"id": "5804cabc-11f9-43b0-a2b2-d6a966bdcf33", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Update"
curl -s $BASE_URL/company/$NEW_ID -X PUT -d '{"id": "'"$NEW_ID"'", "name": "NCorp"}' -H "Content-Type: application/json" | jq .

echo "Delete new"
curl -s -X DELETE $BASE_URL/company/$NEW_ID

#!/usr/bin/env bash
BASE_URL=http://127.0.0.1:8000

echo "Company not found by uuid (fail)"
curl -s $BASE_URL/company/5804cabc-11f9-43b0-a2b2-d6a966bdcf33 | jq .

echo "company id is not a UUID (alpha fail)"
curl -s $BASE_URL/company/xyz | jq .

#echo "Existing"
#curl -s $BASE_URL/company/1 | jq .
#curl -s $BASE_URL/company/2 | jq .
#echo "Not found"
#curl -s $BASE_URL/company/0 | jq .
#echo "Fail to update"
#curl -s $BASE_URL/company/1 -X PUT -d '{"id": "3", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Create new company"
curl -s $BASE_URL/company -d '{"name": "Test Corp", "github": "gh"}' -H "Content-Type: application/json" | jq . | tee /tmp/test_new_company.json
NEW_ID=`jq -r .id /tmp/test_new_company.json`
echo NEW_ID $NEW_ID

echo "Update company by non-UUID (fail)"
curl -s $BASE_URL/company/7 -X PUT -d '{"id": "7", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Update company with non-matching company id (fail)"
curl -s $BASE_URL/company/$NEW_ID -X PUT -d '{"id": "5804cabc-11f9-43b0-a2b2-d6a966bdcf33", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Update when not found (fail)"
curl -s $BASE_URL/company/5804cabc-11f9-43b0-a2b2-d6a966bdcf33 -X PUT -d '{"id": "5804cabc-11f9-43b0-a2b2-d6a966bdcf33", "name": "New Corp"}' -H "Content-Type: application/json" | jq .

echo "Update company"
curl -s $BASE_URL/company/$NEW_ID -X PUT -d '{"id": "'"$NEW_ID"'", "name": "Geminus AI"}' -H "Content-Type: application/json" | jq .

if [ "$1" != "keep" ];
then
    echo "Delete new company"
    curl -s -X DELETE $BASE_URL/company/$NEW_ID | jq .
fi

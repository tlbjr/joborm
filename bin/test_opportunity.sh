#!/usr/bin/env bash
BASE_URL=http://127.0.0.1:8000

echo "Not found"
curl -s $BASE_URL/opportunity/019a3b79-1243-7ca3-9f9c-1adc8b909dfb | jq .

echo "Not a UUID"
curl -s $BASE_URL/opportunity/14158928 | jq .
curl -s $BASE_URL/opportunity/xyz | jq .

#echo "Existing"
#curl -s $BASE_URL/opportunity/1 | jq .
#curl -s $BASE_URL/opportunity/2 | jq .
#curl -s $BASE_URL/opportunity/3 | jq .
#echo "Not found"
#curl -s $BASE_URL/opportunity/4 | jq .
#echo "Fail to update"
#curl -s $BASE_URL/opportunity/4 -X PUT -d '{"id": "4", "company_id": "1"}' -H "Content-Type: application/json" | jq .
#echo "Update"
#curl -s $BASE_URL/opportunity/2 -X PUT -d '{"id": "2", "company_id": "2", "position": "N/A", "process": {"items": []}}' -H "Content-Type: application/json" | jq .

echo "Create new company"
curl -s $BASE_URL/company -d '{"name": "Test comapny for oppo"}' -H "Content-Type: application/json" | jq . | tee /tmp/test_new_company_for_oppo.json
COMPANY_ID=`jq -r .id /tmp/test_new_company_for_oppo.json`
echo $COMPANY_ID

echo "Create new"
curl -s $BASE_URL/opportunity -d '{"company_id": "'"$COMPANY_ID"'", "position": "Something New", "process": {"items": []}}' -H "Content-Type: application/json" | jq . | tee /tmp/test_new_oppo.json
NEW_ID=`jq -r .id /tmp/test_new_oppo.json`
echo $NEW_ID

echo "Fail to update"
curl -s $BASE_URL/opportunity/4 -X PUT -d '{"id": "7", "position": "New Fail"}' -H "Content-Type: application/json" | jq .

echo "Update w/o company_id"
curl -s $BASE_URL/opportunity/$NEW_ID -X PUT -d '{"id": "'"$NEW_ID"'", "position": "No company", "process": {"items": []}}' -H "Content-Type: application/json" | jq .

echo "Update"
curl -s $BASE_URL/opportunity/$NEW_ID -X PUT -d '{"id": "'"$NEW_ID"'", "company_id": "'"$COMPANY_ID"'", "position": "N/A", "process": {"items": []}}' -H "Content-Type: application/json" | jq .

echo "Delete new"
curl -s -X DELETE $BASE_URL/opportunity/$NEW_ID

echo "Delete test company"
curl -s -X DELETE $BASE_URL/company/$COMPANY_ID

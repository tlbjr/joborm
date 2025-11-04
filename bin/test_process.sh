#!/usr/bin/env bash

BASE_URL=http://127.0.0.1:8000

#echo "Existing"
#curl -s $BASE_URL/process/1 | jq .
#curl -s $BASE_URL/process/2 | jq .
#curl -s $BASE_URL/process/3 | jq .
#echo "Update"
#curl -s $BASE_URL/process/2 -X PUT -d '{"id": "2", "company_id": "2", "name": "N/A", "process": {"items": [{"type_": "Panel", "location": "in-person", "with_": "internal"}]}}' -H "Content-Type: application/json" | jq .

echo "Create new company"
curl -s $BASE_URL/company -d '{"name": "Test Process Company"}' -H "Content-Type: application/json" | jq . | tee /tmp/new_company_for_process.json
COMPANY_ID=`jq -r .id /tmp/new_company_for_process.json`
echo COMPANY_ID: $COMPANY_ID

echo "Create new opportunity"
curl -s $BASE_URL/opportunity -d '{"name": "Test Process Oppo", "company_id": "'"$COMPANY_ID"'"}' -H "Content-Type: application/json" | jq . | tee /tmp/new_oppo_for_process.json
OPPORTUNITY_ID=`jq -r .id /tmp/new_oppo_for_process.json`
echo OPPORTUNITY_ID: $OPPORTUNITY_ID

echo "Create new"
curl -s $BASE_URL/process -d '{"opportunity_id": "'"$OPPORTUNITY_ID"'", "items": [{"type_": "Panel"}]}' -H "Content-Type: application/json" | jq . | tee /tmp/new_process_for_test.json
NEW_ID=`jq -r .id /tmp/new_process_for_test.json`
echo NEW_ID: $NEW_ID

#echo "Update Fail - Not a UUID"
#curl -s $BASE_URL/process/4 -X PUT -d '{"id": "4", "company_id": "1", "name": "N/A", "process": {"items": []}}' -H "Content-Type: application/json" | jq .

#echo "Update Fail - Not Found"
#curl -s $BASE_URL/process/019a3b79-1243-7ca3-9f9c-1adc8b909dfb -X PUT -d '{"id": "019a3b79-1243-7ca3-9f9c-1adc8b909dfb", "company_id": "1", "name": "N/A", "process": {"items": []}}' -H "Content-Type: application/json" | jq .

echo "Delete oppo - can't"
curl -s -X DELETE $BASE_URL/opportunity/$OPPORTUNITY_ID | jq .

echo "Delete company - can't"
curl -s -X DELETE $BASE_URL/company/$COMPANY_ID | jq .

echo "Delete new"
curl -s -X DELETE $BASE_URL/process/$NEW_ID | jq .

echo "Delete oppo"
curl -s -X DELETE $BASE_URL/opportunity/$OPPORTUNITY_ID | jq .

echo "Delete company"
curl -s -X DELETE $BASE_URL/company/$COMPANY_ID | jq .

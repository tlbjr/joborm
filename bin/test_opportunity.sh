#!/usr/bin/env bash
BASE_URL=http://127.0.0.1:8000

echo "Opportunity not found by uuid (fail)"
curl -s $BASE_URL/opportunity/019a3b79-1243-7ca3-9f9c-1adc8b909dfb | jq .

echo "Opportunity id is not a UUID (number fail)"
curl -s $BASE_URL/opportunity/14158928 | jq .

echo "Opportunity id is not a UUID (alpha fail)"
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
#curl -s $BASE_URL/opportunity/2 -X PUT -d '{"id": "2", "company_id": "2", "name": "N/A", "process": {"items": []}}' -H "Content-Type: application/json" | jq .

echo "Create new company (opp test)"
curl -s $BASE_URL/company -d '{"name": "Non-Company"}' -H "Content-Type: application/json" | jq . | tee /tmp/test_new_company_for_oppo.json
COMPANY_ID=`jq -r .id /tmp/test_new_company_for_oppo.json`
echo COMPANY_ID $COMPANY_ID

echo "Create new oppo w/o company_id (fail)"
curl -s $BASE_URL/opportunity -d '{"name": "Something New"}' -H "Content-Type: application/json" | jq . | tee /tmp/test_new_oppo.json

echo "Create new oppo"
curl -s $BASE_URL/opportunity -d '{"company_id": "'"$COMPANY_ID"'", "name": "New Test Position"}' -H "Content-Type: application/json" | jq . | tee /tmp/test_new_oppo.json
NEW_ID=`jq -r .id /tmp/test_new_oppo.json`
echo NEW_ID $NEW_ID

echo "Update oppo by non-UUID (fail)"
curl -s $BASE_URL/opportunity/4 -X PUT -d '{"id": "7", "name": "New Fail"}' -H "Content-Type: application/json" | jq .

echo "Update oppo w/o company_id (fail)"
#curl -s $BASE_URL/opportunity/$NEW_ID -X PUT -d '{"id": "'"$NEW_ID"'", "name": "No company", "process_id": "'"$PROCESS_ID"'"}' -H "Content-Type: application/json" | jq .
curl -s $BASE_URL/opportunity/$NEW_ID -X PUT -d '{"id": "'"$NEW_ID"'", "name": "No company"}' -H "Content-Type: application/json" | jq .

echo "Update oppo"
curl -s $BASE_URL/opportunity/$NEW_ID -X PUT -d '{"id": "'"$NEW_ID"'", "company_id": "'"$COMPANY_ID"'", "name": "Non-Job", "process": null}' -H "Content-Type: application/json" | jq .

echo "Create new oppo w/o company_id by url (internal test)"
curl -s $BASE_URL/opportunity/ingest -d '{"url": "http://localhost:8000/example/pages/opportunity"}' -H "Content-Type: application/json" | jq . | tee /tmp/test_new_oppo_ingest.json
COMPANY_INGEST_ID=`jq -r .company_id /tmp/test_new_oppo_ingest.json`
NEW_INGEST_ID=`jq -r .id /tmp/test_new_oppo_ingest.json`
echo COMPANY_INGEST_ID $COMPANY_INGEST_ID
echo NEW_INGEST_ID $NEW_INGEST_ID


if [ "$1" != "keep" ];
then
    echo "Delete test oppo by ingest"
    curl -s -X DELETE $BASE_URL/opportunity/$NEW_INGEST_ID | jq .

    echo "Delete test company by ingest"
    curl -s -X DELETE $BASE_URL/company/$COMPANY_INGEST_ID | jq .

    echo "Delete test oppo"
    curl -s -X DELETE $BASE_URL/opportunity/$NEW_ID | jq .

    echo "Delete test company"
    curl -s -X DELETE $BASE_URL/company/$COMPANY_ID | jq .
fi


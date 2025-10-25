#!/usr/bin/env bash
BASE_URL=http://127.0.0.1:8000

echo "Existing"
curl -s $BASE_URL/opportunity/1 | jq .
curl -s $BASE_URL/opportunity/2 | jq .
curl -s $BASE_URL/opportunity/3 | jq .

echo "Update"
curl -s $BASE_URL/opportunity/2 -X PUT -d '{"id": "2", "company_id": "2", "position": "N/A", "process": {"items": [{"type_": "Panel", "location": "in-person", "with_": "internal"}]}}' -H "Content-Type: application/json" | jq .

echo "Create new"
curl -s $BASE_URL/opportunity -d '{"company_id": "1", "position": "exciting", "process": {"items": []}}' -H "Content-Type: application/json" | jq .

echo "Update"
curl -s $BASE_URL/opportunity/4 -X PUT -d '{"id": "4", "company_id": "1", "position": "N/A", "process": {"items": []}}' -H "Content-Type: application/json" | jq .

echo "Delete new"
curl -s -X DELETE $BASE_URL/opportunity/4

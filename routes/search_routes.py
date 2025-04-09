from flask import Blueprint, request, jsonify
import pandas as pd

search_bp = Blueprint('search_bp', __name__)

# Load the Excel file (only once)
excel_data = pd.read_excel("certificates/test.xlsx", sheet_name=0)
excel_data.columns = excel_data.columns.str.strip().str.upper().str.replace('\n', ' ').str.replace('\xa0', ' ')
print("AVAILABLE COLUMNS:", excel_data.columns.tolist())


@search_bp.route('/search', methods=['POST'])
def search_item():
    item_no = request.json.get('itemNumber')
    if not item_no:
        return jsonify([])

    # Normalize both sides
    item_no = str(item_no).strip().upper()
    excel_data['ITEM NUMBER'] = excel_data['ITEM NUMBER'].astype(str).str.strip().str.upper()

    print("Item Number Received:", item_no)
    print("Sample ITEM NUMBERs:", excel_data['ITEM NUMBER'].head(10).tolist())

    matches = excel_data[excel_data['ITEM NUMBER'] == item_no]
    if matches.empty:
        print("No matches found.")
        return jsonify([])

    filtered = matches[[
        "ITEM NUMBER",
        "NAME",
        "POSITION TITLE",
        "SCHOOL NAME",
        "PLANTILLA DATE OF FIRST APPOINTMENT AS PERMANENT (MONTH, DAY, YEAR)",
        "SALARY",
        "ACTUAL DATE OF LATEST APPOINTMENT  (MONTH, DAY, YEAR)"
    ]]

    records = filtered.rename(columns={
        "ITEM NUMBER": "ItemNumber",
        "NAME": "Name",
        "POSITION TITLE": "Position Title",
        "SCHOOL NAME": "School Name",
        "PLANTILLA DATE OF FIRST APPOINTMENT AS PERMANENT (MONTH, DAY, YEAR)": "StartDate",
        "SALARY": "Salary",
        "ACTUAL DATE OF LATEST APPOINTMENT  (MONTH, DAY, YEAR)": "PromotionDate"
    }).to_dict(orient='records')


    return jsonify(records)


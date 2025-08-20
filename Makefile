reset:
	jq 'walk(if type=="object" and has("subject_name") then .subject_name="" else . end)' dataset/timetable.json > dataset/timetable.json.tmp && mv dataset/timetable.json.tmp dataset/timetable.json

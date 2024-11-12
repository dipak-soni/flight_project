from rest_framework import serializers

class TravelEntrySerializer(serializers.Serializer):
    travel_entry_id = serializers.IntegerField()
    user_id = serializers.CharField()
    event_id = serializers.CharField()
    planner_id = serializers.CharField()
    airport_code = serializers.CharField()
    files = serializers.ListField(
        child=serializers.FileField(),
        required=True
    )
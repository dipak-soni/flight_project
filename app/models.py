from django.db import models

# Create your models here.

class User(models.Model):
    travel_entry_id=models.IntegerField(primary_key=True)
    class Meta:
        db_table = "user"
    
    def __str__(self):
        return str(self.travel_entry_id)
        

class Ticket(models.Model):
    id=models.AutoField(primary_key=True)
    travel_entry_id=models.ForeignKey(User, on_delete=models.CASCADE)
    event_id=models.CharField(max_length=25)
    planner_id=models.CharField(max_length=25)
    user_id=models.CharField(max_length=25)
    flight_no = models.CharField(max_length=10, null=True, blank=True)
    passenger_name = models.CharField(max_length=100, null=True, blank=True)
    source_location = models.CharField(max_length=100, null=True, blank=True)
    departure_date = models.CharField(max_length=50,null=True, blank=True)
    departure_time = models.CharField(max_length=50,null=True, blank=True)
    arrival_date = models.CharField(max_length=50,null=True, blank=True)
    arrival_time = models.CharField(max_length=50,null=True, blank=True)
    arrival_location = models.CharField(max_length=100, null=True, blank=True)
    airline_name = models.CharField(max_length=100, null=True, blank=True)
    ticket_type=models.CharField(max_length=25,null=True, blank=True)
    dtentry=models.DateTimeField(auto_now=True)
    iGuestId=models.CharField(max_length=25, null=True, blank=True)
    cStatus=models.CharField(max_length=25, null=True, blank=True)
    
    class Meta:
        db_table = "ticket"
    
    def __str__(self):
        return f"{self.flight_no} - {self.passenger_name}"
    

from django.db import models
from users.models import User


class SupportTicket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_description = models.TextField(max_length=1000)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed'), ('in_progress', 'In Progress')], default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support Ticket {self.ticket_id} - {self.status}"


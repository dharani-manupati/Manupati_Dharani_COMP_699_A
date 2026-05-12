from app.database import db
from datetime import datetime


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)

    # Owner (Employee)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    # Optional: link to leave request
    leave_request_id = db.Column(db.Integer, db.ForeignKey('leave_requests.id'), nullable=True)

    # File Details
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))  # pdf, jpg, png, etc.
    file_size = db.Column(db.Integer)  # in bytes

    # Upload Info
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Verification (HR can verify documents)
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('hr_admins.id'), nullable=True)
    verified_at = db.Column(db.DateTime)

    # Status
    status = db.Column(db.String(20), default='active')
    # values: active, archived, deleted

    # =========================
    # BUSINESS LOGIC METHODS
    # =========================

    def mark_verified(self, hr_id):
        """
        HR verifies the document
        """
        self.is_verified = True
        self.verified_by = hr_id
        self.verified_at = datetime.utcnow()

    def archive(self):
        """
        Archive document (soft delete)
        """
        self.status = 'archived'

    def delete(self):
        """
        Mark document as deleted (soft delete)
        """
        self.status = 'deleted'

    def __repr__(self):
        return f"<Document {self.file_name} Emp:{self.employee_id}>"
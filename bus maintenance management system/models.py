from datetime import datetime
from app import db

class MaintenanceUpdate(db.Model):
    """Model for storing maintenance updates for buses."""
    
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.String(10), db.ForeignKey('bus.id'), nullable=False, index=True)  # Foreign key reference
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tires = db.Column(db.String(100), nullable=True)
    brakes = db.Column(db.String(100), nullable=True)
    oil = db.Column(db.String(100), nullable=True)
    engine = db.Column(db.String(100), nullable=True)
    lights = db.Column(db.String(100), nullable=True)
    engine_performance = db.Column(db.String(100), nullable=True)
    transmission_fluid = db.Column(db.String(100), nullable=True)
    battery_charger = db.Column(db.String(100), nullable=True)
    brake_pads = db.Column(db.String(100), nullable=True)
    comments = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<MaintenanceUpdate {self.bus_id} on {self.date}>'


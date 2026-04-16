"""
Modelos de base de datos — User y CalculationHistory.
"""
import json
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(UserMixin, db.Model):
    """Usuario de la plataforma."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    display_name = db.Column(db.String(120), default="")
    preferred_lang = db.Column(db.String(5), default="es")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    calculations = db.relationship(
        "CalculationHistory", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class CalculationHistory(db.Model):
    """Registro de cada cálculo realizado por un usuario."""
    __tablename__ = "calculation_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    method_name = db.Column(db.String(100), nullable=False)
    method_description = db.Column(db.String(200), default="")
    matrix_input = db.Column(db.Text, nullable=False)   # JSON
    vector_input = db.Column(db.Text, nullable=False)   # JSON
    solution = db.Column(db.Text, nullable=False)        # JSON
    steps_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_matrix(self, matrix: list):
        self.matrix_input = json.dumps(matrix)

    def get_matrix(self) -> list:
        return json.loads(self.matrix_input)

    def set_vector(self, vector: list):
        self.vector_input = json.dumps(vector)

    def get_vector(self) -> list:
        return json.loads(self.vector_input)

    def set_solution(self, solution: list):
        self.solution = json.dumps(solution)

    def get_solution(self) -> list:
        return json.loads(self.solution)

    def __repr__(self):
        return f"<Calc #{self.id} {self.method_name} by user {self.user_id}>"

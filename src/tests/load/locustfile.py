"""
@file:          tests/load/locustfile.py
@description:   Locust load testing script for the FastAPI application simulating full user workflow.
@date:          30 July 2026
@last modified:   30 July 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

import uuid
import random
from locust import HttpUser, task, between

class TodoUser(HttpUser):
    wait_time = between(0.01, 3)
    token = None
    created_todo_ids = []

    def on_start(self):
        """Executed when a Locust user starts. Registers & logs in to obtain JWT token."""
        unique_id = str(uuid.uuid4())[:8]
        self.email = f"load_user_{unique_id}@example.com"
        self.password = "Password@123"
        self.name = f"LoadUser {unique_id}"

        # 1. Register user
        reg_resp = self.client.post("/api/v1/users/", json={
            "username": self.name,
            "email": self.email,
            "password": self.password
        })

        if reg_resp.status_code not in (200, 201):
            # Fallback in case user exists
            pass

        # 2. Acquire access token
        token_resp = self.client.post("/api/v1/users/token", json={
            "email": self.email,
            "password": self.password
        })

        if token_resp.status_code == 200:
            data = token_resp.json()
            header = {"Bearer": data["access_token"] }
            self.client.headers.update(header)

    @task(3)
    def list_todos(self):
        """Fetch all todos for logged in user."""
        self.client.get("/api/v1/todo/")

    @task(2)
    def create_todo(self):
        """Create a new todo with items."""
        payload = {
            "title": f"Load Test Todo {random.randint(1, 1000)}",
            "items": [
                {"item": "Task item 1", "is_checked": False},
                {"item": "Task item 2", "is_checked": True}
            ]
        }
        res = self.client.post("/api/v1/todo/", json=payload)
        if res.status_code in (200, 201):
            todo_data = res.json()
            if "id" in todo_data:
                self.created_todo_ids.append(todo_data["id"])

    @task(2)
    def update_todo(self):
        """Patch update title and status of a todo."""
        if not self.created_todo_ids:
            return
        todo_id = random.choice(self.created_todo_ids)
        patch_payload = {
            "title": f"Updated Title {random.randint(1, 1000)}",
            "status": random.choice(["pending", "completed", "skipped"])
        }
        self.client.patch(f"/api/v1/todo/{todo_id}", json=patch_payload)

    @task(1)
    def update_todo_items(self):
        """Patch update items of a todo."""
        if not self.created_todo_ids:
            return
        todo_id = random.choice(self.created_todo_ids)
        patch_payload = {
            "items": [
                {"item": "Updated Task item 1", "is_checked": True},
                {"item": "Updated Task item 2", "is_checked": False}
            ]
        }
        self.client.patch(f"/api/v1/todo/{todo_id}/items", json=patch_payload)

    @task(3)
    def update_existing_todo_item(self):
        """Patch update a specific item of a todo."""
        if not self.created_todo_ids:
            return
        todo_id = random.choice(self.created_todo_ids)
        # Fetch the todo to get its items
        res = self.client.get(f"/api/v1/todo/{todo_id}")
        if res.status_code != 200:
            return
        todo_data = res.json()
        items = todo_data.get("items", [])
        if not items:
            return
        item_to_update = random.choice(items)
        item_id = item_to_update.get("id")
        patch_payload = {
            "items":[
                {
                    "id": item_id,
                    "item": f"Updated Specific Item {random.randint(1, 1000)}",
                    "is_checked": not item_to_update.get("is_checked", False)
                }
            ]
        }
        self.client.patch(f"/api/v1/todo/{todo_id}/items/{item_id}", json=patch_payload)

    @task(1)
    def delete_todo(self):
        """Delete a todo item."""
        if not self.created_todo_ids:
            return
        todo_id = self.created_todo_ids.pop()
        self.client.delete(f"/api/v1/todo/{todo_id}")

    def on_stop(self):
        """Delete all created todos for this user."""
        for todo_id in self.created_todo_ids:
            self.client.delete(f"/api/v1/todo/{todo_id}")
        self.created_todo_ids.clear()
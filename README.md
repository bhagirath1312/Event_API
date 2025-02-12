# Event Management API Documentation

## Overview
The Event Management API provides endpoints for user authentication, event management, and registration. It supports role-based access for attendees, organizers, and administrators.

## Base URL
```
http://localhost:8000/api
```

## Authentication
### 1. Register a New User
**Endpoint:** `POST /auth/register`

**Description:** Registers a new user in the system.

**Request Body:**
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "securepassword",
  "role": "attendee"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "attendee"
}
```

### 2. User Login
**Endpoint:** `POST /auth/login`

**Description:** Authenticates a user and returns a JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "expires_in": 60
}
```

### 3. Get Current User
**Endpoint:** `GET /auth/me`

**Headers:**
```json
{
  "Authorization": "Bearer jwt_token_here"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "attendee"
}
```

---

## User Management
### 4. Update User Role
**Endpoint:** `PUT /auth/me/update-role`

**Description:** Updates the current user's role (attendee/organizer).

**Request Body:**
```json
{
  "new_role": "organizer"
}
```

**Response:**
```json
{
  "message": "Role updated successfully to organizer"
}
```

---

## Events
### 5. Create an Event
**Endpoint:** `POST /events`

**Description:** Allows an organizer to create a new event.

**Request Body:**
```json
{
  "title": "Tech Conference 2025",
  "description": "A conference about the latest in tech.",
  "event_date": "2025-06-15T10:00:00",
  "location": "New York, USA",
  "max_capacity": 100,
  "registration_deadline": "2025-06-10T23:59:59",
  "category": "Technology",
  "status": "upcoming"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Tech Conference 2025",
  "description": "A conference about the latest in tech.",
  "event_date": "2025-06-15T10:00:00",
  "location": "New York, USA",
  "max_capacity": 100,
  "registration_deadline": "2025-06-10T23:59:59",
  "category": "Technology",
  "status": "upcoming",
  "user_id": 2
}
```

### 6. Get All Events
**Endpoint:** `GET /events`

**Response:**
```json
[
  {
    "id": 1,
    "title": "Tech Conference 2025",
    "location": "New York, USA",
    "status": "upcoming"
  }
]
```

### 7. Get Event by ID
**Endpoint:** `GET /events/{event_id}`

**Response:**
```json
{
  "id": 1,
  "title": "Tech Conference 2025",
  "location": "New York, USA",
  "status": "upcoming"
}
```

### 8. Update an Event
**Endpoint:** `PUT /events/{event_id}`

**Request Body:** _(Optional fields)_
```json
{
  "title": "Updated Conference Title",
  "status": "ongoing"
}
```

**Response:**
```json
{
  "message": "Event updated successfully"
}
```

### 9. Delete an Event
**Endpoint:** `DELETE /events/{event_id}`

**Response:**
```json
{
  "message": "Event deleted successfully"
}
```

---

## Registration
### 10. Register for an Event
**Endpoint:** `POST /events/{event_id}/register`

**Response:**
```json
{
  "message": "Successfully registered for the event",
  "event_id": 1
}
```

### 11. Admin Registration for an Event
**Endpoint:** `POST /events/{event_id}/admin-register`

**Request Body:**
```json
{
  "user_id": 3
}
```

**Response:**
```json
{
  "message": "Admin successfully registered user for event"
}
```

### 12. Cancel Registration
**Endpoint:** `DELETE /events/{event_id}/registrations/{user_id}`

**Response:**
```json
{
  "message": "Registration cancelled successfully"
}
```

### 13. Get Registered Events for a User
**Endpoint:** `GET /your-registered-events`

**Response:**
```json
{
  "user_id": 1,
  "registered_events": [
    {
      "id": 1,
      "title": "Tech Conference 2025"
    }
  ]
}
```

---

## Admin Actions
### 14. Admin Actions Overview
**Admin users can:**
- View all users.
- Assign and update roles.
- Register users for events.
- Manage events.

### 15. Get All Users
**Endpoint:** `GET /admin/users`

**Response:**
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "role": "attendee"
  }
]
```

### 16. Update User Role (Admin)
**Endpoint:** `PUT /admin/users/{user_id}/role`

**Request Body:**
```json
{
  "role": "organizer"
}
```

**Response:**
```json
{
  "message": "User role updated successfully"
}
```

---

## Error Responses
Common error responses:

```json
{
  "detail": "Unauthorized"
}
```
```json
{
  "detail": "Event is full"
}
```
```json
{
  "detail": "User not found"
}
```

---

## Conclusion
This API provides a complete event management system with authentication, event handling, and role-based access control.


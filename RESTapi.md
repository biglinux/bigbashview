
---

# File API Documentation

## Introduction

This API provides a simple yet powerful way to manage JSON files on a server. It's built on Python's web.py framework and offers basic CRUD (Create, Read, Update, Delete) operations. This API is particularly useful for applications that need to persistently store configuration data, user settings, or any other JSON-serializable information.

## Base URL

The foundational URL for all API endpoints is:

```
http://<your_server_ip>:<port>/api/file
```

Replace `<your_server_ip>` and `<port>` with the actual IP address and port where your server is running.

## API Endpoints

### Read a File (GET)

**Utility:**  
Reading a file is essential for any configuration-driven application, or for initializing an application state based on stored data.

**Example:**

```http
GET http://localhost:19000/api/file?filename=$HOME/myfile.json
```

### Create a File (POST)

**Utility:**  
Creating a new JSON file is often needed for storing initial settings, saving a new user profile, or recording application state to be restored later.

**Example:**

```http
POST http://localhost:19000/api/file?filename=$HOME/newfile.json
```

**Request Body:**

```json
{
    "key": "value"
}
```

### Update a File (PUT)

**Utility:**  
Updating a file is crucial for modifying settings or state without affecting other existing data. For instance, you can update a user's profile, or modify specific configuration parameters while keeping others intact.

**Example:**

```http
PUT http://localhost:19000/api/file?filename=$HOME/existingfile.json
```

**Request Body:**

```json
{
    "new_key": "new_value"
}
```

### Delete a File (DELETE)

**Utility:**  
The ability to delete a file is important for clean-up operations, like removing user profiles or old configuration files that are no longer needed.

**Example:**

```http
DELETE http://localhost:19000/api/file?filename=$HOME/deletefile.json
```

## Special Features

### Home Directory Resolution

**Utility:**  
The `$HOME` variable allows users to specify files relative to the home directory of the user running the server. This feature is beneficial for multi-user systems where each user has their own space and makes the API calls more concise.

**Example:**

```http
GET http://localhost:19000/api/file?filename=$HOME/myfile.json
```

This will read `myfile.json` from the home directory of the user running the server.

---

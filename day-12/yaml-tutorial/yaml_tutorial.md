# YAML Tutorial – From Basics to Advanced

**YAML** = **Y**AML **A**in’t **M**arkup **L**anguage.  
It’s a human-readable data format for configuration files.  

---

## 🔑 1. Basic Structure

- YAML uses **indentation** (spaces only, no tabs ❌).
- Data is represented as **key: value** pairs.

```yaml
name: John Doe
age: 28
country: India
```

---

## 🔑 2. Lists (Arrays)

Use a dash (`-`) to represent lists:

```yaml
fruits:
  - apple
  - banana
  - mango
```

Equivalent in Python:

```python
["apple", "banana", "mango"]
```

---

## 🔑 3. Nested Structures

You can combine dictionaries and lists:

```yaml
person:
  name: Alice
  age: 30
  hobbies:
    - painting
    - reading
    - cycling
```

---

## 🔑 4. Data Types

YAML supports various data types:

```yaml
string: "Hello World"
integer: 42
float: 3.14
boolean_true: true
boolean_false: false
null_value: null
```

---

## 🔑 5. Multi-line Strings

Use `|` (literal) or `>` (folded):

```yaml
bio: |
  This is line 1
  This is line 2
  This keeps line breaks.

quote: >
  This is line 1
  This is line 2
  This folds into a single paragraph.
```

---

## 🔑 6. References & Anchors

Reuse values with anchors (`&`) and aliases (`*`):

```yaml
default: &default
  country: India
  active: true

user1:
  <<: *default
  name: Raj

user2:
  <<: *default
  name: Priya
```

Both users inherit `country: India` and `active: true`.

---

## 🔑 7. YAML vs JSON

YAML is a superset of JSON.  

This JSON:

```json
{
  "name": "Alice",
  "age": 25
}
```

is valid YAML:

```yaml
name: Alice
age: 25
```

---

## 🔑 8. Real-world Examples

### (a) **Docker Compose (docker-compose.yml)**
```yaml
version: "3"
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
  db:
    image: postgres:latest
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
```

---

### (b) **Kubernetes Deployment (deployment.yml)**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp-container
          image: myapp:1.0
          ports:
            - containerPort: 8080
```

---

### (c) **GitHub Actions Workflow (.github/workflows/ci.yml)**
```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Install Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Run Tests
        run: |
          pip install -r requirements.txt
          pytest
```

---

## ✅ Best Practices

1. Always use **spaces**, not tabs.
2. Keep indentation consistent.
3. Use quotes if your strings have `:`, `#`, or special characters.
4. Validate YAML with online tools (`yamllint`) or in IDEs.
5. Comment with `#`:

```yaml
name: Alice   # This is a comment
```

---

🎯 YAML is powerful, simple, and widely used in DevOps, Cloud, and Machine Learning projects.

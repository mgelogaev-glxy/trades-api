# 📚 COMPLETE STUDY GUIDE - TRADES & POSITIONS API

## 🎯 PROJECT OVERVIEW

### What You Built
A REST API with FastAPI that queries a SQLite database to:

- **GET /trades** - Filter and retrieve trade records with pagination  
- **GET /positions** - Calculate net positions (BUY - SELL) per cryptocurrency symbol

### Tech Stack
- **Language:** Python 3  
- **Framework:** FastAPI (web framework)  
- **Database:** SQLite (file-based database)  
- **Testing:** pytest + httpx  
- **Tools:** uvicorn (ASGI server), virtual environment

### Architecture
- **Functional programming** - No classes, pure functions  
- **Separation of concerns** - `db.py` (database) + `api.py` (HTTP endpoints)  
- **Simple & clean** - Easy to understand and maintain

---

## 📖 KEY CONCEPTS YOU LEARNED

### 1. SQL QUERIES

#### Basic SELECT with WHERE
- `SELECT` = Choose which columns to return  
- `FROM` = Which table to query  
- `WHERE` = Filter rows (like Excel filter)  
- `?` = Placeholder for safe parameter substitution (prevents SQL injection)

#### Multiple filters with AND
- `AND` = All conditions must be true  
- `UPPER()` = Convert to uppercase for case-insensitive comparison

#### Sorting
- `ORDER BY` = Sort results  
- `ASC` = Ascending (oldest first)  
- `DESC` = Descending (newest first)

#### Pagination
- `LIMIT` = How many rows to return (page size)  
- `OFFSET` = How many rows to skip (for pagination)  

Example: Skip first 40, return next 20 (page 3 with `page_size=20`)

#### Aggregation with GROUP BY
```sql
SELECT symbol,
       SUM(CASE WHEN side='BUY' THEN quantity
                WHEN side='SELL' THEN -quantity
                ELSE 0 END) AS net_position
FROM trades
GROUP BY symbol;
```

---

### 2. FASTAPI

#### What is FastAPI?
Modern Python web framework for building APIs:

- Auto-generates OpenAPI documentation  
- Built-in data validation  
- Fast and async-ready  
- Type hints for better code

#### Key Components

1. **Decorators (@app.get)**  
   Registers the function as a GET endpoint

2. **Query Parameters**  
   - `Query(...)` = required  
   - `Query(None)` = optional  
   - Includes `description=`, `ge=`, `le=` for validation

3. **Validation**  
   Automatic parameter validation (returns 422 if invalid)

4. **Error Handling**  
   Returns 500 if server error occurs

#### HTTP Status Codes
- **200** = Success  
- **422** = Validation error (bad input)  
- **500** = Server error  

---

### 3. PAGINATION

#### The Problem
Returning all data at once is slow and wasteful.

#### The Solution
Paginate results with **page** and **page_size**.

| Page | Page Size | Offset | SQL | Results |
|------|------------|---------|-----|----------|
| 1 | 20 | 0 | LIMIT 20 OFFSET 0 | Trades 1–20 |
| 2 | 20 | 20 | LIMIT 20 OFFSET 20 | Trades 21–40 |
| 3 | 20 | 40 | LIMIT 20 OFFSET 40 | Trades 41–60 |

Formula:  
`OFFSET = (page - 1) * page_size`

---

### 4. PYTHON CONCEPTS

#### Type Hints
```python
account_id: int
Optional[str]
-> List[Dict]
```

#### `.append()` vs `.extend()`
`extend()` is used for SQL param lists to flatten arguments.

---

### 5. DATABASE (SQLite)

- File-based, no server needed  
- Perfect for small datasets  
- Uses `sqlite3` (built-in Python library)

#### SQL Injection Prevention
Use parameterized queries (`?` placeholders).

---

### 6. TESTING WITH PYTEST

#### Structure
```python
client.get(url)
response.status_code
response.json()
assert ...
```

#### What You Tested
- Required parameter validation (422)  
- Data structure correctness  
- Filtering and sorting logic  
- Net position calculations  

---

## 🔑 YOUR DESIGN DECISIONS

### Why FastAPI?
✅ Modern, validated, documented, fast.

### Why SQLite?
✅ Simple setup, perfect for small data.

### Why Functional Programming?
✅ Simple, pure, testable functions.

### Why Case-Insensitive Symbol Matching?
✅ Better UX.

### Why Pagination?
✅ Scalability, efficiency, production-ready.

### Why Position Calculation in SQL?
✅ Database aggregation is faster.

---

## 🎤 POTENTIAL INTERVIEW QUESTIONS & ANSWERS

### Technical Questions

**Q1:** How does `/trades` work?  
**A:** Validates input → builds SQL query dynamically → executes safely → returns JSON.

**Q2:** How does `/positions` work?  
**A:** Aggregates trades using `SUM(CASE WHEN...) GROUP BY symbol` for net positions.

**Q3:** Why pagination?  
**A:** Performance, UX, scalability, best practice.

**Q4:** How prevent SQL injection?  
**A:** Use parameterized queries (`?`).

**Q5:** Invalid `account_id`?  
**A:** Returns empty list (`[]`), not error.

**Q6:** Why not async?  
**A:** Simpler, SQLite is synchronous, dataset is small.

---

### Design Questions

**Q7:** What would you change for production?  
Authentication, rate limiting, ISO-8601 validation, connection pooling, monitoring, etc.

**Q8:** How handle millions of trades?  
Indexes, pagination, caching, async, partitioning, Redis.

**Q9:** Why functional, not OOP?  
Simplicity and clarity for small-scale project.

---

### Code Change Requests

**Q10:** Add filter for trades above certain price.  
✅ Add to query in both `api.py` and `db.py`.

**Q11:** Return total count with paginated results.  
✅ Add count query and include in JSON response.

**Q12:** Sort by price instead of timestamp.  
✅ Add `sort_by` param, whitelist fields.

**Q13:** Filter by multiple symbols.  
✅ Accept list input (`List[str]`) and use `IN (...)` in SQL.

---

### Behavioral Questions

**Q14:** Most challenging part?  
Getting SQL aggregation right with `CASE` + `GROUP BY`.

**Q15:** How did you test?  
Manual, automated with pytest, and real dataset validation.

**Q16:** If had more time?  
Add error handling, Dockerization, UI visualization, async, metrics.

---

## 📋 QUICK REFERENCE CHEAT SHEET

### SQL Quick Reference
```sql
SELECT * FROM trades WHERE account_id=? LIMIT ? OFFSET ?;
```

### FastAPI Quick Reference
```python
@app.get("/trades")
def get_trades(account_id: int = Query(...), page: int = 1, page_size: int = 20):
    ...
```

### Pagination Formula
```
OFFSET = (page - 1) * page_size
```

---

## 🎯 FINAL TIPS FOR INTERVIEW

✅ Be confident  
✅ Explain choices and trade-offs  
✅ Admit what you don’t know  
✅ Show enthusiasm  
✅ Ask about their tech stack

**Power Phrases:**
> "I chose X over Y because..."  
> "In production, I’d also consider..."  
> "Let me walk you through this..."

---

## 🚀 YOU'RE READY!

You built:
- ✅ Fully functional API  
- ✅ Pagination  
- ✅ Tests  
- ✅ Clean code

You learned:
- ✅ SQL aggregation  
- ✅ FastAPI validation  
- ✅ Testing fundamentals  
- ✅ Pagination logic  

**Good luck on Monday! 🎉**

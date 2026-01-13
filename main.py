# # This is a sample Python script.
#
# # Press ⌃F5 to execute it or replace it with your code.
# # Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
from tkinter.constants import INSERT

from fastapi import FastAPI, Request, HTTPException
import mysql.connector

app = FastAPI()

def get_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="tester",
        password="tester",
        database="llmagent"
    )


# ---------------------------
# CREATE
# ---------------------------
@app.post("/todos")
async def create_todo(request: Request):
    body = await request.json()
    content = body.get("content")

    if not content:
        raise HTTPException(status_code=400, detail="content is required")

    conn = get_db()
    cursor = conn.cursor()

    # 👉 학생이 작성해야 하는 SQL
    # INSERT 문 작성
    # 예: INSERT INTO todo (content) VALUES (%s)
    cursor.execute(
        "INSERT INTO todo (content) VALUES (%s)",  # 데이터 추가
        (content,)
    )
    conn.commit()

    todo_id = cursor.lastrowid

    # 👉 학생이 작성해야 하는 SQL
    # SELECT 문 작성하여 방금 만든 todo 조회
    cursor.execute(
        "SELECT id, content, created_at FROM todo WHERE id = %s",
        (todo_id,)
    )
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "content": row[1],
        "created_at": str(row[2])
    }


# ---------------------------
# READ
# ---------------------------
@app.get("/todos")
def get_todos():
    conn = get_db()
    cursor = conn.cursor()

    # 3. 전체 조회 SELECT 문 작성
    cursor.execute("SELECT id, content, created_at FROM todo")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {"id": r[0], "content": r[1], "created_at": str(r[2])}
        for r in rows
    ]


# ---------------------------
# DELETE
# ---------------------------
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db()
    cursor = conn.cursor()

    # 4. 삭제 DELETE 문 작성
    cursor.execute(
        "DELETE FROM todo WHERE id = %s",
        (todo_id,)
    )
    conn.commit()

    affected = cursor.rowcount  # 영향을 받은 행의 수

    cursor.close()
    conn.close()

    if affected == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted"}
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pymysql

app = FastAPI()
templates = Jinja2Templates(directory="templates")  

# DB Connection
def connection():
    conn = pymysql.connect(
        host="localhost",
        user="rajatjaiswal",
        password="rajat@2004",
        database="hospital",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

# HOME
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "message": "Hospital Patient Record System"})

# SHOW ALL
@app.get("/patients", response_class=HTMLResponse)
async def get_patients(request: Request):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "patients": patients})

# VIEW SINGLE
@app.get("/patients/{patient_id}", response_class=HTMLResponse)
async def get_patient(request: Request, patient_id: int):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id=%s", (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return templates.TemplateResponse("view.html", {"request": request, "patient": patient})

# ADD - FORM
@app.get("/patients/add", response_class=HTMLResponse)
async def add_patient_form(request: Request):
    return templates.TemplateResponse("form.html", {
        "request": request,
        "action_url": "/patients/add",
        "patient": None,
        "title": "Add Patient"
    })

# ADD - POST
@app.post("/patients/add", response_class=HTMLResponse)
async def add_patient(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    disease: str = Form(...),
    address: str = Form(...)
):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, age, disease, address) VALUES (%s,%s,%s,%s)",
                   (name, age, disease, address))
    conn.commit()
    conn.close()
    return RedirectResponse("/patients", status_code=303)

# UPDATE - FORM
@app.get("/patients/update/{patient_id}", response_class=HTMLResponse)
async def update_patient_form(request: Request, patient_id: int):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id=%s", (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return templates.TemplateResponse("form.html", {
        "request": request,
        "action_url": f"/patients/update/{patient_id}",
        "patient": patient,
        "title": "Update Patient"
    })

# UPDATE - POST
@app.post("/patients/update/{patient_id}", response_class=HTMLResponse)
async def update_patient(
    request: Request,
    patient_id: int,
    name: str = Form(...),
    age: int = Form(...),
    disease: str = Form(...),
    address: str = Form(...)
):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE patients SET name=%s, age=%s, disease=%s, address=%s WHERE id=%s",
                   (name, age, disease, address, patient_id))
    conn.commit()
    conn.close()
    return RedirectResponse("/patients", status_code=303)

# DELETE
@app.post("/patients/delete/{patient_id}", response_class=HTMLResponse)
async def delete_patient(request: Request, patient_id: int):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/patients", status_code=303)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
else :
    print("FastAPI app is ready to run.")   
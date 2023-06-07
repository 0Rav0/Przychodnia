## Endpointy
### Ogólne
http://localhost:8000/admin/

http://localhost:8000/api/login

http://localhost:8000/api/token/refresh/

http://localhost:8000/api/register

http://localhost:8000/api/email-verify 

## Dla pacjenta
http://localhost:8000/api/patient/profile

http://localhost:8000/api/free/0000-00-00/1   (data, pk doktora)

http://localhost:8000/api/patient/appointments 

http://localhost:8000/api/patient/appointments/1  (pk)

http://localhost:8000/api/patient/appointments/False     (status: False = przyszła, True=historia)
  
  
http://localhost:8000/api/patient/prescriptions 

http://localhost:8000/api/patient/prescriptions/1   (pk - wizyty)
 
## Dla lekarza  
http://localhost:8000/api/doctor/list

http://localhost:8000/api/doctor/1  (pk)

http://localhost:8000/api/doctor/profile 
  
  
http://localhost:8000/api/doctor/appointments 

http://localhost:8000/api/doctor/appointments/1   (pk)

http://localhost:8000/api/doctor/appointments/1/patient   (pk - wizyty)

### inne  
http://localhost:8000/api/reception/


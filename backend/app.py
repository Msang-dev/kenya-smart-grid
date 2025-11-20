from fastapi import FastAPI, HTTPException, Depends, status
app = FastAPI(title="Kenyan Smart Grid API", lifespan=lifespan)


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


# Utility functions


def verify_password(plain, hashed):
return pwd_context.verify(plain, hashed)


def get_password_hash(password):
return pwd_context.hash(password)


def create_access_token(data: dict):
to_encode = data.copy()
expire = datetime.utcnow() + timedelta(days=7)
to_encode.update({"exp": expire, "sub": data.get('sub')})
return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
token = credentials.credentials
try:
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
username = payload.get('sub')
if username is None:
raise HTTPException(status_code=401, detail='Invalid authentication')
return username
except jwt.PyJWTError:
raise HTTPException(status_code=401, detail='Invalid authentication')


# Routes
@app.get('/')
async def root():
return {"message":"Kenya Smart Grid Dispatch API","status":"ok"}


@app.post('/register')
async def register(u: UserRegister):
if supabase is None:
raise HTTPException(status_code=500, detail='Database not configured')
# check existing
res = supabase.table('users').select('*').eq('username', u.username).execute()
if res.data:
raise HTTPException(status_code=400, detail='username exists')
hashed = get_password_hash(u.password)
user_row = {
'username': u.username,
'email': u.email,
'password_hash': hashed,
'full_name': u.full_name,
'role': 'operator',
'created_at': datetime.utcnow().isoformat()
}
supabase.table('users').insert(user_row).execute()
token = create_access_token({'sub': u.username})
return {'message':'registered','access_token': token}


@app.post('/login')
async def login(u: UserLogin):
if supabase is None:
raise HTTPException(status_code=500, detail='Database not configured')
res = supabase.table('users').select('*').eq('username', u.username).execute()
if not res.d

CREATE TABLE leads (
  id SERIAL PRIMARY KEY,
  name TEXT,
  email TEXT,
  user_type TEXT,
  company TEXT,
  message TEXT,
  extra_info TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
